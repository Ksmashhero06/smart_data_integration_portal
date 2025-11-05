from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from blockchain import Blockchain
from audit_log import AuditLog
import uuid
import json
import os
import base64
import time
from datetime import datetime
from io import BytesIO

app = Flask(__name__)
app.secret_key = 'super_secret_key_123'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Determine base directory for file storage
BASE_DIR = '/app' if os.environ.get('RENDER') else os.path.dirname(os.path.abspath(__file__))

# File paths
USER_FILE = os.path.join(BASE_DIR, 'users.json')
ATTACK_RESULT_FILE = os.path.join(BASE_DIR, 'attack_results.json')
SNAPSHOT_FILE = os.path.join(BASE_DIR, 'snapshots.json')
ANNUAL_REPORT_FILE = os.path.join(BASE_DIR, 'annual_reports.json')

def load_users():
    """Load users from users.json or initialize with default users."""
    default_users = {
        'student1': {'password': 'pass123', 'role': 'student', 'id': str(uuid.uuid4())},
        'faculty1': {'password': 'pass456', 'role': 'faculty', 'id': str(uuid.uuid4())},
        'admin1': {'password': 'pass789', 'role': 'admin', 'id': str(uuid.uuid4())},
        'developer1': {'password': 'pass101', 'role': 'developer', 'id': str(uuid.uuid4())}
    }
    if os.path.exists(USER_FILE):
        try:
            with open(USER_FILE, 'r') as f:
                users = json.load(f)
                for username, data in users.items():
                    if 'id' not in data:
                        data['id'] = str(uuid.uuid4())
                return users
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading users.json: {e}")
    save_users(default_users)
    return default_users

def save_users(users):
    """Save users to users.json."""
    try:
        with open(USER_FILE, 'w') as f:
            json.dump(users, f, indent=4)
    except IOError as e:
        print(f"Error saving users: {e}")

def load_annual_reports():
    """Load annual reports from annual_reports.json."""
    if os.path.exists(ANNUAL_REPORT_FILE):
        try:
            with open(ANNUAL_REPORT_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}

def save_annual_reports(reports):
    """Save annual reports to annual_reports.json."""
    try:
        with open(ANNUAL_REPORT_FILE, 'w') as f:
            json.dump(reports, f, indent=4)
    except IOError as e:
        print(f"Error saving annual reports: {e}")

users = load_users()
blockchain = Blockchain()
audit_log = AuditLog()
annual_reports = load_annual_reports()

class User(UserMixin):
    """User model for Flask-Login."""
    def __init__(self, user_id, username, role):
        self.id = user_id
        self.username = username
        self.role = role

@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login."""
    for username, data in users.items():
        if data['id'] == user_id:
            return User(user_id, username, data['role'])
    return None

@app.template_filter('datetime')
def format_datetime(timestamp):
    """Format timestamp as readable datetime."""
    try:
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    except (ValueError, TypeError):
        return "Invalid Timestamp"

@app.route('/')
def index():
    """Render the homepage."""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('homepage.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if not username or not password:
            flash('Username and password are required', 'error')
            return redirect(url_for('login'))
        if username in users and users[username]['password'] == password:
            user = User(users[username]['id'], username, users[username]['role'])
            login_user(user)
            audit_log.log_action(username, 'login', f'User {username} logged in')
            return redirect(url_for('dashboard'))
        flash('Invalid credentials', 'error')
    return render_template('homepage.html')

@app.route('/logout')
@login_required
def logout():
    """Handle user logout."""
    audit_log.log_action(current_user.username, 'logout', f'User {current_user.username} logged out')
    logout_user()
    flash('You have been logged out successfully', 'success')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Render role-specific dashboard."""
    try:
        if current_user.role == 'student':
            student_annual_reports = {
                report_id: report for report_id, report in annual_reports.items()
                if report.get('target') == 'Student'
            }
            return render_template('dashboard_student.html', 
                                 records=blockchain.get_student_records(), 
                                 annual_reports=student_annual_reports)
        elif current_user.role == 'faculty':
            faculty_annual_reports = {
                report_id: report for report_id, report in annual_reports.items()
                if report.get('author') == current_user.username
            }
            return render_template('dashboard_faculty.html', 
                                 reports=blockchain.get_reports(), 
                                 annual_reports=faculty_annual_reports, 
                                 users=users)
        elif current_user.role == 'admin':
            return render_template('dashboard_admin.html', 
                                 users=users, 
                                 logs=audit_log.get_logs(), 
                                 annual_reports=annual_reports)
        elif current_user.role == 'developer':
            attack_result = None
            snapshot_result = None
            if os.path.exists(ATTACK_RESULT_FILE):
                try:
                    with open(ATTACK_RESULT_FILE, 'r') as f:
                        attack_result = json.load(f)
                except (json.JSONDecodeError, IOError):
                    attack_result = None
            if os.path.exists(SNAPSHOT_FILE):
                try:
                    with open(SNAPSHOT_FILE, 'r') as f:
                        snapshot_result = json.load(f)
                except (json.JSONDecodeError, IOError):
                    snapshot_result = None
            return render_template('dashboard_developer.html', 
                                 validation=blockchain.validate_chain(), 
                                 metrics=blockchain.get_quality_metrics(), 
                                 logs=audit_log.get_logs(),
                                 attack_result=attack_result,
                                 snapshot_result=snapshot_result)
        return 'Unauthorized', 403
    except Exception as e:
        flash(f'Error loading dashboard: {str(e)}', 'error')
        return redirect(url_for('logout'))

@app.route('/submit_annual_report', methods=['POST'])
@login_required
def submit_annual_report():
    """Handle annual report submission for faculty and admin."""
    if current_user.role not in ['faculty', 'admin']:
        return 'Unauthorized', 403
    try:
        report_data = request.form.get('report_data')
        category = request.form.get('category')
        target = request.form.get('target')
        event_date = request.form.get('event_date')
        from_date = request.form.get('from_date')
        to_date = request.form.get('to_date')
        department = request.form.get('department')
        certificate = request.files.get('certificate')

        # Validate inputs
        if not all([report_data, category, target, department]):
            flash('All fields are required except certificate', 'error')
            return redirect(url_for('dashboard'))

        # Determine event dates
        if event_date:
            from_date = event_date
            to_date = event_date
        elif not (from_date and to_date):
            flash('Please provide valid event dates', 'error')
            return redirect(url_for('dashboard'))

        # Handle certificate upload
        certificate_data = None
        certificate_filename = None
        if certificate and certificate.filename:
            if certificate.filename.endswith(('.pdf', '.png', '.jpg', '.jpeg')):
                certificate_data = base64.b64encode(certificate.read()).decode('utf-8')
                certificate_filename = certificate.filename
            else:
                flash('Certificate must be PDF, PNG, JPG, or JPEG', 'error')
                return redirect(url_for('dashboard'))

        # Validate the report
        validation_result = blockchain.validate_annual_report(
            report_data, category, from_date, to_date, department, current_user.username
        )
        if validation_result != 'valid':
            flash(f'Annual report validation failed: {validation_result}', 'error')
            return redirect(url_for('dashboard'))

        report_id = str(uuid.uuid4())
        block = blockchain.add_annual_report(
            report_id, report_data, category, from_date, to_date, department, 
            current_user.username, target
        )
        annual_reports[report_id] = {
            'data': report_data,
            'category': category,
            'from_date': from_date,
            'to_date': to_date,
            'department': department,
            'author': current_user.username,
            'target': target,
            'timestamp': block['timestamp'],
            'certificate': certificate_data,
            'certificate_filename': certificate_filename,
            'hash': block['hash']
        }
        save_annual_reports(annual_reports)
        audit_log.log_action(
            current_user.username, 
            'submit_annual_report', 
            f'Annual report {report_id} submitted ({category}) for {target}'
        )
        flash('Annual report submitted successfully')
    except Exception as e:
        flash(f'Error submitting report: {str(e)}', 'error')
    return redirect(url_for('dashboard'))

@app.route('/update_annual_report/<report_id>', methods=['POST'])
@login_required
def update_annual_report(report_id):
    """Handle updating an existing annual report."""
    if current_user.role not in ['faculty', 'admin']:
        return 'Unauthorized', 403
    try:
        if report_id not in annual_reports:
            flash('Report not found', 'error')
            return redirect(url_for('dashboard'))

        report = annual_reports[report_id]
        if report['author'] != current_user.username:
            flash('You can only update your own reports', 'error')
            return redirect(url_for('dashboard'))

        report_data = request.form.get('report_data')
        category = request.form.get('category')
        target = request.form.get('target')
        event_date = request.form.get('event_date')
        from_date = request.form.get('from_date')
        to_date = request.form.get('to_date')
        department = request.form.get('department')
        certificate = request.files.get('certificate')

        # Validate inputs
        if not all([report_data, category, target, department]):
            flash('All fields are required except certificate', 'error')
            return redirect(url_for('dashboard'))

        # Determine event dates
        if event_date:
            from_date = event_date
            to_date = event_date
        elif not (from_date and to_date):
            flash('Please provide valid event dates', 'error')
            return redirect(url_for('dashboard'))

        # Handle certificate update
        certificate_data = report.get('certificate')
        certificate_filename = report.get('certificate_filename')
        if certificate and certificate.filename:
            if certificate.filename.endswith(('.pdf', '.png', '.jpg', '.jpeg')):
                certificate_data = base64.b64encode(certificate.read()).decode('utf-8')
                certificate_filename = certificate.filename
            else:
                flash('Certificate must be PDF, PNG, JPG, or JPEG', 'error')
                return redirect(url_for('dashboard'))

        # Validate the updated report
        validation_result = blockchain.validate_annual_report(
            report_data, category, from_date, to_date, department, current_user.username
        )
        if validation_result != 'valid':
            flash(f'Annual report update failed: {validation_result}', 'error')
            return redirect(url_for('dashboard'))

        block = blockchain.add_annual_report(
            report_id, report_data, category, from_date, to_date, department, 
            current_user.username, target
        )
        annual_reports[report_id] = {
            'data': report_data,
            'category': category,
            'from_date': from_date,
            'to_date': to_date,
            'department': department,
            'author': current_user.username,
            'target': target,
            'timestamp': time.time(),
            'certificate': certificate_data,
            'certificate_filename': certificate_filename,
            'hash': block['hash']
        }
        save_annual_reports(annual_reports)
        audit_log.log_action(
            current_user.username, 
            'update_annual_report', 
            f'Annual report {report_id} updated ({category}) for {target}'
        )
        flash('Annual report updated successfully')
    except Exception as e:
        flash(f'Error updating report: {str(e)}', 'error')
    return redirect(url_for('dashboard'))

@app.route('/download_certificate/<report_id>')
@login_required
def download_certificate(report_id):
    """Download certificate for a report."""
    try:
        if current_user.role not in ['faculty', 'admin', 'student', 'developer']:
            return 'Unauthorized', 403
        report = annual_reports.get(report_id)
        if report and report.get('certificate'):
            certificate_data = base64.b64decode(report['certificate'])
            filename = report.get('certificate_filename', 'certificate.pdf')
            return send_file(
                BytesIO(certificate_data),
                download_name=filename,
                as_attachment=True
            )
        flash('No certificate available', 'error')
    except Exception as e:
        flash(f'Error downloading certificate: {str(e)}', 'error')
    return redirect(url_for('dashboard'))

@app.route('/admin_add_user', methods=['POST'])
@login_required
def admin_add_user():
    """Allow admin to add new users."""
    if current_user.role != 'admin':
        return 'Unauthorized', 403
    try:
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')
        if not all([username, password, role]):
            flash('All fields are required', 'error')
            return redirect(url_for('dashboard'))
        if username in users:
            flash('Username already exists', 'error')
            return redirect(url_for('dashboard'))
        users[username] = {'password': password, 'role': role, 'id': str(uuid.uuid4())}
        save_users(users)
        audit_log.log_action(current_user.username, 'add_user', f'User {username} added with role {role}')
        flash('User added successfully')
    except Exception as e:
        flash(f'Error adding user: {str(e)}', 'error')
    return redirect(url_for('dashboard'))

@app.route('/admin_remove_user', methods=['POST'])
@login_required
def admin_remove_user():
    """Allow admin to remove users."""
    if current_user.role != 'admin':
        return 'Unauthorized', 403
    try:
        username = request.form.get('username')
        if not username:
            flash('Username is required', 'error')
            return redirect(url_for('dashboard'))
        if username not in users:
            flash('User does not exist', 'error')
            return redirect(url_for('dashboard'))
        if username == current_user.username:
            flash('Cannot remove your own account', 'error')
            return redirect(url_for('dashboard'))
        del users[username]
        save_users(users)
        audit_log.log_action(current_user.username, 'remove_user', f'User {username} removed')
        flash('User removed successfully')
    except Exception as e:
        flash(f'Error removing user: {str(e)}', 'error')
    return redirect(url_for('dashboard'))

@app.route('/developer_validate_blockchain', methods=['POST'])
@login_required
def developer_validate_blockchain():
    """Handle developer blockchain attack simulations."""
    if current_user.role != 'developer':
        return 'Unauthorized', 403
    try:
        attack_type = request.form.get('attack_type', 'tampering')
        attack_result = blockchain.simulate_attack(attack_type)
        audit_log.log_action(current_user.username, 'validate_blockchain', f'Blockchain validation performed: {attack_type}')
        try:
            with open(ATTACK_RESULT_FILE, 'w') as f:
                json.dump(attack_result, f, indent=4)
        except IOError as e:
            flash(f'Error saving attack result: {e}', 'error')
        flash(f'Validation result: {attack_result["result"]}')
    except Exception as e:
        flash(f'Error validating blockchain: {str(e)}', 'error')
    return redirect(url_for('dashboard'))

@app.route('/developer_analyze_snapshot', methods=['POST'])
@login_required
def developer_analyze_snapshot():
    """Handle developer blockchain snapshot analysis."""
    if current_user.role != 'developer':
        return 'Unauthorized', 403
    try:
        snapshot_name = request.form.get('snapshot_name', 'Snapshot_' + str(int(time.time())))
        snapshot_result = blockchain.analyze_snapshot(snapshot_name)
        audit_log.log_action(current_user.username, 'analyze_snapshot', f'Snapshot analysis performed: {snapshot_name}')
        try:
            with open(SNAPSHOT_FILE, 'w') as f:
                json.dump(snapshot_result, f, indent=4)
        except IOError as e:
            flash(f'Error saving snapshot result: {e}', 'error')
        flash('Snapshot analysis completed successfully')
    except Exception as e:
        flash(f'Error analyzing snapshot: {str(e)}', 'error')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)