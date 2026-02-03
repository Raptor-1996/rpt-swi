#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RPT See Who Is In - Professional Network Security Tool
Version: 2.0.0
Author: Raptor-1996
GitHub: https://github.com/Raptor-1996
Email: EbiRom1996@gmail.com
"""

import os
import sys
import time
import json
import sqlite3
import socket
import argparse
import subprocess
import threading
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import logging

# ==================== COLORS & UI ====================
class Colors:
    """کلاس مدیریت رنگ‌های ترمینال"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    
    @staticmethod
    def print(text: str, color: str = None):
        """چاپ متن رنگی"""
        if color:
            print(f"{color}{text}{Colors.END}")
        else:
            print(text)

class Banner:
    """نمایش بنر برنامه"""
    @staticmethod
    def show():
        """نمایش بنر اصلی"""
        banner = f"""
{Colors.CYAN}{Colors.BOLD}
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
{Colors.END}
        """
        print(banner)
        
        info = f"""
{Colors.GREEN}👤 Author: Raptor-1996{Colors.END}
{Colors.GREEN}📧 Email: EbiRom1996@gmail.com{Colors.END}
{Colors.GREEN}🐙 GitHub: https://github.com/Raptor-1996{Colors.END}
{Colors.GREEN}📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.END}
        """
        print(info)

# ==================== DATABASE ====================
class DeviceDatabase:
    """مدیریت پایگاه داده دستگاه‌ها"""
    
    def __init__(self, db_path: str = None):
        """مقداردهی اولیه پایگاه داده"""
        if db_path is None:
            config_dir = Path.home() / '.config' / 'rpt-swi'
            config_dir.mkdir(parents=True, exist_ok=True)
            db_path = str(config_dir / 'devices.db')
        
        self.db_path = db_path
        self.connection = None
        self._init_database()
    
    def _init_database(self):
        """ایجاد جداول پایگاه داده"""
        try:
            self.connection = sqlite3.connect(self.db_path)
            cursor = self.connection.cursor()
            
            # جدول دستگاه‌ها
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS devices (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ip_address TEXT UNIQUE NOT NULL,
                    mac_address TEXT,
                    hostname TEXT,
                    vendor TEXT,
                    first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status TEXT DEFAULT 'unknown',
                    is_trusted INTEGER DEFAULT 0,
                    is_blocked INTEGER DEFAULT 0,
                    open_ports TEXT,
                    os_guess TEXT,
                    notes TEXT
                )
            ''')
            
            # جدول اسکن‌ها
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS scans (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    scan_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    scan_type TEXT,
                    interface TEXT,
                    devices_found INTEGER,
                    duration_seconds REAL,
                    success INTEGER DEFAULT 1
                )
            ''')
            
            # جدول رویدادها
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    event_type TEXT,
                    event_source TEXT,
                    event_data TEXT,
                    severity TEXT DEFAULT 'info'
                )
            ''')
            
            # جدول قوانین فایروال
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS firewall_rules (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    rule_type TEXT,
                    target_ip TEXT,
                    target_mac TEXT,
                    action TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP,
                    is_active INTEGER DEFAULT 1,
                    notes TEXT
                )
            ''')
            
            # ایجاد ایندکس‌ها
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_devices_ip ON devices(ip_address)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_devices_mac ON devices(mac_address)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_devices_status ON devices(status)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_scans_time ON scans(scan_time)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_events_time ON events(event_time)')
            
            self.connection.commit()
            
        except sqlite3.Error as e:
            print(f"{Colors.RED}Database error: {e}{Colors.END}")
            raise
    
    def add_device(self, device: Dict) -> bool:
        """افزودن یا به‌روزرسانی دستگاه"""
        try:
            cursor = self.connection.cursor()
            
            # بررسی وجود دستگاه
            cursor.execute(
                "SELECT id FROM devices WHERE ip_address = ? OR mac_address = ?",
                (device.get('ip'), device.get('mac'))
            )
            existing = cursor.fetchone()
            
            if existing:
                # به‌روزرسانی دستگاه موجود
                cursor.execute('''
                    UPDATE devices SET
                        mac_address = COALESCE(?, mac_address),
                        hostname = COALESCE(?, hostname),
                        vendor = COALESCE(?, vendor),
                        last_seen = ?,
                        status = 'online'
                    WHERE ip_address = ? OR mac_address = ?
                ''', (
                    device.get('mac'),
                    device.get('hostname'),
                    device.get('vendor'),
                    datetime.now(),
                    device.get('ip'),
                    device.get('mac')
                ))
            else:
                # افزودن دستگاه جدید
                cursor.execute('''
                    INSERT INTO devices 
                    (ip_address, mac_address, hostname, vendor, first_seen, last_seen, status)
                    VALUES (?, ?, ?, ?, ?, ?, 'online')
                ''', (
                    device.get('ip'),
                    device.get('mac'),
                    device.get('hostname'),
                    device.get('vendor'),
                    datetime.now(),
                    datetime.now()
                ))
            
            self.connection.commit()
            return True
            
        except sqlite3.Error as e:
            print(f"{Colors.RED}Error adding device: {e}{Colors.END}")
            return False
    
    def get_devices(self, status: str = None, trusted: bool = None) -> List[Dict]:
        """دریافت لیست دستگاه‌ها"""
        try:
            cursor = self.connection.cursor()
            
            query = "SELECT * FROM devices WHERE 1=1"
            params = []
            
            if status:
                query += " AND status = ?"
                params.append(status)
            
            if trusted is not None:
                query += " AND is_trusted = ?"
                params.append(1 if trusted else 0)
            
            query += " ORDER BY last_seen DESC"
            
            cursor.execute(query, params)
            
            columns = [desc[0] for desc in cursor.description]
            devices = []
            
            for row in cursor.fetchall():
                device = dict(zip(columns, row))
                devices.append(device)
            
            return devices
            
        except sqlite3.Error as e:
            print(f"{Colors.RED}Error getting devices: {e}{Colors.END}")
            return []
    
    def log_event(self, event_type: str, source: str, data: str, severity: str = "info"):
        """ثبت رویداد در پایگاه داده"""
        try:
            cursor = self.connection.cursor()
            
            cursor.execute('''
                INSERT INTO events (event_type, event_source, event_data, severity)
                VALUES (?, ?, ?, ?)
            ''', (event_type, source, data, severity))
            
            self.connection.commit()
            return True
            
        except sqlite3.Error as e:
            print(f"{Colors.RED}Error logging event: {e}{Colors.END}")
            return False
    
    def close(self):
        """بستن اتصال به پایگاه داده"""
        if self.connection:
            self.connection.close()

# ==================== NETWORK SCANNER ====================
class NetworkScanner:
    """اسکنر شبکه پیشرفته"""
    
    def __init__(self, database: DeviceDatabase):
        self.db = database
        self.my_info = self._get_my_network_info()
    
    def _get_my_network_info(self) -> Dict:
        """دریافت اطلاعات شبکه جاری"""
        info = {}
        
        try:
            # نام میزبان
            info['hostname'] = socket.gethostname()
            
            # آدرس IP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            info['ip'] = s.getsockname()[0]
            s.close()
            
            # آدرس MAC
            try:
                # تلاش برای دریافت MAC از کارت شبکه فعال
                import uuid
                mac = uuid.getnode()
                info['mac'] = ':'.join(['{:02x}'.format((mac >> ele) & 0xff) 
                                       for ele in range(0, 8*6, 8)][::-1])
            except:
                info['mac'] = 'Unknown'
            
            # اطلاعات اینترفیس
            try:
                import netifaces
                interfaces = netifaces.interfaces()
                info['interfaces'] = []
                
                for iface in interfaces:
                    if iface != 'lo':
                        addrs = netifaces.ifaddresses(iface)
                        if netifaces.AF_INET in addrs:
                            ip_info = addrs[netifaces.AF_INET][0]
                            info['interfaces'].append({
                                'name': iface,
                                'ip': ip_info.get('addr'),
                                'netmask': ip_info.get('netmask')
                            })
            except ImportError:
                info['interfaces'] = []
            
            # Gateway و DNS
            try:
                import netifaces
                gateways = netifaces.gateways()
                if 'default' in gateways and netifaces.AF_INET in gateways['default']:
                    info['gateway'] = gateways['default'][netifaces.AF_INET][0]
            except:
                info['gateway'] = 'Unknown'
            
        except Exception as e:
            print(f"{Colors.YELLOW}Warning: {e}{Colors.END}")
            info = {'ip': 'Unknown', 'mac': 'Unknown', 'hostname': 'Unknown'}
        
        return info
    
    def scan_network(self, scan_type: str = "quick", interface: str = None) -> Tuple[List[Dict], Dict]:
        """اسکن شبکه"""
        Colors.print(f"\n🔍 Starting {scan_type} scan...", Colors.BLUE)
        
        devices = []
        start_time = time.time()
        
        try:
            if scan_type == "quick":
                devices = self._quick_scan()
            elif scan_type == "arp":
                devices = self._arp_scan()
            elif scan_type == "nmap":
                devices = self._nmap_scan()
            elif scan_type == "full":
                devices = self._full_scan()
            else:
                devices = self._quick_scan()
            
            # افزودن اطلاعات سازنده از MAC
            for device in devices:
                if 'mac' in device and device['mac'] != 'Unknown':
                    device['vendor'] = self._get_vendor_from_mac(device['mac'])
            
            # ذخیره در پایگاه داده
            for device in devices:
                self.db.add_device(device)
            
            # ثبت اسکن
            duration = time.time() - start_time
            self._log_scan(scan_type, len(devices), duration, interface)
            
        except Exception as e:
            Colors.print(f"Scan error: {e}", Colors.RED)
        
        return devices, self.my_info
    
    def _quick_scan(self) -> List[Dict]:
        """اسکن سریع با استفاده از nmap"""
        devices = []
        
        try:
            # تعیین شبکه بر اساس IP جاری
            if self.my_info['ip'] != 'Unknown':
                ip_parts = self.my_info['ip'].split('.')
                network = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.0/24"
            else:
                network = "192.168.1.0/24"
            
            Colors.print(f"📡 Scanning network: {network}", Colors.BLUE)
            
            # اجرای nmap
            cmd = ['nmap', '-sn', '-n', network]
            result = subprocess.run(cmd, 
                                  capture_output=True, 
                                  text=True,
                                  timeout=60)
            
            current_device = {}
            for line in result.stdout.split('\n'):
                if 'Nmap scan report for' in line:
                    if current_device:
                        devices.append(current_device)
                    ip = line.split()[-1]
                    current_device = {'ip': ip, 'mac': 'Unknown', 'hostname': 'Unknown'}
                
                elif 'MAC Address:' in line:
                    parts = line.split(':', 1)
                    if len(parts) > 1:
                        mac_info = parts[1].strip()
                        # استخراج MAC و سازنده
                        mac_parts = mac_info.split(' ')
                        if mac_parts:
                            current_device['mac'] = mac_parts[0].upper()
                            if len(mac_parts) > 1:
                                current_device['vendor'] = ' '.join(mac_parts[1:]).strip('()')
            
            if current_device:
                devices.append(current_device)
            
            Colors.print(f"✅ Found {len(devices)} devices", Colors.GREEN)
            
        except subprocess.TimeoutExpired:
            Colors.print("⏰ Scan timeout", Colors.YELLOW)
        except Exception as e:
            Colors.print(f"Scan error: {e}", Colors.RED)
        
        return devices
    
    def _arp_scan(self) -> List[Dict]:
        """اسکن با استفاده از ARP"""
        devices = []
        
        try:
            # استفاده از جدول ARP سیستم
            cmd = ['arp', '-n']
            result = subprocess.run(cmd, 
                                  capture_output=True, 
                                  text=True)
            
            for line in result.stdout.split('\n'):
                parts = line.split()
                if len(parts) >= 3 and '.' in parts[0]:
                    devices.append({
                        'ip': parts[0],
                        'mac': parts[2].upper(),
                        'hostname': parts[1] if parts[1] != '?' else 'Unknown'
                    })
            
            Colors.print(f"✅ ARP found {len(devices)} devices", Colors.GREEN)
            
        except Exception as e:
            Colors.print(f"ARP scan error: {e}", Colors.YELLOW)
        
        return devices
    
    def _nmap_scan(self) -> List[Dict]:
        """اسکن کامل با nmap"""
        return self._quick_scan()  # در حال حاضر مشابه quick scan
    
    def _full_scan(self) -> List[Dict]:
        """اسکن کامل با تمام روش‌ها"""
        devices = []
        
        # ترکیب نتایج از همه روش‌ها
        nmap_devices = self._quick_scan()
        arp_devices = self._arp_scan()
        
        # ادغام و حذف تکراری‌ها
        seen_ips = set()
        all_devices = nmap_devices + arp_devices
        
        for device in all_devices:
            if device['ip'] not in seen_ips:
                seen_ips.add(device['ip'])
                devices.append(device)
        
        Colors.print(f"✅ Full scan found {len(devices)} unique devices", Colors.GREEN)
        return devices
    
    def _get_vendor_from_mac(self, mac: str) -> str:
        """دریافت نام سازنده از آدرس MAC"""
        # این یک لیست ساده است. در نسخه کامل از دیتابیس IEEE OUI استفاده می‌شود
        vendors = {
            '00:50:56': 'VMware',
            '00:0C:29': 'VMware',
            '00:1C:14': 'VMware',
            '00:05:69': 'VMware',
            '08:00:27': 'VirtualBox',
            '00:1D:0F': 'Cisco',
            '00:1E:13': 'Cisco',
            '00:24:E4': 'Dell',
            '00:26:B9': 'Dell',
            '00:13:D4': 'Intel',
            '00:15:00': 'Intel',
            '00:16:EA': 'Intel',
            '00:03:93': 'Apple',
            '00:05:02': 'Apple',
            '00:0A:27': 'Apple',
            '00:1B:63': 'Apple',
            '00:1C:B3': 'Apple',
            '00:1D:4F': 'Apple',
            '00:1E:52': 'Apple',
            '00:1E:C2': 'Apple',
            '00:1F:5B': 'Apple',
            '00:1F:F3': 'Apple',
            '00:21:E9': 'Apple',
            '00:22:41': 'Apple',
            '00:23:12': 'Apple',
            '00:23:32': 'Apple',
            '00:23:6C': 'Apple',
            '00:23:DF': 'Apple',
            '00:24:36': 'Apple',
            '00:24:A5': 'Apple',
            '00:25:00': 'Apple',
            '00:25:4B': 'Apple',
            '00:25:BC': 'Apple',
        }
        
        mac_prefix = mac.upper().replace(':', '')[:6]
        
        for prefix, vendor in vendors.items():
            if mac_prefix.startswith(prefix.replace(':', '')):
                return vendor
        
        return "Unknown"
    
    def _log_scan(self, scan_type: str, devices_found: int, duration: float, interface: str):
        """ثبت اطلاعات اسکن در پایگاه داده"""
        try:
            cursor = self.db.connection.cursor()
            
            cursor.execute('''
                INSERT INTO scans (scan_type, interface, devices_found, duration_seconds)
                VALUES (?, ?, ?, ?)
            ''', (scan_type, interface, devices_found, duration))
            
            self.db.connection.commit()
            
        except Exception as e:
            print(f"{Colors.YELLOW}Failed to log scan: {e}{Colors.END}")

# ==================== FIREWALL MANAGER ====================
class FirewallManager:
    """مدیریت فایروال"""
    
    def __init__(self, database: DeviceDatabase):
        self.db = database
        self.chain_name = "RPT-SWI"
        self._ensure_chain_exists()
    
    def _ensure_chain_exists(self):
        """اطمینان از وجود زنجیره فایروال"""
        try:
            # بررسی وجود زنجیره
            result = subprocess.run(['iptables', '-L', self.chain_name, '-n'],
                                  capture_output=True,
                                  text=True)
            
            if result.returncode != 0:
                # ایجاد زنجیره جدید
                subprocess.run(['iptables', '-N', self.chain_name], check=True)
                subprocess.run(['iptables', '-A', 'INPUT', '-j', self.chain_name], check=True)
                Colors.print(f"✅ Created firewall chain: {self.chain_name}", Colors.GREEN)
                
        except Exception as e:
            Colors.print(f"⚠ Firewall chain error: {e}", Colors.YELLOW)
    
    def block_device(self, ip_address: str, mac_address: str = None, comment: str = "") -> bool:
        """مسدودسازی دستگاه"""
        try:
            # مسدودسازی با IP
            cmd = ['iptables', '-A', self.chain_name, '-s', ip_address, '-j', 'DROP']
            subprocess.run(cmd, check=True)
            
            # مسدودسازی با MAC اگر موجود باشد
            if mac_address:
                cmd = ['iptables', '-A', self.chain_name, '-m', 'mac',
                      '--mac-source', mac_address, '-j', 'DROP']
                subprocess.run(cmd, check=True)
            
            # به‌روزرسانی وضعیت در پایگاه داده
            cursor = self.db.connection.cursor()
            cursor.execute(
                "UPDATE devices SET is_blocked = 1 WHERE ip_address = ? OR mac_address = ?",
                (ip_address, mac_address)
            )
            
            # ثبت رویداد
            self.db.log_event(
                "device_blocked",
                "firewall",
                json.dumps({'ip': ip_address, 'mac': mac_address, 'comment': comment}),
                "warning"
            )
            
            Colors.print(f"✅ Blocked device: {ip_address} ({mac_address or 'No MAC'})", Colors.GREEN)
            return True
            
        except Exception as e:
            Colors.print(f"❌ Failed to block device: {e}", Colors.RED)
            return False
    
    def unblock_device(self, ip_address: str, mac_address: str = None) -> bool:
        """آزادسازی دستگاه"""
        try:
            # حذف قوانین IP
            subprocess.run(['iptables', '-D', self.chain_name, '-s', ip_address, '-j', 'DROP'],
                         stderr=subprocess.DEVNULL)
            
            # حذف قوانین MAC
            if mac_address:
                subprocess.run(['iptables', '-D', self.chain_name, '-m', 'mac',
                              '--mac-source', mac_address, '-j', 'DROP'],
                             stderr=subprocess.DEVNULL)
            
            # به‌روزرسانی وضعیت در پایگاه داده
            cursor = self.db.connection.cursor()
            cursor.execute(
                "UPDATE devices SET is_blocked = 0 WHERE ip_address = ? OR mac_address = ?",
                (ip_address, mac_address)
            )
            
            # ثبت رویداد
            self.db.log_event(
                "device_unblocked",
                "firewall",
                json.dumps({'ip': ip_address, 'mac': mac_address}),
                "info"
            )
            
            Colors.print(f"✅ Unblocked device: {ip_address}", Colors.GREEN)
            return True
            
        except Exception as e:
            Colors.print(f"⚠ Could not unblock device: {e}", Colors.YELLOW)
            return False
    
    def list_blocked_devices(self) -> List[Dict]:
        """لیست دستگاه‌های مسدود شده"""
        try:
            cursor = self.db.connection.cursor()
            cursor.execute(
                "SELECT * FROM devices WHERE is_blocked = 1 ORDER BY last_seen DESC"
            )
            
            columns = [desc[0] for desc in cursor.description]
            devices = [dict(zip(columns, row)) for row in cursor.fetchall()]
            
            return devices
            
        except Exception as e:
            Colors.print(f"Error getting blocked devices: {e}", Colors.RED)
            return []
    
    def get_firewall_status(self) -> Dict:
        """دریافت وضعیت فایروال"""
        status = {
            'chain_exists': False,
            'total_rules': 0,
            'blocked_ips': 0
        }
        
        try:
            # بررسی وجود زنجیره
            result = subprocess.run(['iptables', '-L', self.chain_name, '-n'],
                                  capture_output=True,
                                  text=True)
            
            if result.returncode == 0:
                status['chain_exists'] = True
                
                # شمارش قوانین
                lines = result.stdout.strip().split('\n')
                if len(lines) > 2:
                    status['total_rules'] = len(lines) - 2
                    
                    # شمارش IP‌های مسدود شده
                    for line in lines[2:]:
                        if 'DROP' in line and '0.0.0.0/0' not in line:
                            status['blocked_ips'] += 1
            
        except Exception as e:
            Colors.print(f"Error getting firewall status: {e}", Colors.YELLOW)
        
        return status

# ==================== UI & DISPLAY ====================
class DisplayManager:
    """مدیریت نمایش اطلاعات"""
    
    @staticmethod
    def show_devices(devices: List[Dict], my_ip: str = None):
        """نمایش دستگاه‌های کشف شده"""
        if not devices:
            Colors.print("❌ No devices found!", Colors.RED)
            return
        
        print("\n" + "="*80)
        print(f"{'DEVICES FOUND':^80}")
        print("="*80)
        
        print(f"\n{'#':<3} {'IP Address':<15} {'MAC Address':<17} {'Hostname':<20} {'Vendor':<20} {'Status':<10}")
        print("-"*85)
        
        for i, device in enumerate(devices, 1):
            ip = device.get('ip_address', device.get('ip', 'Unknown'))
            mac = device.get('mac_address', device.get('mac', 'Unknown'))
            hostname = device.get('hostname', 'Unknown')
            vendor = device.get('vendor', 'Unknown')[:20]
            
            # تعیین وضعیت
            if my_ip and ip == my_ip:
                status = f"{Colors.GREEN}[YOU]{Colors.END}"
            elif device.get('is_blocked'):
                status = f"{Colors.RED}[BLOCKED]{Colors.END}"
            elif device.get('is_trusted'):
                status = f"{Colors.BLUE}[TRUSTED]{Colors.END}"
            else:
                status = ""
            
            print(f"{i:<3} {ip:<15} {mac[:17]:<17} {hostname[:20]:<20} {vendor:<20} {status}")
        
        print("\n" + "="*80)
    
    @staticmethod
    def show_network_info(info: Dict):
        """نمایش اطلاعات شبکه"""
        print("\n" + "="*60)
        print(f"{'NETWORK INFORMATION':^60}")
        print("="*60)
        
        print(f"\n{Colors.BOLD}Your Information:{Colors.END}")
        print(f"  Hostname: {info.get('hostname', 'Unknown')}")
        print(f"  IP Address: {info.get('ip', 'Unknown')}")
        print(f"  MAC Address: {info.get('mac', 'Unknown')}")
        
        if 'gateway' in info:
            print(f"  Gateway: {info.get('gateway', 'Unknown')}")
        
        if 'interfaces' in info and info['interfaces']:
            print(f"\n{Colors.BOLD}Network Interfaces:{Colors.END}")
            for iface in info['interfaces']:
                print(f"  {iface.get('name')}: {iface.get('ip')} / {iface.get('netmask')}")
        
        print("\n" + "="*60)
    
    @staticmethod
    def show_menu():
        """نمایش منوی اصلی"""
        menu_items = [
            ("1", "🔍 Scan Network", "Discover devices on your network"),
            ("2", "🌐 Network Info", "Show your network configuration"),
            ("3", "📊 View Devices", "Show all discovered devices"),
            ("4", "🛡️ Firewall", "Block/unblock devices"),
            ("5", "📈 Statistics", "Show program statistics"),
            ("6", "⚙️ Settings", "Configure program settings"),
            ("7", "🧪 Tests", "Run diagnostic tests"),
            ("8", "💾 Export Data", "Export data to file"),
            ("9", "❓ Help", "Show help information"),
            ("0", "🚪 Exit", "Exit the program")
        ]
        
        print("\n" + "="*60)
        print(f"{'MAIN MENU':^60}")
        print("="*60)
        
        for item in menu_items:
            print(f"{Colors.BOLD}{item[0]:<2}{Colors.END} {item[1]:<20} {item[2]}")
        
        print("="*60)

# ==================== MAIN APPLICATION ====================
class RPTswiApplication:
    """کلاس اصلی برنامه"""
    
    def __init__(self):
        """مقداردهی اولیه برنامه"""
        self.db = DeviceDatabase()
        self.scanner = NetworkScanner(self.db)
        self.firewall = FirewallManager(self.db)
        self.display = DisplayManager()
        self.running = True
        
        # ثبت شروع برنامه
        self.db.log_event("program_start", "system", "RPT SWI started", "info")
    
    def run(self):
        """اجرای برنامه"""
        Banner.show()
        
        while self.running:
            try:
                self.display.show_menu()
                choice = input(f"\n{Colors.BOLD}Select option (0-9): {Colors.END}").strip()
                
                if choice == "1":
                    self.scan_network_menu()
                elif choice == "2":
                    self.show_network_info()
                elif choice == "3":
                    self.view_devices()
                elif choice == "4":
                    self.firewall_menu()
                elif choice == "5":
                    self.show_statistics()
                elif choice == "6":
                    self.settings_menu()
                elif choice == "7":
                    self.run_tests()
                elif choice == "8":
                    self.export_data()
                elif choice == "9":
                    self.show_help()
                elif choice == "0":
                    self.exit_program()
                else:
                    Colors.print("❌ Invalid choice! Please select 0-9", Colors.RED)
                
            except KeyboardInterrupt:
                Colors.print("\n\n⚠ Program interrupted by user", Colors.YELLOW)
                self.exit_program()
            except Exception as e:
                Colors.print(f"\n❌ Error: {e}", Colors.RED)
    
    def scan_network_menu(self):
        """منوی اسکن شبکه"""
        print("\n" + "="*60)
        print(f"{'SCAN NETWORK':^60}")
        print("="*60)
        
        print("\nSelect scan type:")
        print("1. Quick Scan (Fast, nmap only)")
        print("2. ARP Scan (Very fast, local network)")
        print("3. Full Scan (Comprehensive, all methods)")
        print("4. Back to main menu")
        
        choice = input(f"\n{Colors.BOLD}Select (1-4): {Colors.END}").strip()
        
        if choice == "1":
            devices, my_info = self.scanner.scan_network("quick")
            self.display.show_devices(devices, my_info.get('ip'))
        elif choice == "2":
            devices, my_info = self.scanner.scan_network("arp")
            self.display.show_devices(devices, my_info.get('ip'))
        elif choice == "3":
            devices, my_info = self.scanner.scan_network("full")
            self.display.show_devices(devices, my_info.get('ip'))
        elif choice == "4":
            return
        else:
            Colors.print("❌ Invalid choice!", Colors.RED)
    
    def show_network_info(self):
        """نمایش اطلاعات شبکه"""
        self.display.show_network_info(self.scanner.my_info)
        input(f"\n{Colors.BOLD}Press Enter to continue...{Colors.END}")
    
    def view_devices(self):
        """نمایش دستگاه‌های کشف شده"""
        devices = self.db.get_devices()
        
        if not devices:
            Colors.print("❌ No devices in database. Scan network first!", Colors.YELLOW)
            return
        
        print("\n" + "="*60)
        print(f"{'VIEW DEVICES':^60}")
        print("="*60)
        
        print("\nFilter options:")
        print("1. All devices")
        print("2. Online devices")
        print("3. Blocked devices")
        print("4. Trusted devices")
        print("5. Back to main menu")
        
        choice = input(f"\n{Colors.BOLD}Select (1-5): {Colors.END}").strip()
        
        filtered_devices = []
        
        if choice == "1":
            filtered_devices = devices
        elif choice == "2":
            filtered_devices = [d for d in devices if d.get('status') == 'online']
        elif choice == "3":
            filtered_devices = [d for d in devices if d.get('is_blocked')]
        elif choice == "4":
            filtered_devices = [d for d in devices if d.get('is_trusted')]
        elif choice == "5":
            return
        else:
            Colors.print("❌ Invalid choice!", Colors.RED)
            return
        
        self.display.show_devices(filtered_devices, self.scanner.my_info.get('ip'))
        
        # گزینه‌های مدیریت دستگاه
        if filtered_devices:
            print("\nDevice Management:")
            print("  block <number>   - Block selected device")
            print("  trust <number>   - Mark as trusted")
            print("  details <number> - Show device details")
            print("  back             - Return to menu")
            
            cmd = input(f"\n{Colors.BOLD}Enter command: {Colors.END}").strip().lower()
            
            if cmd.startswith('block '):
                try:
                    num = int(cmd.split()[1]) - 1
                    if 0 <= num < len(filtered_devices):
                        device = filtered_devices[num]
                        self.firewall.block_device(
                            device.get('ip_address', device.get('ip')),
                            device.get('mac_address', device.get('mac')),
                            "Manual block"
                        )
                except:
                    Colors.print("❌ Invalid device number!", Colors.RED)
            
            elif cmd.startswith('trust '):
                try:
                    num = int(cmd.split()[1]) - 1
                    if 0 <= num < len(filtered_devices):
                        device = filtered_devices[num]
                        cursor = self.db.connection.cursor()
                        cursor.execute(
                            "UPDATE devices SET is_trusted = 1 WHERE ip_address = ?",
                            (device.get('ip_address', device.get('ip')),)
                        )
                        self.db.connection.commit()
                        Colors.print(f"✅ Device marked as trusted: {device.get('ip_address')}", Colors.GREEN)
                except:
                    Colors.print("❌ Invalid device number!", Colors.RED)
        
        input(f"\n{Colors.BOLD}Press Enter to continue...{Colors.END}")
    
    def firewall_menu(self):
        """منوی فایروال"""
        while True:
            print("\n" + "="*60)
            print(f"{'FIREWALL CONTROL':^60}")
            print("="*60)
            
            status = self.firewall.get_firewall_status()
            
            print(f"\n{Colors.BOLD}Firewall Status:{Colors.END}")
            print(f"  Chain: {'✅ Active' if status['chain_exists'] else '❌ Inactive'}")
            print(f"  Total Rules: {status['total_rules']}")
            print(f"  Blocked IPs: {status['blocked_ips']}")
            
            print("\nOptions:")
            print("1. List blocked devices")
            print("2. Block a device")
            print("3. Unblock a device")
            print("4. Show firewall rules")
            print("5. Back to main menu")
            
            choice = input(f"\n{Colors.BOLD}Select (1-5): {Colors.END}").strip()
            
            if choice == "1":
                blocked = self.firewall.list_blocked_devices()
                if blocked:
                    self.display.show_devices(blocked, self.scanner.my_info.get('ip'))
                else:
                    Colors.print("✅ No devices are blocked", Colors.GREEN)
                    
            elif choice == "2":
                ip = input("Enter IP address to block: ").strip()
                if ip:
                    mac = input("Enter MAC address (optional): ").strip()
                    comment = input("Enter comment (optional): ").strip()
                    self.firewall.block_device(ip, mac if mac else None, comment)
                    
            elif choice == "3":
                blocked = self.firewall.list_blocked_devices()
                if blocked:
                    print("\nBlocked devices:")
                    for i, device in enumerate(blocked, 1):
                        print(f"{i}. {device.get('ip_address')} ({device.get('mac_address', 'No MAC')})")
                    
                    try:
                        num = int(input("\nEnter device number to unblock: ").strip()) - 1
                        if 0 <= num < len(blocked):
                            device = blocked[num]
                            self.firewall.unblock_device(
                                device.get('ip_address'),
                                device.get('mac_address')
                            )
                    except:
                        Colors.print("❌ Invalid selection!", Colors.RED)
                else:
                    Colors.print("✅ No devices to unblock", Colors.GREEN)
                    
            elif choice == "4":
                print("\nFirewall Rules:")
                subprocess.run(['iptables', '-L', self.firewall.chain_name, '-n', '--line-numbers'])
                
            elif choice == "5":
                break
                
            else:
                Colors.print("❌ Invalid choice!", Colors.RED)
            
            input(f"\n{Colors.BOLD}Press Enter to continue...{Colors.END}")
    
    def show_statistics(self):
        """نمایش آمار برنامه"""
        try:
            cursor = self.db.connection.cursor()
            
            # شمارش دستگاه‌ها
            cursor.execute("SELECT COUNT(*) FROM devices")
            total_devices = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM devices WHERE status = 'online'")
            online_devices = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM devices WHERE is_blocked = 1")
            blocked_devices = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM devices WHERE is_trusted = 1")
            trusted_devices = cursor.fetchone()[0]
            
            # شمارش اسکن‌ها
            cursor.execute("SELECT COUNT(*) FROM scans")
            total_scans = cursor.fetchone()[0]
            
            # آخرین اسکن
            cursor.execute("SELECT MAX(scan_time) FROM scans")
            last_scan = cursor.fetchone()[0]
            
            print("\n" + "="*60)
            print(f"{'STATISTICS':^60}")
            print("="*60)
            
            print(f"\n{Colors.BOLD}Device Statistics:{Colors.END}")
            print(f"  Total Devices: {total_devices}")
            print(f"  Online Devices: {online_devices}")
            print(f"  Blocked Devices: {blocked_devices}")
            print(f"  Trusted Devices: {trusted_devices}")
            
            print(f"\n{Colors.BOLD}Scan Statistics:{Colors.END}")
            print(f"  Total Scans: {total_scans}")
            print(f"  Last Scan: {last_scan or 'Never'}")
            
            print(f"\n{Colors.BOLD}Firewall Statistics:{Colors.END}")
            status = self.firewall.get_firewall_status()
            print(f"  Chain Status: {'Active' if status['chain_exists'] else 'Inactive'}")
            print(f"  Total Rules: {status['total_rules']}")
            print(f"  Blocked IPs: {status['blocked_ips']}")
            
            print("\n" + "="*60)
            
        except Exception as e:
            Colors.print(f"Error getting statistics: {e}", Colors.RED)
        
        input(f"\n{Colors.BOLD}Press Enter to continue...{Colors.END}")
    
    def settings_menu(self):
        """منوی تنظیمات"""
        print("\n" + "="*60)
        print(f"{'SETTINGS':^60}")
        print("="*60)
        
        print("\nSettings options:")
        print("1. Database management")
        print("2. Firewall settings")
        print("3. Scan settings")
        print("4. Notification settings")
        print("5. Back to main menu")
        
        choice = input(f"\n{Colors.BOLD}Select (1-5): {Colors.END}").strip()
        
        if choice == "1":
            print("\nDatabase Management:")
            print("1. Clear database")
            print("2. Backup database")
            print("3. Restore database")
            print("4. Show database info")
            
            db_choice = input(f"\n{Colors.BOLD}Select (1-4): {Colors.END}").strip()
            
            if db_choice == "1":
                confirm = input("Are you sure you want to clear all data? (yes/no): ").lower()
                if confirm == 'yes':
                    cursor = self.db.connection.cursor()
                    cursor.execute("DELETE FROM devices")
                    cursor.execute("DELETE FROM scans")
                    cursor.execute("DELETE FROM events")
                    self.db.connection.commit()
                    Colors.print("✅ Database cleared", Colors.GREEN)
                    
        elif choice == "2":
            print("\nFirewall Settings:")
            new_chain = input(f"Enter new chain name [{self.firewall.chain_name}]: ").strip()
            if new_chain:
                self.firewall.chain_name = new_chain
                Colors.print(f"✅ Firewall chain name updated to: {new_chain}", Colors.GREEN)
        
        input(f"\n{Colors.BOLD}Press Enter to continue...{Colors.END}")
    
    def run_tests(self):
        """اجرای تست‌های تشخیصی"""
        Colors.print("\n🧪 Running diagnostic tests...", Colors.BLUE)
        
        tests = [
            ("Python Version", lambda: sys.version.split()[0]),
            ("Root Access", lambda: "✅" if os.geteuid() == 0 else "❌"),
            ("Nmap", lambda: "✅" if self._check_command('nmap') else "❌"),
            ("iptables", lambda: "✅" if self._check_command('iptables') else "❌"),
            ("Database", lambda: "✅" if self.db.connection else "❌"),
            ("Network Info", lambda: "✅" if self.scanner.my_info.get('ip') != 'Unknown' else "❌"),
        ]
        
        print("\n" + "="*60)
        print(f"{'DIAGNOSTIC TESTS':^60}")
        print("="*60)
        
        for test_name, test_func in tests:
            try:
                result = test_func()
                print(f"{test_name:<20} {result}")
            except Exception as e:
                print(f"{test_name:<20} ❌ Error: {e}")
        
        print("\n" + "="*60)
        
        input(f"\n{Colors.BOLD}Press Enter to continue...{Colors.END}")
    
    def _check_command(self, cmd: str) -> bool:
        """بررسی وجود دستور در سیستم"""
        try:
            subprocess.run(['which', cmd], capture_output=True, check=True)
            return True
        except:
            return False
    
    def export_data(self):
        """صادر کردن داده‌ها"""
        print("\n" + "="*60)
        print(f"{'EXPORT DATA':^60}")
        print("="*60)
        
        print("\nExport options:")
        print("1. Export devices to JSON")
        print("2. Export devices to CSV")
        print("3. Export scan history")
        print("4. Export events log")
        print("5. Back to main menu")
        
        choice = input(f"\n{Colors.BOLD}Select (1-5): {Colors.END}").strip()
        
        if choice == "1":
            devices = self.db.get_devices()
            filename = f"devices_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            data = {
                'export_time': datetime.now().isoformat(),
                'total_devices': len(devices),
                'devices': devices
            }
            
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2, default=str)
            
            Colors.print(f"✅ Devices exported to: {filename}", Colors.GREEN)
        
        input(f"\n{Colors.BOLD}Press Enter to continue...{Colors.END}")
    
    def show_help(self):
        """نمایش راهنمای برنامه"""
        help_text = f"""
{Colors.BOLD}RPT See Who Is In - Help{Colors.END}

{Colors.UNDERLINE}Overview:{Colors.END}
RPT See Who Is In is a professional network security tool for monitoring
and managing devices on your network.

{Colors.UNDERLINE}Features:{Colors.END}
• Network scanning and device discovery
• MAC address vendor detection
• Firewall management (block/unblock devices)
• Database for tracking devices over time
• Statistics and reporting
• Export data to JSON/CSV

{Colors.UNDERLINE}Requirements:{Colors.END}
• Linux operating system
• Python 3.6+
• nmap, iptables, arp-scan (optional)
• Root/administrator privileges

{Colors.UNDERLINE}Basic Usage:{Colors.END}
1. Scan your network to discover devices
2. View device information and vendors
3. Block suspicious devices using firewall
4. Monitor network changes over time

{Colors.UNDERLINE}Contact:{Colors.END}
Author: Raptor-1996
Email: EbiRom1996@gmail.com
GitHub: https://github.com/Raptor-1996

{Colors.BOLD}Always use this tool responsibly and only on networks you own or have permission to monitor.{Colors.END}
        """
        
        print(help_text)
        input(f"\n{Colors.BOLD}Press Enter to continue...{Colors.END}")
    
    def exit_program(self):
        """خروج از برنامه"""
        Colors.print("\n👋 Thank you for using RPT See Who Is In!", Colors.GREEN)
        Colors.print("Created by: Raptor-1996", Colors.BLUE)
        Colors.print("Email: EbiRom1996@gmail.com", Colors.BLUE)
        Colors.print("GitHub: https://github.com/Raptor-1996\n", Colors.BLUE)
        
        # ثبت خروج برنامه
        self.db.log_event("program_exit", "system", "RPT SWI exited normally", "info")
        
        # بستن پایگاه داده
        self.db.close()
        
        self.running = False

# ==================== COMMAND LINE INTERFACE ====================
def parse_arguments():
    """پارسی‌سازی آرگومان‌های خط فرمان"""
    parser = argparse.ArgumentParser(
        description='RPT See Who Is In - Professional Network Security Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  sudo python3 main.py              # Start interactive mode
  sudo python3 main.py --scan       # Quick network scan
  sudo python3 main.py --block 192.168.1.100  # Block an IP
  sudo python3 main.py --list       # List all devices
  sudo python3 main.py --stats      # Show statistics
        """
    )
    
    parser.add_argument('--scan', '-s', action='store_true',
                       help='Perform a quick network scan')
    parser.add_argument('--scan-type', choices=['quick', 'arp', 'full'],
                       default='quick', help='Type of scan to perform')
    parser.add_argument('--block', '-b', metavar='IP',
                       help='Block a specific IP address')
    parser.add_argument('--unblock', '-u', metavar='IP',
                       help='Unblock a specific IP address')
    parser.add_argument('--list', '-l', action='store_true',
                       help='List all discovered devices')
    parser.add_argument('--stats', action='store_true',
                       help='Show program statistics')
    parser.add_argument('--info', '-i', action='store_true',
                       help='Show network information')
    parser.add_argument('--export', '-e', metavar='FILE',
                       help='Export data to JSON file')
    parser.add_argument('--test', '-t', action='store_true',
                       help='Run diagnostic tests')
    parser.add_argument('--version', '-v', action='store_true',
                       help='Show version information')
    
    return parser.parse_args()

def main():
    """تابع اصلی اجرای برنامه"""
    args = parse_arguments()
    
    # نمایش نسخه
    if args.version:
        print("RPT See Who Is In v2.0.0")
        print("Created by Raptor-1996")
        return
    
    # بررسی دسترسی root
    if os.geteuid() != 0:
        print(f"{Colors.RED}❌ Error: This program must be run as root!{Colors.END}")
        print(f"{Colors.YELLOW}💡 Please run: sudo python3 main.py{Colors.END}")
        sys.exit(1)
    
    # ایجاد نمونه برنامه
    app = RPTswiApplication()
    
    try:
        # پردازش آرگومان‌های خط فرمان
        if args.scan:
            devices, my_info = app.scanner.scan_network(args.scan_type)
            app.display.show_devices(devices, my_info.get('ip'))
            
        elif args.block:
            app.firewall.block_device(args.block, comment="Command line block")
            
        elif args.unblock:
            app.firewall.unblock_device(args.unblock)
            
        elif args.list:
            devices = app.db.get_devices()
            app.display.show_devices(devices, app.scanner.my_info.get('ip'))
            
        elif args.stats:
            app.show_statistics()
            
        elif args.info:
            app.display.show_network_info(app.scanner.my_info)
            
        elif args.export:
            devices = app.db.get_devices()
            data = {
                'export_time': datetime.now().isoformat(),
                'devices': devices
            }
            with open(args.export, 'w') as f:
                json.dump(data, f, indent=2, default=str)
            Colors.print(f"✅ Data exported to: {args.export}", Colors.GREEN)
            
        elif args.test:
            app.run_tests()
            
        else:
            # حالت تعاملی
            app.run()
            
    except KeyboardInterrupt:
        Colors.print("\n\n⚠ Program interrupted by user", Colors.YELLOW)
        app.exit_program()
    except Exception as e:
        Colors.print(f"\n❌ Fatal error: {e}", Colors.RED)
        sys.exit(1)

if __name__ == "__main__":
    main()
