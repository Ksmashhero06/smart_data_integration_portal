import json
import os
import hashlib
import time
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ANNUAL_REPORT_FILE = os.path.join(BASE_DIR, 'annual_reports.json')
BLOCKCHAIN_FILE = os.path.join(BASE_DIR, 'blockchain.json')

def calculate_hash(block):
    """Calculate SHA-256 hash of a block."""
    block_string = json.dumps(block, sort_keys=True)
    return hashlib.sha256(block_string.encode()).hexdigest()

# Load annual reports
try:
    with open(ANNUAL_REPORT_FILE, 'r') as f:
        annual_reports = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    print("Error: annual_reports.json not found or invalid.")
    exit(1)

# Initialize blockchain with genesis block
chain = [{
    'index': 0,
    'timestamp': time.time(),
    'data': 'Genesis Block',
    'previous_hash': '0',
    'target': 'None',
    'target_username': 'None',
    'hash': None
}]
chain[0]['hash'] = calculate_hash(chain[0])

# Rebuild blockchain from annual reports
for report_id, report in annual_reports.items():
    block = {
        'index': len(chain),
        'timestamp': report['timestamp'],
        'report_id': report_id,
        'data': report['data'],
        'category': report['category'],
        'report_type': report['report_type'],
        'from_date': report['from_date'],
        'to_date': report['to_date'],
        'department': report['department'],
        'author': report['author'],
        'target': report['target'],
        'target_username': report['target_username'],
        'previous_hash': chain[-1]['hash']
    }
    block['hash'] = calculate_hash(block)
    chain.append(block)
    report['hash'] = block['hash']  # Update the report with the hash

# Save updated blockchain
try:
    with open(BLOCKCHAIN_FILE, 'w') as f:
        json.dump(chain, f, indent=4)
except IOError as e:
    print(f"Error saving blockchain.json: {e}")
    exit(1)

# Save updated annual reports
try:
    with open(ANNUAL_REPORT_FILE, 'w') as f:
        json.dump(annual_reports, f, indent=4)
except IOError as e:
    print(f"Error saving annual_reports.json: {e}")
    exit(1)

print("Successfully rebuilt blockchain.json and updated annual_reports.json with hashes")
print(f"New chain length: {len(chain)}")