import json
import os
import time
from datetime import datetime

class AuditLog:
    def __init__(self):
        self.logs = []
        self.log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'audit_logs.json')
        self.load_logs()

    def load_logs(self):
        """Load audit logs from audit_logs.json."""
        if os.path.exists(self.log_file):
            try:
                with open(self.log_file, 'r') as f:
                    self.logs = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.logs = []
        else:
            self.logs = []

    def save_logs(self):
        """Save audit logs to audit_logs.json."""
        try:
            with open(self.log_file, 'w') as f:
                json.dump(self.logs, f, indent=4)
        except IOError as e:
            print(f"Error saving audit logs: {e}")

    def log_action(self, user, action, details):
        """Log an action with timestamp."""
        log_entry = {
            'timestamp': time.time(),
            'user': user,
            'action': action,
            'details': details
        }
        self.logs.append(log_entry)
        self.save_logs()

    def get_logs(self):
        """Get all audit logs."""
        return self.logs