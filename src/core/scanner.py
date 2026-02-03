#!/usr/bin/env python3

import subprocess
import re
import socket
import threading
import ipaddress
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import netifaces
import scapy.all as scapy
import pandas as pd

class NetworkScanner:
    def __init__(self, database):
        self.db = database
        self.logger = database.logger
        self.active_scans = {}
        
    def get_network_info(self):
        """Get comprehensive network information"""
        info = {
            'interfaces': [],
            'default_gateway': None,
            'dns_servers': [],
            'public_ip': None
        }
        
        try:
            # Get all interfaces
            interfaces = netifaces.interfaces()
            for iface in interfaces:
                if iface == 'lo':
                    continue
                    
                addrs = netifaces.ifaddresses(iface)
                if netifaces.AF_INET in addrs:
                    ip_info = addrs[netifaces.AF_INET][0]
                    mac_info = addrs[netifaces.AF_LINK][0] if netifaces.AF_LINK in addrs else {}
                    
                    interface_info = {
                        'name': iface,
                        'ip': ip_info.get('addr'),
                        'netmask': ip_info.get('netmask'),
                        'broadcast': ip_info.get('broadcast'),
                        'mac': mac_info.get('addr', '00:00:00:00:00:00')
                    }
                    
                    # Calculate network
                    if interface_info['ip'] and interface_info['netmask']:
                        network = ipaddress.IPv4Network(
                            f"{interface_info['ip']}/{interface_info['netmask']}", 
                            strict=False
                        )
                        interface_info['network'] = str(network)
                    
                    info['interfaces'].append(interface_info)
            
            # Get gateway
            gateways = netifaces.gateways()
            if 'default' in gateways and netifaces.AF_INET in gateways['default']:
                info['default_gateway'] = gateways['default'][netifaces.AF_INET]
            
            # Get DNS from resolv.conf
            try:
                with open('/etc/resolv.conf', 'r') as f:
                    for line in f:
                        if line.startswith('nameserver'):
                            dns = line.split()[1]
                            info['dns_servers'].append(dns)
            except:
                pass
            
            # Get public IP
            try:
                import requests
                info['public_ip'] = requests.get('https://api.ipify.org', timeout=3).text
            except:
                pass
            
            self.logger.log(f"Retrieved network info for {len(info['interfaces'])} interfaces")
            
        except Exception as e:
            self.logger.log(f"Error getting network info: {str(e)}", level="ERROR")
        
        return info
    
    def scan_network(self, interface=None, timeout=30):
        """Scan network using multiple methods"""
        self.logger.log(f"Starting network scan (timeout: {timeout}s)")
        
        devices = []
        scan_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.active_scans[scan_id] = {'status': 'running', 'devices_found': 0}
        
        try:
            # Method 1: ARP Scan (fastest)
            arp_devices = self._arp_scan(interface, timeout//3)
            devices.extend(arp_devices)
            
            # Method 2: Nmap Ping Scan
            nmap_devices = self._nmap_scan(interface, timeout//3)
            devices.extend([d for d in nmap_devices if not any(d['ip'] == existing['ip'] for existing in devices)])
            
            # Method 3: ICMP Ping Sweep
            icmp_devices = self._icmp_scan(interface, timeout//3)
            devices.extend([d for d in icmp_devices if not any(d['ip'] == existing['ip'] for existing in devices)])
            
            # Get details for each device
            with ThreadPoolExecutor(max_workers=10) as executor:
                futures = []
                for device in devices:
                    futures.append(executor.submit(self._enrich_device_info, device))
                
                enriched_devices = []
                for future in as_completed(futures):
                    try:
                        enriched_devices.append(future.result())
                    except Exception as e:
                        self.logger.log(f"Error enriching device: {str(e)}")
            
            # Remove duplicates
            unique_devices = self._remove_duplicates(enriched_devices)
            
            # Update database
            for device in unique_devices:
                self.db.add_or_update_device(device)
            
            self.active_scans[scan_id].update({
                'status': 'completed',
                'devices_found': len(unique_devices),
                'end_time': datetime.now()
            })
            
            self.logger.log(f"Scan completed: Found {len(unique_devices)} unique devices")
            
            return unique_devices
            
        except Exception as e:
            self.logger.log(f"Scan failed: {str(e)}", level="ERROR")
            self.active_scans[scan_id]['status'] = 'failed'
            self.active_scans[scan_id]['error'] = str(e)
            return []
    
    def _arp_scan(self, interface, timeout):
        """ARP scan using scapy"""
        devices = []
        
        try:
            # Get network for interface
            if_info = self.get_network_info()
            target_interface = None
            
            for iface in if_info['interfaces']:
                if interface and iface['name'] == interface:
                    target_interface = iface
                    break
                elif not interface and iface['name'] != 'lo':
                    target_interface = iface
                    break
            
            if not target_interface or 'network' not in target_interface:
                return devices
            
            # Create ARP request
            arp_request = scapy.ARP(pdst=target_interface['network'])
            broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
            arp_request_broadcast = broadcast/arp_request
            
            # Send and receive
            answered_list = scapy.srp(
                arp_request_broadcast, 
                timeout=timeout, 
                verbose=False,
                iface=target_interface['name']
            )[0]
            
            for element in answered_list:
                device = {
                    'ip': element[1].psrc,
                    'mac': element[1].hwsrc.upper(),
                    'hostname': None,
                    'vendor': self._get_vendor_from_mac(element[1].hwsrc),
                    'last_seen': datetime.now(),
                    'detection_method': 'arp'
                }
                devices.append(device)
                
        except Exception as e:
            self.logger.log(f"ARP scan error: {str(e)}")
        
        return devices
    
    def _nmap_scan(self, interface, timeout):
        """Nmap scan"""
        devices = []
        
        try:
            # Get network for scanning
            if_info = self.get_network_info()
            target_network = None
            
            for iface in if_info['interfaces']:
                if interface and iface['name'] == interface:
                    if 'network' in iface:
                        target_network = iface['network']
                    break
                elif not interface and iface['name'] != 'lo' and 'network' in iface:
                    target_network = iface['network']
                    break
            
            if not target_network:
                return devices
            
            # Run nmap
            cmd = [
                'nmap', '-sn', '-PR', '--max-retries', '2',
                '--max-rtt-timeout', '500ms', '--max-parallelism', '100',
                '-oX', '-', target_network
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            # Parse XML output
            import xml.etree.ElementTree as ET
            root = ET.fromstring(result.stdout)
            
            for host in root.findall('host'):
                ip = host.find('address[@addrtype="ipv4"]')
                mac = host.find('address[@addrtype="mac"]')
                hostname_elem = host.find('hostnames/hostname')
                
                if ip is not None:
                    device = {
                        'ip': ip.get('addr'),
                        'mac': mac.get('addr').upper() if mac is not None else None,
                        'hostname': hostname_elem.get('name') if hostname_elem is not None else None,
                        'vendor': mac.get('vendor') if mac is not None else None,
                        'last_seen': datetime.now(),
                        'detection_method': 'nmap'
                    }
                    devices.append(device)
                    
        except subprocess.TimeoutExpired:
            self.logger.log("Nmap scan timeout")
        except Exception as e:
            self.logger.log(f"Nmap scan error: {str(e)}")
        
        return devices
    
    def _icmp_scan(self, interface, timeout):
        """ICMP ping scan"""
        devices = []
        
        try:
            # Get network range
            if_info = self.get_network_info()
            target_network = None
            
            for iface in if_info['interfaces']:
                if interface and iface['name'] == interface:
                    if 'network' in iface:
                        target_network = ipaddress.IPv4Network(iface['network'])
                    break
                elif not interface and iface['name'] != 'lo' and 'network' in iface:
                    target_network = ipaddress.IPv4Network(iface['network'])
                    break
            
            if not target_network:
                return devices
            
            # Ping each IP in parallel
            def ping_ip(ip):
                try:
                    cmd = ['ping', '-c', '1', '-W', '1', str(ip)]
                    result = subprocess.run(
                        cmd,
                        capture_output=True,
                        text=True,
                        timeout=2
                    )
                    return ip if result.returncode == 0 else None
                except:
                    return None
            
            ips = list(target_network.hosts())[:254]  # Limit to 254 hosts
            
            with ThreadPoolExecutor(max_workers=50) as executor:
                futures = {executor.submit(ping_ip, ip): ip for ip in ips}
                
                for future in as_completed(futures):
                    ip = future.result()
                    if ip:
                        device = {
                            'ip': str(ip),
                            'mac': None,
                            'hostname': None,
                            'vendor': None,
                            'last_seen': datetime.now(),
                            'detection_method': 'icmp'
                        }
                        devices.append(device)
                        
        except Exception as e:
            self.logger.log(f"ICMP scan error: {str(e)}")
        
        return devices
    
    def _enrich_device_info(self, device):
        """Get additional information for a device"""
        try:
            # Get hostname via reverse DNS
            try:
                hostname = socket.gethostbyaddr(device['ip'])[0]
                device['hostname'] = hostname
            except:
                pass
            
            # Get MAC if not present via ARP
            if not device['mac']:
                try:
                    arp_output = subprocess.check_output(
                        ['arp', '-n', device['ip']],
                        text=True
                    )
                    mac_match = re.search(r'(([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2}))', arp_output)
                    if mac_match:
                        device['mac'] = mac_match.group(1).upper()
                        device['vendor'] = self._get_vendor_from_mac(device['mac'])
                except:
                    pass
            
            # Get open ports (quick scan)
            try:
                cmd = ['nmap', '-T4', '-F', device['ip']]
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                ports = []
                for line in result.stdout.split('\n'):
                    if '/tcp' in line and 'open' in line:
                        port = line.split('/')[0]
                        ports.append(int(port))
                
                if ports:
                    device['open_ports'] = ports[:5]  # Limit to 5 ports
            except:
                pass
            
        except Exception as e:
            self.logger.log(f"Error enriching device {device['ip']}: {str(e)}")
        
        return device
    
    def _get_vendor_from_mac(self, mac):
        """Get vendor from MAC using local database"""
        from src.utils.mac_vendors import MAC_VENDORS
        
        if not mac:
            return "Unknown"
        
        # Normalize MAC
        mac = mac.upper().replace(':', '').replace('-', '')
        
        # Check prefixes (3 bytes, 2 bytes, 1 byte)
        for prefix_len in [6, 4, 2]:
            prefix = mac[:prefix_len]
            for vendor_prefix, vendor_name in MAC_VENDORS.items():
                if vendor_prefix.replace(':', '').startswith(prefix):
                    return vendor_name
        
        return "Unknown"
    
    def _remove_duplicates(self, devices):
        """Remove duplicate devices based on IP and MAC"""
        unique_devices = []
        seen_ips = set()
        seen_macs = set()
        
        for device in devices:
            ip = device.get('ip')
            mac = device.get('mac')
            
            if ip and ip not in seen_ips:
                if mac and mac in seen_macs:
                    continue
                
                unique_devices.append(device)
                seen_ips.add(ip)
                if mac:
                    seen_macs.add(mac)
        
        return unique_devices
    
    def continuous_monitoring(self, interval=300):
        """Continuous network monitoring"""
        import time
        
        self.logger.log(f"Starting continuous monitoring (interval: {interval}s)")
        
        known_devices = set()
        
        while True:
            try:
                current_devices = self.scan_network()
                current_ips = {d['ip'] for d in current_devices if d['ip']}
                
                # Detect new devices
                new_devices = current_ips - known_devices
                if new_devices:
                    new_device_list = [d for d in current_devices if d['ip'] in new_devices]
                    self.logger.log(f"New devices detected: {len(new_devices)}")
                    # Send notification
                    # self.notifier.send_new_device_alert(new_device_list)
                
                # Detect disappeared devices
                disappeared_devices = known_devices - current_ips
                if disappeared_devices:
                    self.logger.log(f"Devices disappeared: {len(disappeared_devices)}")
                
                known_devices = current_ips
                
                time.sleep(interval)
                
            except KeyboardInterrupt:
                self.logger.log("Continuous monitoring stopped")
                break
            except Exception as e:
                self.logger.log(f"Monitoring error: {str(e)}", level="ERROR")
                time.sleep(60)
