<!-- Smart Data Integration Portal -->
## Abstract 
The Smart Data Integration Portal leverages a blockchain architecture to ensure secure, verifiable, and tamper-proof data submission and validation for institutional annual reports. Smart contracts automate the verification and validation of reports, enforcing submission guidelines such as report length (10–500 characters), content rules (letters required, no forbidden keywords: “malicious”, “hack”, “exploit”), and category constraints (Seminar, Workshop, Project, Internship, Hackathon), enhancing transparency and operational efficiency. The system features a user-friendly Flask-based frontend with a blue-grey theme (navy blue #1E3A8A, light grey #D1D5DB, dark grey #4B5563, white #FFFFFF), incorporating modals, sortable tables, and toast notifications for seamless data submission, report tracking, and certificate downloads. A robust backend ensures secure data management, while role-based access control (RBAC) restricts access to authorized users (Student, Faculty, Admin, Developer). Immutable audit trails maintain accountability and traceability, streamlining institutional reporting with accuracy and trust.

## Introduction
The Smart Data Integration Portal is a Flask-based web application designed to automate and secure the process of collecting, validating, and managing institutional annual reports using blockchain technology. The system employs a blockchain architecture with SHA-256 hashing to ensure data integrity, transparency, and tamper-proof storage, addressing challenges in traditional report management systems. Smart contracts automate report verification, enforcing rules on report length, content, and categories (Seminar, Workshop, Project, Internship, Hackathon). Faculty can submit detailed annual reports with fields including report type (Summary/Evaluation), category, event dates, department (e.g., CS, EE, ME), and an optional certificate description, displayed in sortable tables with download links. The frontend, styled with a blue-grey theme, features modals for submission, toast notifications for feedback, and sortable tables for tracking. A secure backend facilitates seamless data submission, review, and report generation, while role-based access control (using Flask-Login) and immutable audit trails enhance security and accountability.

## Existing System
Manual report submission and review systems are prone to errors, delays, and tampering, often requiring extensive manual validation that slows down institutional workflows. Traditional database systems for report management rely on centralized storage, making them vulnerable to unauthorized modifications and lacking robust validation mechanisms. File-based storage systems with version control fail to provide automatic data validation and struggle with maintaining version consistency across submissions. Cloud-based report portals, while convenient, do not guarantee data integrity and are susceptible to insider threats, often lacking transparency in data handling. Digital report management platforms with basic security measures offer limited auditability, no traceability of records, and fail to enforce structured submission guidelines, leading to inconsistencies in report quality and compliance.

## Proposed System
The proposed system utilizes a blockchain architecture with SHA-256 hashing to ensure secure, verifiable, and tamper-proof report management for institutional annual reports, deployed locally at D:\portfolio\smart_data_integration_portal on Windows and to Render via GitHub. Role-based access control (RBAC) restricts access to authorized users (Student, Faculty, Admin, Developer), ensuring secure data handling. Smart contracts automate data validation, enforcing submission guidelines such as report length (10–500 characters), content rules (e.g., presence of letters, no forbidden keywords), category validation (Seminar, Workshop, Project, Internship, Hackathon), and limits (max 5 reports per user, updates differ by 10%). Faculty can submit detailed annual reports with fields like report type, category, event dates, department, and optional certificate descriptions, stored in the blockchain and annual_reports.json, displayed in sortable tables with downloadable certificates. Immutable audit trails, stored in audit_logs.json, maintain a transparent and traceable record of all actions. The system integrates a seamless Flask-based frontend with a blue-grey theme and a robust backend, enabling efficient data submission, report generation, and tracking, while ensuring compliance and trust through blockchain technology.

## Features

<!-- User Roles: -->
Student: View blockchain records in sortable tables.
Faculty: Submit and update annual reports (categories: Seminar, Workshop, Project, Internship, Hackathon) with fields including report type (Summary/Evaluation), event dates, department (CS, EE, ME), and optional certificate description, using modal dialogs with smart contract validation.
Admin: Manage users via interactive modal dialogs, view and sort audit logs with toggleable sections.
Developer: Validate blockchain integrity, simulate attacks (tampering, hash collision, double-spending), analyze blockchain snapshots (chain growth, report diversity, vulnerabilities), and view quality metrics.


Blockchain: SHA-256-based chain for secure report storage, ensuring data integrity.
Smart Contracts: Automate report validation (10–500 characters, letters required, no forbidden keywords: “malicious”, “hack”, “exploit”) and enforce submission limits (max 5 per user, updates differ by 10%), including category validation for annual reports.

UI Enhancements: 
Blue-grey theme (navy blue #1E3A8A, light grey #D1D5DB, dark grey #4B5563, white #FFFFFF), modal dialogs for form submissions, toast notifications for feedback, sortable tables for records/logs/reports, progress indicators for simulations/snapshots, and real-time form validation.

Snapshot Analysis: Developers can create blockchain snapshots to analyze chain growth, report diversity, and potential vulnerabilities, stored in snapshots.json.

Annual Reports: Faculty submit annual reports with category validation, stored in the blockchain and annual_reports.json, displayed in sortable tables with filters and certificate download links.
Persistence: Users, audit logs, attack results, snapshots, and annual reports stored in JSON files (users.json, audit_logs.json, attack_results.json, snapshots.json, annual_reports.json) in the root directory locally, mapped to /app on Render.

Security: User authentication with Flask-Login, audit logging for all actions in audit_logs.json.

<!-- ## Modules -->

## User Interface (Frontend) Module: 
Implemented in Flask templates with a modern, responsive design using Bootstrap/Tailwind CSS and DataTables.js. The interface features a collapsible sidebar navigation with icons for Dashboard, Reports, Profile, and Settings, replacing traditional top navigation links. Reports are displayed in a card-based layout with clear sections (Timestamp, Category, Department) and icon-based actions (download 📥, edit ✏️). Each card uses white backgrounds with soft shadows against a modern color palette of soft blues and greys, with data fields truncated via "View More" expandable modals to reduce visual clutter. 

Key UI/UX features include:
- Sticky department and category filters that remain visible during scrolling
- Primary action buttons (e.g., "Submit New Report") with solid colors and rounded corners
- Compact table headers with intuitive icons (🕒 timestamp, 🏷️ category)
- Interactive row styling (hover highlights, zebra stripes) for improved readability
- Integrated search functionality for filtering by name/event/category
- Toast notifications for user feedback on actions
- Responsive design that transforms card layouts and navigation for mobile devices
- Real-time form validation and modal-based editing workflows

The system maintains role-based access, enabling Students to view blockchain records, Faculty to submit annual reports (with fields for report type, category, dates, department, and certificates), Admins to manage users, and Developers to analyze blockchain snapshots.

## Backend & Smart Contract Module: 
Managed by app.py, blockchain.py, and utils.py, this module handles user requests, processes reports, and interfaces with the blockchain for secure storage. It validates reports using smart contracts (implemented in blockchain.py) before storage, enforcing rules on length, content, and categories. Uses Flask 2.0.1, Flask-Login 0.5.0, and Werkzeug 2.0.3 for backend logic, with data persistence in JSON files (users.json, annual_reports.json, snapshots.json, attack_results.json). Smart contracts ensure reports meet guidelines (e.g., max 5 per user, updates differ by 10%).

## Blockchain & Validation Layer: 
Implemented in blockchain.py, this module ensures security and prevents unauthorized modifications by storing report metadata (hash, timestamp, category) in a blockchain using SHA-256 hashing. Reports and annual reports are validated via smart contracts, ensuring compliance with submission rules. Data is persisted in annual_reports.json for annual reports and other JSON files for additional records, balancing security and simplicity while maintaining verifiability through the blockchain.

## Audit & Logging Module:
 Managed by audit_log.py, this module tracks all user actions (e.g., report submissions, user management, blockchain validation) to ensure accountability and transparency. It logs actions to audit_logs.json in a structured format, capturing details like user ID, action, and timestamp. RBAC is implemented using Flask-Login, ensuring only authorized users (Student, Faculty, Admin, Developer) can perform actions, aligning with role-based security requirements.

<!-- Prerequisites -->

Python 3.9+
Git
Render account (for cloud deployment)
GitHub account

<!-- Project Structure -->

smart_data_integration_portal/
├── app.py                  # Main Flask application
├── blockchain.py           # Blockchain and smart contract logic
├── audit_log.py            # Audit log management
├── utils.py                # Utility functions (e.g., hashing)
├── templates/              # HTML templates for dashboards
│   ├── base.html
│   ├── login.html
│   ├── dashboard_student.html
│   ├── dashboard_faculty.html
│   ├── dashboard_admin.html
│   └── dashboard_developer.html
├── static/                 # CSS and JS files
│   ├── css/
│   │   └── styles.css
│   └── js/
│       └── scripts.js
├── requirements.txt        # Python dependencies
├── users.json              # User data storage
├── annual_reports.json     # Annual report storage
├── audit_logs.json         # Audit log storage
├── attack_results.json     # Attack simulation results
├── snapshots.json          # Blockchain snapshot data
└── README.md               # Project documentation

<!-- Setup Instructions -->

## Local Setup

## Clone the Repository:
git clone https://github.com/your-username/smart_data_integration_portal.git
cd smart_data_integration_portal


## Create Virtual Environment:
python -m venv venv
.\venv\Scripts\activate


## Install Dependencies:
pip install -r requirements.txt


## Set Up Environment:
Ensure app.py is configured to run on http://localhost:5000.
Create necessary JSON files in the root directory (mapped to /app on Render): users.json, audit_logs.json, attack_results.json, snapshots.json, annual_reports.json.


## Run the Application:
python app.py


Access at http://localhost:5000.



## Deployment to Render

Push to GitHub:
Create a repository on GitHub (smart_data_integration_portal).
Push your local project:git remote add origin https://github.com/your-username/smart_data_integration_portal.git
git branch -M main
git push -u origin main




## Set Up Render:
Sign up at https://render.com and connect your GitHub account.
Create a Web Service, select your repository, and configure:
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: gunicorn -w 4 -b 0.0.0.0:5000 app:app
Disk: Name: data, Mount Path: /app, Size: 1 GB


Deploy and access the provided URL (e.g., https://smart-data-integration-portal.onrender.com).


### Verify Persistence:
Ensure users.json, audit_logs.json, attack_results.json, snapshots.json, and annual_reports.json are stored in /app.



<!--  Usage -->

## Default Users:
Student: student1 / pass123
Faculty: faculty1 / pass456
Admin: admin1 / pass789
Developer: developer1 / pass101


## Key Actions:
Student: Log in to view blockchain records in sortable tables on the Student dashboard.
Faculty: Log in to submit annual reports via modals (e.g., Seminar report with event dates and certificate), minimum 2 reports required for Developer simulations.
Admin: Log in to add/remove users via modal dialogs, persisted in users.json, and view audit logs with sortable tables.
Developer: Log in to run attack simulations (tampering, hash collision, double-spending) or snapshot analysis after Faculty adds blocks.


## Enable Attack Simulations and Snapshot Analysis:
Log in as faculty1, submit 2–3 annual reports (e.g., “Seminar on AI 2025” with category Seminar).
Log in as developer1, run simulations or analyze a snapshot to view metrics like chain growth.



## Troubleshooting

Files Not Persisting:
Verify disk configuration in Render.
Check file permissions in /app.


Attack Simulations or Snapshot Analysis Fail:
Submit reports as faculty1 to add blocks.
Ensure blockchain.py returns dictionaries in simulate_attack and analyze_snapshot.


UI Issues:
Clear browser cache.
Check browser console for JavaScript errors.



## Contributing

Fork the repository.
Create a feature branch (git checkout -b feature-name).
Commit changes (git commit -m "Add feature").
Push to the branch (git push origin feature-name).
Open a Pull Request.


## References

Wang, X., Li, Y., & Zhang, Z. (2023). Blockchain-based Data Integrity Verification for Secure Applications. IEEE Transactions on Industrial Informatics.
Sharma, A., & Jain, P. K. (2022). Role Based Access Control with Blockchain for Secured Data Sharing. International Journal of Information Security.
Patel, S., Shah, K., & Thakkar, R. (2020). Hybrid Blockchain for Secure and Scalable Data Management. Journal of Blockchain Technology.
Chen, J., Xu, L., & Zhang, Q. (2020). Blockchain-Based Audit Transparent Data Management. IEEE Access.
Kim, L. J. (2019). Smart Data Integration for Universities. MIT – AR2019-003.

