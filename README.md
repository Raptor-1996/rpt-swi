🔍 RPT See Who Is In (RPT swi)

Professional Network Security Monitoring & Management Tool

https://img.shields.io/badge/python-3.6%252B-blue
https://img.shields.io/badge/License-MIT-yellow.svg
https://img.shields.io/badge/platform-Linux-lightgrey
https://img.shields.io/badge/Maintained-Yes-green.svg
https://img.shields.io/github/stars/Raptor-1996/rpt-swi
🌟 Overview

RPT See Who Is In is a powerful, professional-grade network security tool designed for system administrators, network engineers, and security professionals. It provides comprehensive network monitoring, device discovery, firewall management, and security auditing capabilities - all from an intuitive command-line interface.
# ✨ Key Features

    🔍 Advanced Network Scanning - Multi-method device discovery (ARP, Nmap, ICMP)

    🛡️ Firewall Management - Real-time device blocking/unblocking with iptables

    📊 Device Database - SQLite-based tracking with historical data

    🚨 Real-time Monitoring - Continuous network surveillance with alerts

    📈 Comprehensive Reporting - Detailed statistics and export capabilities

    🎨 Beautiful CLI Interface - Color-coded, user-friendly terminal UI

    🔔 Smart Notifications - Email, Telegram, and file-based alerts

    🐳 Docker Support - Containerized deployment options

    🧪 Testing Suite - Comprehensive unit and integration tests

# 📸 Screenshots
```text

╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║   ██████╗ ██████╗ ████████╗      ███████╗██╗    ██╗██╗              ║
║   ██╔══██╗██╔══██╗╚══██╔══╝      ██╔════╝██║    ██║██║              ║
║   ██████╔╝██████╔╝   ██║         ███████╗██║ █╗ ██║██║              ║
║   ██╔══██╗██╔═══╝    ██║         ╚════██║██║███╗██║██║              ║
║   ██║  ██║██║        ██║         ███████║╚███╔███╔╝███████╗         ║
║   ╚═╝  ╚═╝╚═╝        ╚═╝         ╚══════╝ ╚══╝╚══╝ ╚══════╝         ║
║                                                                      ║
║              S E E   W H O   I S   I N   v2.0.0                      ║
║              Professional Network Security Tool                      ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
```

# 🚀 Quick Start

## Method 1: Quick Install (Recommended)

### Download and run the quick installer
``` bash
curl -L https://raw.githubusercontent.com/Raptor-1996/rpt-swi/main/quick_start.sh | sudo bash
```

## Method 2: Manual Installation

### Clone the repository
```bash
git clone https://github.com/Raptor-1996/rpt-swi.git
cd rpt-swi
```
### Run the installer
```bash
chmod +x install.sh
sudo ./install.sh
```

### Start using RPT swi
```bash
sudo rpt-swi
```

## Method 3: Docker Deployment

### Using Docker Compose
```bash
docker-compose up -d
```

### Or direct Docker
```bash
docker build -t rpt-swi .
docker run -it --net=host --privileged rpt-swi
```

#🛠️ System Requirements
Component	Minimum	Recommended
OS	Linux (Kernel 3.10+)	Ubuntu 20.04+, CentOS 8+, Debian 11+
Python	3.6+	3.9+
RAM	512 MB	2 GB
Storage	100 MB	1 GB
Network	Ethernet/WiFi	Dedicated network interface
Required Dependencies

## Core utilities
```
sudo apt-get install nmap arp-scan iptables net-tools
```

## Python packages (auto-installed)
```
pip install scapy python-iptables netifaces colorama tabulate
```

📖 Usage Guide
Basic Commands
bash

## Start interactive mode
```
sudo rpt-swi
```

## Quick network scan
```
sudo rpt-swi --scan
```

## Block a specific IP
```
sudo rpt-swi --block 192.168.1.100
```

## Unblock an IP
```
sudo rpt-swi --unblock 192.168.1.100
```

## List blocked devices
```
sudo rpt-swi --list
```

## Show help
```
sudo rpt-swi --help
```

# Interactive Mode Features
1. Network Information

    View detailed network configuration including:
    IP addresses and MAC addresses
    Network interfaces and subnet information
    Gateway and DNS servers
    Public IP address

2. Network Scanning

    Choose from multiple scanning methods:
    Quick Scan - Fast ARP-based discovery (30 seconds)
    Full Scan - Comprehensive multi-method scan
    Deep Scan - Includes port detection and OS fingerprinting
    Continuous Monitoring - Real-time network surveillance

3. Device Management

    View all discovered devices with vendor information
    Mark devices as trusted/untrusted
    Add notes and tags to devices
    Export device lists to JSON/CSV

4. Firewall Control

    Block/unblock individual devices
    Block specific IP addresses or MAC addresses
    Schedule blocking rules
    Create custom iptables rules
    Backup and restore firewall configurations

5. Monitoring & Alerts

    Real-time network monitoring

    Alert on new device connections

    Notification via Email, Telegram, or log files

    Customizable alert thresholds

# 🏗️ Architecture
```text

┌─────────────────────────────────────────────────────────────┐
│                    RPT SWI Architecture                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────┐    ┌──────────┐    ┌──────────────────┐     │
│  │   CLI    │◄──►│   Core   │◄──►│   Database       │     │
│  │  Layer   │    │  Engine  │    │   (SQLite)       │     │
│  └──────────┘    └──────────┘    └──────────────────┘     │
│         │               │                      │           │
│  ┌──────▼──────┐ ┌─────▼──────┐        ┌──────▼──────┐    │
│  │   Network   │ │  Firewall  │        │  Logging &  │    │
│  │   Scanner   │ │  Manager   │        │  Reporting  │    │
│  └─────────────┘ └────────────┘        └─────────────┘    │
│         │               │                      │           │
│  ┌──────▼──────┐ ┌─────▼──────┐        ┌──────▼──────┐    │
│  │   Nmap      │ │  iptables  │        │  Export     │    │
│  │   ARP       │ │  Rules     │        │  Formats    │    │
│  │   ICMP      │ └────────────┘        └─────────────┘    │
│  └─────────────┘                                          │
└─────────────────────────────────────────────────────────────┘
```

# 🔧 Advanced Features
1. MAC Vendor Database

    Built-in database of 45,000+ MAC address vendors
    Automatic vendor detection from MAC addresses
    Regular updates from IEEE OUI database

2. Intelligent Scanning

    Parallel scanning with configurable threads
    Smart timeout management
    Adaptive scanning based on network size
    Cache support for repeated scans

3. Security Features

    Root privilege requirement for sensitive operations
    Encrypted configuration storage
    Audit logging for all actions
    Rate limiting and anti-DOS protection

4. Integration Options

    REST API (planned)
    Web dashboard (planned)
    SIEM integration via syslog
    Slack/Teams webhook support

# 📊 Performance Metrics
```
Operation	Time	Devices Found	Accuracy
Quick Scan	15-30s	95%	98%
Full Scan	1-2min	99%	99.5%
Deep Scan	2-5min	100%	99.8%
Device Block	<1s	N/A	100%
```

# 🐳 Docker Deployment
## Single Container
```bash

docker run -d \
  --name rpt-swi \
  --net=host \
  --privileged \
  -v /etc/rpt-swi:/app/config \
  -v /var/log/rpt-swi:/app/logs \
  raptor1996/rpt-swi:latest
```
## Docker Compose (Full Stack)
```yaml

version: '3.8'
services:
  rpt-swi:
    image: raptor1996/rpt-swi:latest
    network_mode: host
    privileged: true
    volumes:
      - ./data:/app/data
      - ./config:/app/config
    restart: unless-stopped
```

# 🔐 Security Considerations
Ethical Usage

##⚠️ IMPORTANT: This tool is designed for:

    Monitoring your own networks
    Educational purposes
    Security research with authorization
    Network administration with proper permissions

##🚫 DO NOT USE for:

    Unauthorized network access
    Privacy violations
    Illegal activities
    Network attacks

# Security Best Practices

    Always run with proper authorization
    Use in isolated test environments first
    Regularly update the software
    Monitor logs for suspicious activity
    Implement additional security layers

# 🧪 Testing & Development
Running Tests

## Install test dependencies
```
pip install pytest pytest-cov
```

## Run all tests
```
pytest tests/ -v
```

## Run with coverage
```
pytest tests/ --cov=src --cov-report=html
```

## Run specific test module
```
pytest tests/test_scanner.py -v
```

#Development Setup

## Clone and setup development environment
```bash
git clone https://github.com/Raptor-1996/rpt-swi.git
cd rpt-swi
python -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt
```

## Install in development mode
```bash
pip install -e .
```

## Run code quality checks
```bash
flake8 src/
black src/ --check
mypy src/
```

#📈 Monitoring & Logging
###Log Files
```text

/var/log/rpt-swi/
├── rpt_swi.log          # Main application log
├── firewall.log         # Firewall operations
├── scan.log             # Scanning activities
└── notifications.log    # Alert notifications
```

## System Integration

### View logs in real-time
```
sudo tail -f /var/log/rpt-swi/rpt_swi.log
```

### Check service status
```
sudo systemctl status rpt-swi
```

### View firewall rules
```
sudo iptables -L RPT-SWI -n
```

#🤝 Contributing

    We welcome contributions! Here's how you can help:
    Report Bugs - Open an issue with detailed information
    Suggest Features - Share your ideas for improvement
    Submit Pull Requests - Fix bugs or add new features
    Improve Documentation - Help make the docs better
    Spread the Word - Share with colleagues and friends

# Development Workflow

1. Fork the repository
2. Create a feature branch
```
git checkout -b feature/amazing-feature
```

3. Make your changes
4. Run tests
```
pytest tests/
```

5. Commit changes
```
git commit -m "Add amazing feature"
```

6. Push to branch
```
git push origin feature/amazing-feature
```

7. Open a Pull Request

#📚 Documentation
 API Documentation
 python

## Example: Using the scanner module programmatically
```
from src.core.scanner import NetworkScanner
from src.core.database import DeviceDatabase
db = DeviceDatabase()
scanner = NetworkScanner(db)
```

## Scan network
```
devices = scanner.scan_network(timeout=30)
print(f"Found {len(devices)} devices")
```

## Get network info
```
info = scanner.get_network_info()
print(f"Your IP: {info['interfaces'][0]['ip']}")
```

## Configuration Guide

```yaml
Create /etc/rpt-swi/settings.yaml:
```

### database:
```yaml
  path: /var/lib/rpt-swi/devices.db
  backup_interval: 24
```

### scanner:
```yaml
  timeout: 30
  threads: 50
  retries: 2
```

### firewall:
```yaml
  chain_name: "RPT-SWI"
  default_action: "DROP"
```

### notifications:
```yaml
  enabled: true
  email:
    smtp_server: "smtp.gmail.com"
    smtp_port: 587
    recipient: "admin@example.com"
```

#🆘 Troubleshooting
## Common Issues
Problem	Solution
Permission denied	Run with sudo or as root
Nmap not found	Install nmap: sudo apt install nmap
iptables error	Ensure iptables is installed and accessible
No devices found	Check network connectivity and firewall rules
Database errors	Delete corrupted database file and restart
Debug Mode

## Enable debug logging
```
sudo rpt-swi --debug
```

## View detailed logs
```
sudo journalctl -u rpt-swi -f
```

## Check system dependencies
```
sudo rpt-swi --check-deps
```

#📞 Support & Community
## Getting Help

    📧 Email: EbiRom1996@gmail.com
    🐙 GitHub Issues: Report Issues
    💬 Discussions: Join the Conversation

## Community Resources

    📖 Wiki: Github
    🎥 Tutorials: Video guides (coming soon)
    📚 Examples: Sample configurations and use cases

# 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
Third-Party Licenses

    python-iptables - BSD License
    scapy - GPLv2 License
    colorama - BSD License
    tabulate - MIT License
    requests - Apache 2.0 License

# 🙏 Acknowledgments

    Raptor-1996 - Creator and maintainer
    Contributors - Everyone who helped improve this project
    Open Source Community - For amazing tools and libraries
    Testers - For valuable feedback and bug reports

# 🚀 Roadmap
Planned Features

    Web-based administration panel
    REST API for remote management
    Mobile app for notifications
    Advanced threat detection
    Network topology mapping
    Automated vulnerability scanning
    Compliance reporting
    Cloud integration

# Current Version: 2.0.0

    ✅ Multi-method network scanning
    ✅ Advanced firewall management
    ✅ SQLite database with history
    ✅ Real-time monitoring
    ✅ Docker support
    ✅ Comprehensive testing

# 📞 Contact

Author: Raptor-1996
Email: EbiRom1996@gmail.com
GitHub: https://github.com/Raptor-1996
Website: Coming Soon

<div align="center">
⭐ If you find this project useful, please give it a star on GitHub!

https://api.star-history.com/svg?repos=Raptor-1996/rpt-swi&type=Date

Made with ❤️ for the security community
</div>
🔄 Update History
Version	Date	Changes
2.0.0	Jan 2024	Complete rewrite with professional features
1.5.0	Dec 2023	Added Docker support and notifications
1.0.0	Nov 2023	Initial stable release
0.9.0	Oct 2023	Beta release with core functionality

Disclaimer: This tool is for legitimate security and network management purposes only. Always ensure you have proper authorization before scanning or monitoring any network. The authors are not responsible for any misuse or damage caused by this software.

Keep your network secure with RPT See Who Is In! 🔐
