# Developer Documentation

## Project Structure

rpt-swi/
├── src/ # Source code
│ ├── main.py # Main entry point
│ ├── core/ # Core modules
│ │ ├── scanner.py # Network scanner
│ │ ├── firewall.py # Firewall manager
│ │ ├── database.py # Database manager
│ │ └── notifications.py # Notification system
│ ├── ui/ # User interface
│ │ ├── cli.py # CLI interface
│ │ ├── colors.py # Color management
│ │ └── progress.py # Progress bars
│ ├── utils/ # Utilities
│ │ ├── helpers.py # Helper functions
│ │ ├── validators.py # Input validation
│ │ └── mac_vendors.py # MAC vendor database
│ └── config/ # Configuration
│ ├── settings.py # Settings manager
│ └── constants.py # Constants
├── tests/ # Test suite
├── docs/ # Documentation
├── config/ # Configuration files
├── data/ # Data files
├── scripts/ # Utility scripts
└── examples/ # Usage examples
text


## Architecture
The application follows a modular architecture:

1. **Core Layer**: Handles network scanning, firewall management, and data storage
2. **UI Layer**: Provides command-line interface with colors and progress indicators
3. **Utility Layer**: Helper functions and validation
4. **Config Layer**: Manages settings and constants

## Adding New Features

### 1. Adding a new scanner module
```python
# In src/core/scanner.py
class NewScannerMethod:
    def scan(self, network):
        # Implementation
        pass

2. Adding a new command-line option
python

# In src/main.py, add to parse_arguments()
parser.add_argument('--new-option', help='Description')

3. Adding database tables
python

# In src/core/database.py
def _init_database(self):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS new_table (
            id INTEGER PRIMARY KEY,
            -- columns
        )
    ''')

Testing
bash

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test
pytest tests/test_scanner.py::TestNetworkScanner -v

Code Style

    Follow PEP 8 guidelines

    Use type hints for function signatures

    Document all public functions and classes

    Write unit tests for new features

Contributing

    Fork the repository

    Create a feature branch

    Make your changes

    Write tests

    Submit a pull request

Contact

For development questions, contact:

    Email: EbiRom1996@gmail.com

    GitHub: @Raptor-1996
    EOF

cat > docs/API.md << 'EOF'
API Documentation
Core Modules
Scanner Module
python

from src.core.scanner import NetworkScanner
from src.core.database import DeviceDatabase

# Initialize
db = DeviceDatabase()
scanner = NetworkScanner(db)

# Scan network
devices, my_info = scanner.scan_network(
    scan_type="quick",  # quick, arp, full
    interface="eth0"
)

# Get network info
info = scanner.get_my_network_info()

Firewall Module
python

from src.core.firewall import FirewallManager

# Initialize
firewall = FirewallManager(db)

# Block a device
firewall.block_device(
    ip_address="192.168.1.100",
    mac_address="00:11:22:33:44:55",
    comment="Suspicious device"
)

# Unblock a device
firewall.unblock_device("192.168.1.100")

# Get status
status = firewall.get_firewall_status()

Database Module
python

from src.core.database import DeviceDatabase

# Initialize
db = DeviceDatabase()

# Add/update device
db.add_device({
    'ip': '192.168.1.100',
    'mac': '00:11:22:33:44:55',
    'hostname': 'device.local',
    'vendor': 'Manufacturer'
})

# Get devices
devices = db.get_devices(
    status='online',  # Filter by status
    trusted=True      # Filter by trusted status
)

# Log events
db.log_event(
    event_type='scan_complete',
    event_source='scanner',
    event_data='{"devices_found": 10}',
    severity='info'
)

Command Line Interface
Programmatic Usage
python

import subprocess
import json

# Run scan
result = subprocess.run(
    ['rpt-swi', '--scan', '--output', 'scan.json'],
    capture_output=True,
    text=True
)

# Parse output
with open('scan.json', 'r') as f:
    data = json.load(f)

Integration Example
python

#!/usr/bin/env python3
"""
Example: Integrating RPT SWI with other systems
"""

import json
import subprocess
from datetime import datetime

class NetworkMonitor:
    def __init__(self):
        self.scan_results = []
    
    def scan_and_alert(self):
        """Perform scan and check for new devices"""
        # Run scan
        cmd = ['sudo', 'rpt-swi', '--scan', '--format', 'json']
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            
            # Check for new devices
            new_devices = self._find_new_devices(data['devices'])
            
            if new_devices:
                self._send_alert(new_devices)
            
            return data
        return None
    
    def _find_new_devices(self, devices):
        """Compare with previous scan"""
        current_ips = {d['ip'] for d in devices}
        previous_ips = set(self.scan_results[-1] if self.scan_results else [])
        
        new_ips = current_ips - previous_ips
        return [d for d in devices if d['ip'] in new_ips]
    
    def _send_alert(self, devices):
        """Send alert about new devices"""
        message = f"New devices detected: {len(devices)}"
        for device in devices:
            message += f"\n- {device['ip']} ({device.get('vendor', 'Unknown')})"
        
        print(f"ALERT: {message}")
        # Here you could send email, SMS, webhook, etc.

# Usage
if __name__ == "__main__":
    monitor = NetworkMonitor()
    results = monitor.scan_and_alert()
    
    if results:
        print(f"Scan completed: {results['devices_found']} devices found")
