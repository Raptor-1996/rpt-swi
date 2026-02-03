#!/bin/bash
# Uninstall Script for RPT See Who Is In

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_header() {
    echo -e "${BLUE}"
    echo "╔══════════════════════════════════════════════════════════╗"
    echo "║                                                          ║"
    echo "║               RPT SWI Uninstaller                        ║"
    echo "║                                                          ║"
    echo "╚══════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

print_status() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

check_root() {
    if [[ $EUID -ne 0 ]]; then
        print_error "This script must be run as root"
        exit 1
    fi
}

stop_services() {
    print_status "Stopping RPT SWI services..."
    
    # Stop systemd service
    if systemctl is-active --quiet rpt-swi; then
        systemctl stop rpt-swi
        print_status "Service stopped"
    fi
    
    # Disable service
    if systemctl is-enabled --quiet rpt-swi; then
        systemctl disable rpt-swi
        print_status "Service disabled"
    fi
    
    # Remove service file
    if [ -f /etc/systemd/system/rpt-swi.service ]; then
        rm -f /etc/systemd/system/rpt-swi.service
        systemctl daemon-reload
        print_status "Service file removed"
    fi
}

remove_program_files() {
    print_status "Removing program files..."
    
    # Remove program directory
    if [ -d /opt/rpt-swi ]; then
        rm -rf /opt/rpt-swi
        print_status "Program directory removed: /opt/rpt-swi"
    fi
    
    # Remove symlinks
    if [ -f /usr/local/bin/rpt-swi ]; then
        rm -f /usr/local/bin/rpt-swi
        print_status "Symlink removed: /usr/local/bin/rpt-swi"
    fi
    
    if [ -f /usr/local/bin/rptswi ]; then
        rm -f /usr/local/bin/rptswi
        print_status "Symlink removed: /usr/local/bin/rptswi"
    fi
}

remove_config_files() {
    print_status "Removing configuration files..."
    
    # Remove system config
    if [ -d /etc/rpt-swi ]; then
        rm -rf /etc/rpt-swi
        print_status "System config removed: /etc/rpt-swi"
    fi
    
    # Remove user config
    if [ -d ~/.config/rpt-swi ]; then
        rm -rf ~/.config/rpt-swi
        print_status "User config removed: ~/.config/rpt-swi"
    fi
    
    if [ -d /root/.config/rpt-swi ]; then
        rm -rf /root/.config/rpt-swi
        print_status "Root config removed: /root/.config/rpt-swi"
    fi
    
    # Remove log files
    if [ -d /var/log/rpt-swi ]; then
        rm -rf /var/log/rpt-swi
        print_status "Log files removed: /var/log/rpt-swi"
    fi
    
    # Remove logrotate config
    if [ -f /etc/logrotate.d/rpt-swi ]; then
        rm -f /etc/logrotate.d/rpt-swi
        print_status "Logrotate config removed"
    fi
}

cleanup_firewall() {
    print_status "Cleaning up firewall rules..."
    
    # Try to remove RPT-SWI chain
    if command -v iptables > /dev/null; then
        # Remove chain from INPUT
        iptables -D INPUT -j RPT-SWI 2>/dev/null || true
        
        # Flush chain
        iptables -F RPT-SWI 2>/dev/null || true
        
        # Delete chain
        iptables -X RPT-SWI 2>/dev/null || true
        
        print_status "Firewall rules cleaned up"
    else
        print_warning "iptables not found, skipping firewall cleanup"
    fi
}

remove_dependencies() {
    local response
    read -p "Remove installed dependencies? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_status "Removing dependencies..."
        
        if [ -f /etc/debian_version ]; then
            # Debian/Ubuntu
            apt-get remove -y \
                nmap \
                arp-scan \
                python3-iptables \
                python3-netifaces \
                python3-scapy
            
            apt-get autoremove -y
            
        elif [ -f /etc/redhat-release ]; then
            # RedHat/CentOS/Fedora
            yum remove -y \
                nmap \
                arp-scan \
                python3-iptables \
                python3-netifaces \
                python3-scapy
            
        elif [ -f /etc/arch-release ]; then
            # Arch Linux
            pacman -Rns --noconfirm \
                nmap \
                arp-scan \
                python-iptables \
                python-netifaces \
                python-scapy
        fi
        
        print_status "Dependencies removed"
    else
        print_status "Skipping dependency removal"
    fi
}

cleanup_cron() {
    print_status "Cleaning up cron jobs..."
    
    # Remove backup cron job
    crontab -l 2>/dev/null | grep -v '/opt/rpt-swi/backup.sh' | crontab - 2>/dev/null || true
    
    print_status "Cron jobs cleaned up"
}

show_summary() {
    echo -e "\n${GREEN}Uninstall Complete!${NC}"
    echo "======================================"
    echo ""
    echo "The following items have been removed:"
    echo ""
    echo "✓ Program files (/opt/rpt-swi)"
    echo "✓ Systemd service"
    echo "✓ Configuration files"
    echo "✓ Log files"
    echo "✓ Symlinks"
    echo "✓ Firewall rules"
    echo "✓ Cron jobs"
    echo ""
    echo "The following items remain:"
    echo ""
    echo "• Python packages (if not removed)"
    echo "• System dependencies (if not removed)"
    echo "• User data in home directories"
    echo ""
    echo -e "${YELLOW}Note:${NC} Some configuration and log files may still exist"
    echo "in user home directories (~/.config/rpt-swi)"
    echo ""
    echo "To completely remove all traces, manually delete:"
    echo "  ~/.config/rpt-swi"
    echo "  /root/.config/rpt-swi"
    echo ""
    echo -e "${BLUE}Thank you for using RPT See Who Is In!${NC}"
    echo "We hope to see you again soon."
    echo ""
}

main() {
    print_header
    
    echo -e "${YELLOW}This will completely uninstall RPT See Who Is In.${NC}"
    echo ""
    
    # تایید کاربر
    read -p "Are you sure you want to continue? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Uninstall cancelled."
        exit 0
    fi
    
    check_root
    
    echo ""
    echo -e "${YELLOW}Starting uninstall process...${NC}"
    echo ""
    
    stop_services
    remove_program_files
    remove_config_files
    cleanup_firewall
    cleanup_cron
    
    echo ""
    read -p "Remove user data? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        # Remove all user data
        find /home -name ".config/rpt-swi" -type d -exec rm -rf {} + 2>/dev/null || true
        find /root -name ".config/rpt-swi" -type d -exec rm -rf {} + 2>/dev/null || true
        print_status "User data removed"
    fi
    
    remove_dependencies
    
    show_summary
}

# Run main function
main "$@"
