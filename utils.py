class SmartContract:
    def validate_annual_report(self, report_data, category, report_type, from_date, to_date, department, author):
        """Validate an annual report."""
        if not report_data or len(report_data.strip()) < 10:
            return "Report data is too short or empty"
        if category not in ['Seminar', 'Workshop', 'Project', 'Internship', 'Hackathon', 'Paper Publishing']:
            return "Invalid category"
        if report_type not in ['Summary']:
            return "Invalid report type"
        if not department or len(department.strip()) < 2:
            return "Invalid department"
        if not author:
            return "Author is required"
        if not from_date or not to_date:
            return "Event dates are required"
        return "valid"