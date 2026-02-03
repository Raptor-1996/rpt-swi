#!/bin/bash
Quick Start Script for RPT SWI

set -e

echo "RPT See Who Is In - Quick Start"
echo "================================"
Check if running as root

if [ "$EUID" -ne 0 ]; then
echo "Please run as root: sudo bash quickstart.sh"
exit 1
fi
Colors

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
echo -e "${GREEN}[✓]${NC} $1"
}

print_warning() {
echo -e "${YELLOW}[!]${NC} $1"
}

print_error() {
echo -e "${RED}[✗]${NC} $1"
}
Detect OS

if [ -f /etc/os-release ]; then
. /etc/os-release
OS=$NAME
VER=$VERSION_ID
else
OS=$(uname -s)
VER=$(uname -r)
fi

print_status "Detected OS: $OS $VER"
Install dependencies

print_status "Installing dependencies..."

if [[ "$OS" == "Ubuntu" ]] || [[ "$OS" == "Debian" ]]; then
apt-get update
apt-get install -y python3 python3-pip nmap iptables net-tools

elif [[ "$OS" == "CentOS" ]] || [[ "$OS" == "Red Hat" ]] || [[ "$OS" == "Fedora" ]]; then
yum install -y python3 python3-pip nmap iptables net-tools

elif [[ "$OS" == "Arch" ]] || [[ "$OS" == "Manjaro" ]]; then
pacman -Syu --noconfirm python python-pip nmap iptables net-tools

else
print_warning "Unknown OS. Please install manually:"
print_warning " python3, nmap, iptables, net-tools"
read -p "Continue anyway? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
exit 1
fi
fi
Install Python packages

print_status "Installing Python packages..."
pip3 install --upgrade pip
pip3 install scapy python-iptables netifaces colorama tabulate requests
Create program directory

print_status "Setting up program..."
mkdir -p /opt/rpt-swi
cp -r ./* /opt/rpt-swi/ 2>/dev/null || true
Make executable

chmod +x /opt/rpt-swi/src/main.py
Create symlink

ln -sf /opt/rpt-swi/src/main.py /usr/local/bin/rpt-swi 2>/dev/null || true
Create config directory

mkdir -p ~/.config/rpt-swi

print_status "Installation complete!"
echo ""
echo -e "${BLUE}Usage:${NC}"
echo " sudo rpt-swi # Start interactive mode"
echo " sudo rpt-swi --scan # Quick network scan"
echo " sudo rpt-swi --help # Show help"
echo ""
echo -e "${GREEN}Examples:${NC}"
echo " sudo rpt-swi --scan --output scan.json"
echo " sudo rpt-swi --block 192.168.1.100"
echo " sudo rpt-swi --stats"
echo ""
echo -e "${YELLOW}Note:${NC} Some features require additional tools:"
echo " arp-scan - For ARP scanning"
echo " sqlite3 - For database features"
echo ""
echo "Enjoy using RPT See Who Is In! 🚀"
