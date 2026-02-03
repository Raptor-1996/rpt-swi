#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import time
from datetime import datetime
import readline  # برای تاریخچه دستورات
from tabulate import tabulate
from colorama import init, Fore, Back, Style

init(autoreset=True)

class CLIInterface:
    def __init__(self, scanner, firewall, database, notifier):
        self.scanner = scanner
        self.firewall = firewall
        self.db = database
        self.notifier = notifier
        self.current_view = 'main'
        self.selected_devices = []
        
        # رنگ‌ها
        self.COLORS = {
            'header': Fore.CYAN + Style.BRIGHT,
            'success': Fore.GREEN,
            'warning': Fore.YELLOW,
            'error': Fore.RED,
            'info': Fore.BLUE,
            'menu': Fore.MAGENTA,
            'reset': Style.RESET_ALL
        }
    
    def display_welcome(self):
        """نمایش صفحه خوش آمدگویی"""
        welcome = f"""
{self.COLORS['header']}
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
{self.COLORS['reset']}
        
{self.COLORS['info']}👤 Author: Raptor-1996{self.COLORS['reset']}
{self.COLORS['info']}📧 Email: EbiRom1996@gmail.com{self.COLORS['reset']}
{self.COLORS['info']}🐙 GitHub: https://github.com/Raptor-1996{self.COLORS['reset']}
{self.COLORS['info']}📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{self.COLORS['reset']}
"""
        print(welcome)
        time.sleep(1)
    
    def main_menu(self):
        """منوی اصلی"""
        while True:
            self.clear_screen()
            self.display_header("MAIN MENU")
            
            menu_items = [
                ["1", "Network Information", "View your network details"],
                ["2", "Scan Network", "Discover connected devices"],
                ["3", "Manage Devices", "View/Edit device information"],
                ["4", "Firewall Control", "Block/Unblock devices"],
                ["5", "Monitoring", "Real-time network monitor"],
                ["6", "Reports", "Generate reports and statistics"],
                ["7", "Settings", "Configure program settings"],
                ["8", "Tools", "Additional network tools"],
                ["9", "Help", "Documentation and help"],
                ["0", "Exit", "Exit the program"]
            ]
            
            print(tabulate(menu_items, 
                          headers=["Option", "Function", "Description"],
                          tablefmt="grid",
                          colalign=("center", "left", "left")))
            
            print(f"\n{self.COLORS['menu']}Additional Commands:{self.COLORS['reset']}")
            print("  stats     - Show statistics")
            print("  backup    - Create backup")
            print("  update    - Check for updates")
            print("  clear     - Clear screen")
            print("  history   - Command history")
            
            choice = input(f"\n{self.COLORS['info']}Enter choice (0-9 or command): {self.COLORS['reset']}").strip().lower()
            
            if choice == "0":
                return self.exit_program()
            elif choice == "1":
                self.show_network_info()
            elif choice == "2":
                self.scan_network_menu()
            elif choice == "3":
                self.manage_devices_menu()
            elif choice == "4":
                self.firewall_menu()
            elif choice == "5":
                self.monitoring_menu()
            elif choice == "6":
                self.reports_menu()
            elif choice == "7":
                self.settings_menu()
            elif choice == "8":
                self.tools_menu()
            elif choice == "9":
                self.help_menu()
            elif choice == "stats":
                self.show_statistics()
            elif choice == "backup":
                self.create_backup()
            elif choice == "update":
                self.check_updates()
            elif choice == "clear":
                self.clear_screen()
            elif choice == "history":
                self.show_history()
            else:
                print(f"{self.COLORS['error']}Invalid choice!{self.COLORS['reset']}")
                time.sleep(1)
    
    def show_network_info(self):
        """نمایش اطلاعات شبکه"""
        self.clear_screen()
        self.display_header("NETWORK INFORMATION")
        
        try:
            info = self.scanner.get_network_info()
            
            if not info or not info.get('interfaces'):
                print(f"{self.COLORS['error']}Could not retrieve network information{self.COLORS['reset']}")
                input("\nPress Enter to continue...")
                return
            
            # نمایش اطلاعات هر اینترفیس
            for i, iface in enumerate(info['interfaces'], 1):
                print(f"\n{self.COLORS['header']}[Interface {i}] {iface['name']}{self.COLORS['reset']}")
                print("-" * 50)
                
                interface_data = [
                    ["IP Address", iface.get('ip', 'N/A')],
                    ["MAC Address", iface.get('mac', 'N/A')],
                    ["Netmask", iface.get('netmask', 'N/A')],
                    ["Network", iface.get('network', 'N/A')],
                    ["Broadcast", iface.get('broadcast', 'N/A')]
                ]
                
                print(tabulate(interface_data, tablefmt="simple"))
            
            # نمایش اطلاعات عمومی
            print(f"\n{self.COLORS['header']}[General Information]{self.COLORS['reset']}")
            print("-" * 50)
            
            general_data = [
                ["Default Gateway", info.get('default_gateway', 'N/A')],
                ["DNS Servers", ", ".join(info.get('dns_servers', ['N/A']))],
                ["Public IP", info.get('public_ip', 'N/A')],
                ["Hostname", socket.gethostname()],
                ["System", f"{platform.system()} {platform.release()}"]
            ]
            
            print(tabulate(general_data, tablefmt="simple"))
            
            # نمایش آمار شبکه
            stats = self.db.get_statistics()
            if stats:
                print(f"\n{self.COLORS['header']}[Network Statistics]{self.COLORS['reset']}")
                print("-" * 50)
                
                stats_data = [
                    ["Total Devices", stats.get('total_devices', 0)],
                    ["Active Devices", stats.get('active_devices', 0)],
                    ["Trusted Devices", stats.get('trusted_devices', 0)],
                    ["Blocked Devices", stats.get('blocked_devices', 0)]
                ]
                
                print(tabulate(stats_data, tablefmt="simple"))
            
        except Exception as e:
            print(f"{self.COLORS['error']}Error: {str(e)}{self.COLORS['reset']}")
        
        input("\nPress Enter to continue...")
    
    def scan_network_menu(self):
        """منوی اسکن شبکه"""
        while True:
            self.clear_screen()
            self.display_header("NETWORK SCANNER")
            
            scan_options = [
                ["1", "Quick Scan", "Fast scan (ARP only)"],
                ["2", "Full Scan", "Complete scan (All methods)"],
                ["3", "Deep Scan", "Scan with port detection"],
                ["4", "Continuous Scan", "Monitor network changes"],
                ["5", "Schedule Scan", "Schedule automated scans"],
                ["6", "View Last Results", "Show previous scan results"],
                ["7", "Compare Scans", "Compare with previous scans"],
                ["8", "Export Results", "Export to file"],
                ["0", "Back", "Return to main menu"]
            ]
            
            print(tabulate(scan_options,
                          headers=["Option", "Scan Type", "Description"],
                          tablefmt="grid"))
            
            choice = input(f"\n{self.COLORS['info']}Enter choice (0-8): {self.COLORS['reset']}").strip()
            
            if choice == "0":
                break
            elif choice == "1":
                self.perform_scan("quick")
            elif choice == "2":
                self.perform_scan("full")
            elif choice == "3":
                self.perform_scan("deep")
            elif choice == "4":
                self.continuous_monitoring()
            elif choice == "5":
                self.schedule_scan()
            elif choice == "6":
                self.view_scan_results()
            elif choice == "7":
                self.compare_scans()
            elif choice == "8":
                self.export_results()
            else:
                print(f"{self.COLORS['error']}Invalid choice!{self.COLORS['reset']}")
                time.sleep(1)
    
    def perform_scan(self, scan_type):
        """انجام اسکن شبکه"""
        self.clear_screen()
        self.display_header(f"{scan_type.upper()} SCAN")
        
        # انتخاب اینترفیس
        info = self.scanner.get_network_info()
        interfaces = info.get('interfaces', [])
        
        if not interfaces:
            print(f"{self.COLORS['error']}No network interfaces found!{self.COLORS['reset']}")
            input("\nPress Enter to continue...")
            return
        
        print(f"{self.COLORS['info']}Available interfaces:{self.COLORS['reset']}")
        for i, iface in enumerate(interfaces, 1):
            print(f"  {i}. {iface['name']} ({iface.get('ip', 'No IP')})")
        
        iface_choice = input(f"\n{self.COLORS['info']}Select interface (Enter for default): {self.COLORS['reset']}").strip()
        
        selected_iface = None
        if iface_choice and iface_choice.isdigit():
            idx = int(iface_choice) - 1
            if 0 <= idx < len(interfaces):
                selected_iface = interfaces[idx]['name']
        
        # انتخاب timeout
        print(f"\n{self.COLORS['info']}Scan timeout:{self.COLORS['reset']}")
        print("  1. Fast (15 seconds)")
        print("  2. Normal (30 seconds)")
        print("  3. Thorough (60 seconds)")
        
        timeout_choice = input(f"\n{self.COLORS['info']}Select timeout [2]: {self.COLORS['reset']}").strip() or "2"
        
        timeouts = {"1": 15, "2": 30, "3": 60}
        timeout = timeouts.get(timeout_choice, 30)
        
        # شروع اسکن
        print(f"\n{self.COLORS['warning']}Starting {scan_type} scan...{self.COLORS['reset']}")
        print(f"Interface: {selected_iface or 'Auto'}")
        print(f"Timeout: {timeout} seconds")
        print("\n" + "="*50)
        
        start_time = time.time()
        
        try:
            # نمایش progress bar
            self.show_progress("Scanning network", 0)
            
            # انجام اسکن
            devices = self.scanner.scan_network(
                interface=selected_iface,
                timeout=timeout
            )
            
            duration = time.time() - start_time
            
            self.clear_screen()
            self.display_header("SCAN RESULTS")
            
            print(f"{self.COLORS['success']}Scan completed in {duration:.2f} seconds{self.COLORS['reset']}")
            print(f"{self.COLORS['info']}Devices found: {len(devices)}{self.COLORS['reset']}")
            
            if devices:
                self.display_devices(devices)
            else:
                print(f"\n{self.COLORS['warning']}No devices found!{self.COLORS['reset']}")
            
            # ذخیره نتایج
            save = input(f"\n{self.COLORS['info']}Save results to database? (y/n): {self.COLORS['reset']}").strip().lower()
            if save == 'y':
                self.db.add_scan_record(len(devices), duration, selected_iface, scan_type)
                print(f"{self.COLORS['success']}Results saved!{self.COLORS['reset']}")
            
        except KeyboardInterrupt:
            print(f"\n{self.COLORS['warning']}Scan interrupted by user{self.COLORS['reset']}")
        except Exception as e:
            print(f"\n{self.COLORS['error']}Scan failed: {str(e)}{self.COLORS['reset']}")
        
        input("\nPress Enter to continue...")
    
    def display_devices(self, devices):
        """نمایش دستگاه‌های کشف شده"""
        if not devices:
            print(f"{self.COLORS['warning']}No devices to display{self.COLORS['reset']}")
            return
        
        # آماده‌سازی داده‌ها برای نمایش
        table_data = []
        for i, device in enumerate(devices, 1):
            status = ""
            if device.get('status') == 'blocked':
                status = f"{Fore.RED}[BLOCKED]{Fore.RESET}"
            elif device.get('trusted'):
                status = f"{Fore.GREEN}[TRUSTED]{Fore.RESET}"
            
            row = [
                i,
                device.get('ip', 'N/A'),
                device.get('mac', 'N/A'),
                device.get('hostname', 'Unknown')[:20],
                device.get('vendor', 'Unknown')[:25],
                device.get('last_seen', 'N/A'),
                status
            ]
            table_data.append(row)
        
        headers = ["#", "IP Address", "MAC Address", "Hostname", "Vendor", "Last Seen", "Status"]
        
        print(tabulate(table_data, 
                      headers=headers,
                      tablefmt="grid",
                      maxcolwidths=[None, 15, 17, 20, 25, 10, 10]))
        
        print(f"\n{self.COLORS['info']}Commands:{self.COLORS['reset']}")
        print("  block <number>    - Block selected device")
        print("  trust <number>    - Add to trusted list")
        print("  details <number>  - Show device details")
        print("  export <format>   - Export to JSON/CSV")
        print("  refresh           - Refresh list")
        print("  back              - Return to menu")
    
    def manage_devices_menu(self):
        """منوی مدیریت دستگاه‌ها"""
        while True:
            self.clear_screen()
            self.display_header("DEVICE MANAGEMENT")
            
            # دریافت دستگاه‌ها از دیتابیس
            devices = self.db.get_all_devices()
            
            if not devices:
                print(f"{self.COLORS['warning']}No devices in database{self.COLORS['reset']}")
                print("Please scan the network first.")
                input("\nPress Enter to continue...")
                break
            
            print(f"{self.COLORS['info']}Total devices: {len(devices)}{self.COLORS['reset']}\n")
            
            # نمایش خلاصه
            summary = [
                ["Active", sum(1 for d in devices if 'last_seen' in d and 
                              (datetime.now() - datetime.fromisoformat(d['last_seen'])).days < 1)],
                ["Blocked", sum(1 for d in devices if d.get('status') == 'blocked')],
                ["Trusted", sum(1 for d in devices if d.get('trusted'))],
                ["Unknown", sum(1 for d in devices if d.get('status') == 'unknown')]
            ]
            
            print(tabulate(summary, 
                          headers=["Status", "Count"],
                          tablefmt="simple"))
            
            print(f"\n{self.COLORS['menu']}Management Options:{self.COLORS['reset']}")
            options = [
                ["1", "View All Devices", "Show complete device list"],
                ["2", "Search Device", "Search by IP/MAC/Hostname"],
                ["3", "Trusted Devices", "Manage whitelist"],
                ["4", "Blocked Devices", "View and manage blocked devices"],
                ["5", "Device History", "View device connection history"],
                ["6", "Cleanup Database", "Remove old entries"],
                ["7", "Import/Export", "Import/Export device data"],
                ["0", "Back", "Return to main menu"]
            ]
            
            print(tabulate(options,
                          headers=["Option", "Function", "Description"],
                          tablefmt="simple"))
            
            choice = input(f"\n{self.COLORS['info']}Enter choice (0-7): {self.COLORS['reset']}").strip()
            
            if choice == "0":
                break
            elif choice == "1":
                self.view_all_devices(devices)
            elif choice == "2":
                self.search_device()
            elif choice == "3":
                self.manage_trusted_devices()
            elif choice == "4":
                self.manage_blocked_devices()
            elif choice == "5":
                self.view_device_history()
            elif choice == "6":
                self.cleanup_database()
            elif choice == "7":
                self.import_export_menu()
            else:
                print(f"{self.COLORS['error']}Invalid choice!{self.COLORS['reset']}")
                time.sleep(1)
    
    def firewall_menu(self):
        """منوی فایروال"""
        while True:
            self.clear_screen()
            self.display_header("FIREWALL CONTROL")
            
            # نمایش وضعیت فایروال
            status = self.firewall.get_firewall_status()
            
            print(f"{self.COLORS['info']}Firewall Status:{self.COLORS['reset']}")
            status_data = [
                ["Chain Exists", "✓" if status.get('chain_exists') else "✗"],
                ["Total Rules", status.get('total_rules', 0)],
                ["Blocked IPs", status.get('blocked_ips', 0)],
                ["Saved Rules", status.get('saved_rules_count', 0)]
            ]
            
            print(tabulate(status_data, tablefmt="simple"))
            
            print(f"\n{self.COLORS['menu']}Firewall Options:{self.COLORS['reset']}")
            options = [
                ["1", "Block Device", "Block specific device"],
                ["2", "Block IP", "Block IP address"],
                ["3", "Block Port", "Block network port"],
                ["4", "Unblock Device", "Remove blocking"],
                ["5", "View Rules", "Show current rules"],
                ["6", "Backup/Restore", "Backup/restore rules"],
                ["7", "Schedule Block", "Schedule blocking"],
                ["8", "Advanced Rules", "Custom iptables rules"],
                ["0", "Back", "Return to main menu"]
            ]
            
            print(tabulate(options,
                          headers=["Option", "Action", "Description"],
                          tablefmt="grid"))
            
            choice = input(f"\n{self.COLORS['info']}Enter choice (0-8): {self.COLORS['reset']}").strip()
            
            if choice == "0":
                break
            elif choice == "1":
                self.block_device_ui()
            elif choice == "2":
                self.block_ip_ui()
            elif choice == "3":
                self.block_port_ui()
            elif choice == "4":
                self.unblock_device_ui()
            elif choice == "5":
                self.view_firewall_rules()
            elif choice == "6":
                self.backup_restore_menu()
            elif choice == "7":
                self.schedule_block_ui()
            elif choice == "8":
                self.advanced_rules_ui()
            else:
                print(f"{self.COLORS['error']}Invalid choice!{self.COLORS['reset']}")
                time.sleep(1)
    
    def block_device_ui(self):
        """رابط کاربری برای مسدودسازی دستگاه"""
        self.clear_screen()
        self.display_header("BLOCK DEVICE")
        
        # دریافت دستگاه‌ها
        devices = self.db.get_all_devices()
        
        if not devices:
            print(f"{self.COLORS['warning']}No devices found!{self.COLORS['reset']}")
            print("Please scan the network first.")
            input("\nPress Enter to continue...")
            return
        
        # نمایش دستگاه‌ها
        self.display_devices(devices)
        
        try:
            choice = input(f"\n{self.COLORS['info']}Enter device number to block (or 'all' for all): {self.COLORS['reset']}").strip()
            
            if choice.lower() == 'all':
                confirm = input(f"{self.COLORS['warning']}Block ALL devices? (y/n): {self.COLORS['reset']}").lower()
                if confirm == 'y':
                    blocked_count = 0
                    for device in devices:
                        if not device.get('trusted') and device.get('status') != 'blocked':
                            if self.firewall.block_device(device):
                                blocked_count += 1
                    print(f"{self.COLORS['success']}Blocked {blocked_count} devices{self.COLORS['reset']}")
            elif choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(devices):
                    device = devices[idx]
                    
                    if device.get('trusted'):
                        print(f"{self.COLORS['warning']}This device is trusted!{self.COLORS['reset']}")
                        force = input("Block anyway? (y/n): ").lower()
                        if force != 'y':
                            return
                    
                    comment = input(f"{self.COLORS['info']}Enter comment (optional): {self.COLORS['reset']}").strip()
                    
                    if self.firewall.block_device(device):
                        print(f"{self.COLORS['success']}Device blocked successfully!{self.COLORS['reset']}")
                    else:
                        print(f"{self.COLORS['error']}Failed to block device{self.COLORS['reset']}")
                else:
                    print(f"{self.COLORS['error']}Invalid device number!{self.COLORS['reset']}")
            else:
                print(f"{self.COLORS['error']}Invalid input!{self.COLORS['reset']}")
                
        except Exception as e:
            print(f"{self.COLORS['error']}Error: {str(e)}{self.COLORS['reset']}")
        
        input("\nPress Enter to continue...")
    
    def monitoring_menu(self):
        """منوی مانیتورینگ"""
        self.clear_screen()
        self.display_header("REAL-TIME MONITORING")
        
        print(f"{self.COLORS['info']}Starting network monitor...{self.COLORS['reset']}")
        print("Press Ctrl+C to stop\n")
        
        try:
            import threading
            
            stop_monitoring = False
            
            def monitor_loop():
                known_devices = set()
                alert_count = 0
                
                while not stop_monitoring:
                    try:
                        # اسکن شبکه
                        devices = self.scanner.scan_network(timeout=10)
                        current_ips = {d['ip'] for d in devices if 'ip' in d}
                        
                        # تشخیص دستگاه‌های جدید
                        new_devices = current_ips - known_devices
                        if new_devices:
                            alert_count += 1
                            print(f"{self.COLORS['warning']}[ALERT {alert_count}] New devices detected: {len(new_devices)}{self.COLORS['reset']}")
                            
                            for device in devices:
                                if device['ip'] in new_devices:
                                    print(f"  • {device['ip']} ({device.get('mac', 'Unknown')}) - {device.get('vendor', 'Unknown')}")
                        
                        # تشخیص دستگاه‌های ناپدید شده
                        disappeared = known_devices - current_ips
                        if disappeared:
                            print(f"{self.COLORS['info']}[INFO] Devices disappeared: {len(disappeared)}{self.COLORS['reset']}")
                        
                        known_devices.update(current_ips)
                        
                        # نمایش آمار
                        print(f"\r{self.COLORS['info']}Monitoring... Known devices: {len(known_devices)} | Alerts: {alert_count}{self.COLORS['reset']}", end="")
                        
                        time.sleep(30)  # اسکن هر ۳۰ ثانیه
                        
                    except Exception as e:
                        print(f"\n{self.COLORS['error']}Monitoring error: {str(e)}{self.COLORS['reset']}")
                        time.sleep(10)
            
            # شروع مانیتورینگ در thread جداگانه
            monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
            monitor_thread.start()
            
            # منتظر interrupt کاربر
            try:
                while monitor_thread.is_alive():
                    time.sleep(1)
            except KeyboardInterrupt:
                stop_monitoring = True
                print(f"\n\n{self.COLORS['warning']}Monitoring stopped by user{self.COLORS['reset']}")
            
            monitor_thread.join(timeout=5)
            
        except Exception as e:
            print(f"{self.COLORS['error']}Monitoring failed: {str(e)}{self.COLORS['reset']}")
        
        input("\nPress Enter to continue...")
    
    def show_statistics(self):
        """نمایش آمار"""
        self.clear_screen()
        self.display_header("STATISTICS")
        
        try:
            stats = self.db.get_statistics()
            
            if not stats:
                print(f"{self.COLORS['warning']}No statistics available{self.COLORS['reset']}")
                return
            
            # آمار عمومی
            general_stats = [
                ["Total Devices", stats.get('total_devices', 0)],
                ["Active Devices", stats.get('active_devices', 0)],
                ["Trusted Devices", stats.get('trusted_devices', 0)],
                ["Blocked Devices", stats.get('blocked_devices', 0)],
                ["Total Scans", stats.get('total_scans', 0)],
                ["Unread Notifications", stats.get('unread_notifications', 0)]
            ]
            
            print(f"{self.COLORS['header']}General Statistics:{self.COLORS['reset']}")
            print(tabulate(general_stats, tablefmt="grid"))
            
            # آمار فایروال
            fw_stats = self.firewall.get_firewall_status()
            if fw_stats:
                print(f"\n{self.COLORS['header']}Firewall Statistics:{self.COLORS['reset']}")
                firewall_stats = [
                    ["Chain Status", "Active" if fw_stats.get('chain_exists') else "Inactive"],
                    ["Total Rules", fw_stats.get('total_rules', 0)],
                    ["Blocked IPs", fw_stats.get('blocked_ips', 0)],
                    ["Saved Rules", fw_stats.get('saved_rules_count', 0)]
                ]
                print(tabulate(firewall_stats, tablefmt="grid"))
            
            # آخرین اسکن‌ها
            recent_scans = self.db.get_recent_scans(5)
            if recent_scans:
                print(f"\n{self.COLORS['header']}Recent Scans:{self.COLORS['reset']}")
                scan_data = []
                for scan in recent_scans:
                    scan_time = datetime.fromisoformat(scan['scan_time']) if 'scan_time' in scan else 'N/A'
                    scan_data.append([
                        scan.get('id'),
                        scan_time.strftime('%Y-%m-%d %H:%M') if scan_time != 'N/A' else 'N/A',
                        scan.get('devices_found', 0),
                        scan.get('duration_seconds', 0),
                        scan.get('scan_type', 'Unknown')
                    ])
                
                print(tabulate(scan_data,
                              headers=["ID", "Time", "Devices", "Duration", "Type"],
                              tablefmt="simple"))
            
        except Exception as e:
            print(f"{self.COLORS['error']}Error loading statistics: {str(e)}{self.COLORS['reset']}")
        
        input("\nPress Enter to continue...")
    
    def display_header(self, title):
        """نمایش هدر"""
        width = 70
        print(f"{self.COLORS['header']}{'=' * width}{self.COLORS['reset']}")
        print(f"{self.COLORS['header']}{title.center(width)}{self.COLORS['reset']}")
        print(f"{self.COLORS['header']}{'=' * width}{self.COLORS['reset']}\n")
    
    def clear_screen(self):
        """پاک کردن صفحه"""
        import os
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def show_progress(self, message, progress):
        """نمایش نوار پیشرفت"""
        bar_length = 40
        filled_length = int(bar_length * progress)
        bar = '█' * filled_length + '░' * (bar_length - filled_length)
        percent = int(progress * 100)
        
        sys.stdout.write(f'\r{message}: [{bar}] {percent}%')
        sys.stdout.flush()
        
        if progress >= 1:
            sys.stdout.write('\n')
    
    def exit_program(self):
        """خروج از برنامه"""
        self.clear_screen()
        print(f"\n{self.COLORS['header']}Thank you for using RPT See Who Is In!{self.COLORS['reset']}")
        print(f"{self.COLORS['info']}Created by Raptor-1996{self.COLORS['reset']}")
        print(f"{self.COLORS['info']}GitHub: https://github.com/Raptor-1996{self.COLORS['reset']}")
        print(f"{self.COLORS['info']}Email: EbiRom1996@gmail.com{self.COLORS['reset']}\n")
        return False
    
    # متدهای دیگر (خلاصه شده)
    def view_all_devices(self, devices):
        # مشاهده همه دستگاه‌ها
        pass
    
    def search_device(self):
        # جستجوی دستگاه
        pass
    
    def manage_trusted_devices(self):
        # مدیریت دستگاه‌های معتمد
        pass
    
    def manage_blocked_devices(self):
        # مدیریت دستگاه‌های مسدود شده
        pass
    
    def view_device_history(self):
        # مشاهده تاریخچه دستگاه
        pass
    
    def cleanup_database(self):
        # پاک‌سازی دیتابیس
        pass
    
    def import_export_menu(self):
        # منوی واردکردن/صادرکردن
        pass
    
    def block_ip_ui(self):
        # رابط کاربری مسدودسازی IP
        pass
    
    def block_port_ui(self):
        # رابط کاربری مسدودسازی پورت
        pass
    
    def unblock_device_ui(self):
        # رابط کاربری آزادسازی دستگاه
        pass
    
    def view_firewall_rules(self):
        # مشاهده قوانین فایروال
        pass
    
    def backup_restore_menu(self):
        # منوی پشتیبان‌گیری/بازیابی
        pass
    
    def schedule_block_ui(self):
        # زمان‌بندی مسدودسازی
        pass
    
    def advanced_rules_ui(self):
        # قوانین پیشرفته
        pass
    
    def reports_menu(self):
        # منوی گزارشات
        pass
    
    def settings_menu(self):
        # منوی تنظیمات
        pass
    
    def tools_menu(self):
        # منوی ابزارها
        pass
    
    def help_menu(self):
        # منوی کمک
        pass
    
    def create_backup(self):
        # ایجاد پشتیبان
        pass
    
    def check_updates(self):
        # بررسی بروزرسانی
        pass
    
    def show_history(self):
        # نمایش تاریخچه دستورات
        pass
    
    def view_scan_results(self):
        # مشاهده نتایج اسکن
        pass
    
    def compare_scans(self):
        # مقایسه اسکن‌ها
        pass
    
    def export_results(self):
        # صادر کردن نتایج
        pass
    
    def continuous_monitoring(self):
        # مانیتورینگ پیوسته
        pass
    
    def schedule_scan(self):
        # زمان‌بندی اسکن
        pass
