import hashlib
import time
import json
import copy

class Blockchain:
    def __init__(self):
        """Initialize the blockchain with a genesis block."""
        self.chain = []
        self.student_records = []
        self.create_genesis_block()

    def create_genesis_block(self):
        """Create the genesis block for the blockchain."""
        genesis_block = {
            'index': 0,
            'timestamp': time.time(),
            'data': 'Genesis Block',
            'previous_hash': '0',
            'hash': self.calculate_hash(0, time.time(), 'Genesis Block', '0')
        }
        self.chain.append(genesis_block)

    def calculate_hash(self, index, timestamp, data, previous_hash):
        """Calculate the hash of a block."""
        value = f"{index}{timestamp}{data}{previous_hash}"
        return hashlib.sha256(value.encode('utf-8')).hexdigest()

    def get_latest_block(self):
        """Get the latest block in the chain."""
        return self.chain[-1]

    def add_annual_report(self, report_id, report_data, category, from_date, to_date, department, author, target):
        """Add an annual report to the blockchain."""
        block = {
            'index': len(self.chain),
            'timestamp': time.time(),
            'data': {
                'report_id': report_id,
                'report_data': report_data,
                'category': category,
                'from_date': from_date,
                'to_date': to_date,
                'department': department,
                'author': author,
                'target': target
            },
            'previous_hash': self.get_latest_block()['hash']
        }
        block['hash'] = self.calculate_hash(
            block['index'], block['timestamp'], json.dumps(block['data']), block['previous_hash']
        )
        self.chain.append(block)
        return block

    def add_student_record(self, record_data):
        """Add a student record to the blockchain."""
        record = {
            'timestamp': time.time(),
            'data': record_data
        }
        self.student_records.append(record)
        return record

    def get_reports(self):
        """Get all annual reports from the blockchain."""
        reports = []
        for block in self.chain[1:]:  # Skip genesis block
            if 'report_id' in block['data']:
                reports.append(block['data'])
        return reports

    def get_student_records(self):
        """Get all student records."""
        return self.student_records

    def validate_annual_report(self, report_data, category, from_date, to_date, department, author):
        """Validate an annual report before adding it to the blockchain."""
        if not all([report_data, category, from_date, to_date, department, author]):
            return "Missing required fields"
        if category not in ['Seminar', 'Workshop', 'Project', 'Internship', 'Hackathon', 'Paper Publishing']:
            return "Invalid category"
        try:
            # Validate date format (assuming YYYY-MM-DD)
            time.strptime(from_date, '%Y-%m-%d')
            time.strptime(to_date, '%Y-%m-%d')
            if from_date > to_date:
                return "From date cannot be after to date"
        except ValueError:
            return "Invalid date format"
        return "valid"

    def validate_chain(self):
        """Validate the integrity of the blockchain."""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # Verify current block's hash
            if current_block['hash'] != self.calculate_hash(
                current_block['index'], 
                current_block['timestamp'], 
                json.dumps(current_block['data']), 
                current_block['previous_hash']
            ):
                return {'valid': False, 'error': f'Hash mismatch at block {i}'}

            # Verify previous hash
            if current_block['previous_hash'] != previous_block['hash']:
                return {'valid': False, 'error': f'Previous hash mismatch at block {i}'}

        return {'valid': True, 'error': None}

    def simulate_attack(self, attack_type):
        """Simulate different types of attacks on the blockchain and validate."""
        # Create a deep copy of the chain to simulate the attack without affecting the original chain
        original_chain = copy.deepcopy(self.chain)
        result = {'attack_type': attack_type, 'result': ''}

        if attack_type == 'tampering':
            # Simulate tampering by modifying data in a block
            if len(self.chain) > 1:
                self.chain[1]['data']['report_data'] = "Tampered Data"
                self.chain[1]['hash'] = self.calculate_hash(
                    self.chain[1]['index'], 
                    self.chain[1]['timestamp'], 
                    json.dumps(self.chain[1]['data']), 
                    self.chain[1]['previous_hash']
                )
                validation = self.validate_chain()
                result['result'] = f"Tampering detected: {validation['error']}" if not validation['valid'] else "Tampering not detected"
            else:
                result['result'] = "Not enough blocks to tamper"

        elif attack_type == 'double_submission':
            # Simulate double submission by adding the same report twice
            if len(self.chain) > 1:
                block = copy.deepcopy(self.chain[-1])
                block['timestamp'] = time.time()
                block['previous_hash'] = self.get_latest_block()['hash']
                block['hash'] = self.calculate_hash(
                    block['index'], block['timestamp'], json.dumps(block['data']), block['previous_hash']
                )
                self.chain.append(block)
                # Check for duplicate report IDs
                report_ids = [block['data']['report_id'] for block in self.chain[1:] if 'report_id' in block['data']]
                duplicates = len(report_ids) != len(set(report_ids))
                validation = self.validate_chain()
                if duplicates:
                    result['result'] = "Double submission detected: Duplicate report ID found"
                elif not validation['valid']:
                    result['result'] = f"Chain validation failed: {validation['error']}"
                else:
                    result['result'] = "Double submission not detected (but chain is valid)"
            else:
                result['result'] = "Not enough blocks for double submission"

        elif attack_type == 'invalid_hash':
            # Simulate invalid hash injection by modifying a block's hash
            if len(self.chain) > 1:
                self.chain[1]['hash'] = "invalid_hash_value"
                validation = self.validate_chain()
                result['result'] = f"Invalid hash detected: {validation['error']}" if not validation['valid'] else "Invalid hash not detected"
            else:
                result['result'] = "Not enough blocks to inject invalid hash"

        # Restore the original chain
        self.chain = original_chain
        return result

    def get_quality_metrics(self):
        """Get quality metrics of the blockchain."""
        return {
            'chain_length': len(self.chain),
            'last_block_time': self.get_latest_block()['timestamp']
        }

    def analyze_snapshot(self, snapshot_name):
        """Analyze a snapshot of the blockchain."""
        validation = self.validate_chain()
        return {
            'snapshot_name': snapshot_name,
            'timestamp': time.time(),
            'chain_length': len(self.chain),
            'reports_count': len(self.get_reports()),
            'validation': validation
        }