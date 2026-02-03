Quick Start Guide
First Run
bash

# Run with sudo
sudo python3 src/main.py

# Or if installed globally
sudo rpt-swi

Basic Commands
bash

# Quick network scan
sudo rpt-swi --scan

# Show network information
sudo rpt-swi --info

# Block an IP address
sudo rpt-swi --block 192.168.1.100

# Unblock an IP
sudo rpt-swi --unblock 192.168.1.100

# List all devices
sudo rpt-swi --list

# Show statistics
sudo rpt-swi --stats

Interactive Mode

The program has a beautiful interactive menu:

    🔍 Scan Network

    🌐 Show Network Info

    📊 View Devices

    🛡️ Firewall Control

    📈 Statistics

    ⚙️ Settings

    🧪 Tests

    💾 Export Data

Examples
Example 1: Discover all devices
bash

sudo rpt-swi --scan

Example 2: Monitor network continuously
bash

# In interactive mode, select "Scan Network" then "Continuous Monitoring"

Example 3: Block suspicious device
bash

sudo rpt-swi --block 192.168.1.250 --comment "Suspicious activity"

Example 4: Export data
bash

sudo rpt-swi --export scan_results.json

Getting Help
bash

# Show help
sudo rpt-swi --help

# Run diagnostic tests
sudo rpt-swi --test

