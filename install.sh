#!/bin/bash
# Professional Installation Script for RPT SWI

set -e  # Exit on error

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_header() {
    clear
    echo -e "${BLUE}"
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║                                                            ║"
    echo "║    ██████╗ ██████╗ ████████╗    ███████╗██╗    ██╗██╗      ║"
    echo "║    ██╔══██╗██╔══██╗╚══██╔══╝    ██╔════╝██║    ██║██║      ║"
    echo "║    ██████╔╝██████╔╝   ██║       ███████╗██║ █╗ ██║██║      ║"
    echo "║    ██╔══██╗██╔═══╝    ██║       ╚════██║██║███╗██║██║      ║"
    echo "║    ██║  ██║██║        ██║       ███████║╚███╔███╔╝███████╗ ║"
    echo "║    ╚═╝  ╚═╝╚═╝        ╚═╝       ╚══════╝ ╚══╝╚══╝ ╚══════╝ ║"
    echo "║                                                            ║"
    echo "║         See Who Is In - Professional Edition v2.0          ║"
    echo "║                                                            ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo "Created by: Raptor-1996"
    echo "GitHub: https://github.com/Raptor-1996"
    echo "Email: EbiRom1996@gmail.com"
    echo ""
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

check_os() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        OS=$NAME
        VER=$VERSION_ID
    else
        OS=$(uname -s)
        VER=$(uname -r)
    fi
    
    print_status "Detected OS: $OS $VER"
}

install_dependencies_debian() {
    print_status "Installing dependencies for Debian/Ubuntu..."
    
    apt-get update
    apt-get install -y \
        python3 \
        python3-pip \
        python3-venv \
        nmap \
        arp-scan \
        net-tools \
        iptables \
        iptables-persistent \
        sqlite3 \
        libpcap-dev \
        tcpdump \
        git \
        curl \
        wget
    
    # Install Python packages
    pip3 install --upgrade pip
    pip3 install \
        scapy \
        python-iptables \
        netifaces \
        pandas \
        requests \
        colorama \
        tabulate \
        psutil
}

install_dependencies_centos() {
    print_status "Installing dependencies for CentOS/RHEL/Fedora..."
    
    yum install -y \
        python3 \
        python3-pip \
        nmap \
        arp-scan \
        net-tools \
        iptables \
        iptables-services \
        sqlite \
        libpcap-devel \
        tcpdump \
        git \
        curl \
        wget
    
    pip3 install --upgrade pip
    pip3 install \
        scapy \
        python-iptables \
        netifaces \
        pandas \
        requests \
        colorama \
        tabulate \
        psutil
}

install_dependencies_arch() {
    print_status "Installing dependencies for Arch Linux..."
    
    pacman -Syu --noconfirm \
        python \
        python-pip \
        nmap \
        arp-scan \
        net-tools \
        iptables \
        sqlite \
        libpcap \
        tcpdump \
        git \
        curl \
        wget
    
    pip3 install --upgrade pip
    pip3 install \
        scapy \
        python-iptables \
        netifaces \
        pandas \
        requests \
        colorama \
        tabulate \
        psutil
}

setup_python_environment() {
    print_status "Setting up Python virtual environment..."
    
    # Create virtual environment
    python3 -m venv /opt/rpt-swi/venv
    
    # Activate and install requirements
    source /opt/rpt-swi/venv/bin/activate
    pip install -r /opt/rpt-swi/requirements.txt
    
    print_status "Python environment setup complete"
}

install_program() {
    print_status "Installing RPT SWI..."
    
    # Create directory structure
    mkdir -p /opt/rpt-swi
    mkdir -p /var/log/rpt-swi
    mkdir -p /etc/rpt-swi
    
    # Copy program files
    cp -r src/* /opt/rpt-swi/
    cp requirements.txt /opt/rpt-swi/
    cp README.md /opt/rpt-swi/
    cp LICENSE /opt/rpt-swi/
    
    # Copy configuration
    cp config/settings.example.yaml /etc/rpt-swi/settings.yaml
    
    # Set permissions
    chmod -R 755 /opt/rpt-swi
    chmod 644 /etc/rpt-swi/settings.yaml
    chmod 755 /opt/rpt-swi/main.py
    
    # Create symlinks
    ln -sf /opt/rpt-swi/main.py /usr/local/bin/rpt-swi
    ln -sf /opt/rpt-swi/main.py /usr/local/bin/rptswi
    
    # Create systemd service
    cat > /etc/systemd/system/rpt-swi.service << EOF
[Unit]
Description=RPT See Who Is In - Network Security Monitor
After=network.target
Wants=network.target

[Service]
Type=simple
User=root
ExecStart=/opt/rpt-swi/venv/bin/python /opt/rpt-swi/main.py
Restart=on-failure
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF
    
    # Create logrotate configuration
    cat > /etc/logrotate.d/rpt-swi << EOF
/var/log/rpt-swi/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 640 root root
    sharedscripts
    postrotate
        systemctl reload rpt-swi > /dev/null 2>&1 || true
    endscript
}
EOF
    
    print_status "Program files installed"
}

setup_database() {
    print_status "Setting up database..."
    
    # Create user config directory
    mkdir -p /root/.config/rpt-swi
    chmod 700 /root/.config/rpt-swi
    
    # Initialize database
    if [ -f /opt/rpt-swi/init_db.py ]; then
        python3 /opt/rpt-swi/init_db.py
    fi
    
    print_status "Database setup complete"
}

configure_firewall() {
    print_status "Configuring firewall..."
    
    # Enable IP forwarding if not already enabled
    if [ "$(cat /proc/sys/net/ipv4/ip_forward)" != "1" ]; then
        echo "1" > /proc/sys/net/ipv4/ip_forward
        echo "net.ipv4.ip_forward = 1" >> /etc/sysctl.conf
        sysctl -p
    fi
    
    # Create initial iptables rules
    iptables -N RPT-SWI 2>/dev/null || true
    iptables -C INPUT -j RPT-SWI 2>/dev/null || iptables -A INPUT -j RPT-SWI
    
    # Save iptables rules
    if command -v iptables-save > /dev/null; then
        iptables-save > /etc/iptables/rules.v4
    fi
    
    print_status "Firewall configured"
}

create_backup_script() {
    print_status "Creating backup script..."
    
    cat > /opt/rpt-swi/backup.sh << 'EOF'
#!/bin/bash
# Backup script for RPT SWI

BACKUP_DIR="/var/backups/rpt-swi"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup database
cp /root/.config/rpt-swi/devices.db $BACKUP_DIR/devices_$TIMESTAMP.db 2>/dev/null

# Backup configuration
cp /etc/rpt-swi/settings.yaml $BACKUP_DIR/settings_$TIMESTAMP.yaml 2>/dev/null

# Backup iptables rules
iptables-save > $BACKUP_DIR/iptables_$TIMESTAMP.rules 2>/dev/null

# Create archive
tar -czf $BACKUP_DIR/backup_$TIMESTAMP.tar.gz -C $BACKUP_DIR devices_$TIMESTAMP.db settings_$TIMESTAMP.yaml iptables_$TIMESTAMP.rules

# Cleanup old backups (keep 30 days)
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete
find $BACKUP_DIR -name "*.db" -mtime +1 -delete
find $BACKUP_DIR -name "*.yaml" -mtime +1 -delete
find $BACKUP_DIR -name "*.rules" -mtime +1 -delete

echo "Backup completed: $BACKUP_DIR/backup_$TIMESTAMP.tar.gz"
EOF
    
    chmod +x /opt/rpt-swi/backup.sh
    
    # Add to crontab
    (crontab -l 2>/dev/null; echo "0 2 * * * /opt/rpt-swi/backup.sh") | crontab -
    
    print_status "Backup system configured"
}

show_completion() {
    print_header
    echo -e "${GREEN}Installation Complete!${NC}"
    echo ""
    echo "RPT See Who Is In has been successfully installed."
    echo ""
    echo "${BLUE}Usage:${NC}"
    echo "  rpt-swi              # Start interactive mode"
    echo "  rpt-swi --scan       # Quick network scan"
    echo "  rpt-swi --help       # Show help"
    echo ""
    echo "${BLUE}Service Management:${NC}"
    echo "  systemctl start rpt-swi    # Start as service"
    echo "  systemctl enable rpt-swi   # Enable auto-start"
    echo "  systemctl status rpt-swi   # Check status"
    echo ""
    echo "${BLUE}Configuration:${NC}"
    echo "  Edit: /etc/rpt-swi/settings.yaml"
    echo "  Logs: /var/log/rpt-swi/"
    echo "  Data: /root/.config/rpt-swi/"
    echo ""
    echo "${YELLOW}Important:${NC}"
    echo "1. Review firewall rules in /etc/rpt-swi/settings.yaml"
    echo "2. Run initial scan: sudo rpt-swi --scan"
    echo "3. Check logs: tail -f /var/log/rpt-swi/rpt_swi.log"
    echo ""
    echo "Need help? Email: EbiRom1996@gmail.com"
    echo "GitHub: https://github.com/Raptor-1996/rpt-swi"
    echo ""
}

main() {
    print_header
    check_root
    check_os
    
    echo -e "${YELLOW}Starting installation...${NC}"
    echo ""
    
    # Install dependencies based on OS
    case $OS in
        *Debian*|*Ubuntu*|*Mint*)
            install_dependencies_debian
            ;;
        *CentOS*|*RHEL*|*Fedora*|*Amazon*)
            install_dependencies_centos
            ;;
        *Arch*|*Manjaro*)
            install_dependencies_arch
            ;;
        *)
            print_error "Unsupported operating system: $OS"
            print_warning "You may need to install dependencies manually"
            read -p "Continue anyway? (y/n): " -n 1 -r
            echo
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                exit 1
            fi
            ;;
    esac
    
    install_program
    setup_python_environment
    setup_database
    configure_firewall
    create_backup_script
    
    # Enable and start service
    systemctl daemon-reload
    systemctl enable rpt-swi
    systemctl start rpt-swi
    
    show_completion
}

# Run main function
main "$@"
