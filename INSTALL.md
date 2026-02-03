# Installation Guide for RPT See Who Is In

## Quick Install (Ubuntu/Debian)
```bash
# Method 1: Using install script
wget https://github.com/Raptor-1996/rpt-swi/raw/main/install.sh
chmod +x install.sh
sudo ./install.sh
```

# Method 2: Manual installation
```
sudo apt-get update
sudo apt-get install -y python3 python3-pip nmap arp-scan iptables
git clone https://github.com/Raptor-1996/rpt-swi.git
cd rpt-swi
sudo python3 -m pip install -r requirements.txt
sudo python3 src/main.py
```

Docker Installation

# Using Docker Compose
```
docker-compose up -d
```
# Using Docker directly
```
docker build -t rpt-swi .
docker run -it --net=host --privileged rpt-swi
```
# Manual Installation (All Linux)

    Install dependencies:
    bash

# Debian/Ubuntu
```
sudo apt-get install python3 python3-pip nmap iptables
```
# CentOS/RHEL/Fedora
```
sudo yum install python3 python3-pip nmap iptables
```
# Arch Linux
```
sudo pacman -S python python-pip nmap iptables
```
# Install Python packages:
```bash
sudo pip3 install scapy python-iptables netifaces colorama tabulate
```
# Clone and run:
```bash

git clone https://github.com/Raptor-1996/rpt-swi.git
cd rpt-swi
sudo python3 src/main.py
```
# Verification

# After installation, run:
```bash
sudo rpt-swi --test
```
This will verify all dependencies are installed correctly.
