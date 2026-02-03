#!/usr/bin/env python3

import subprocess
import iptc
import json
import time
from pathlib import Path

class FirewallManager:
    def __init__(self, database):
        self.db = database
        self.logger = database.logger
        self.rules_file = Path.home() / '.config' / 'rpt-swi' / 'firewall_rules.json'
        self._ensure_iptables_chain()
    
    def _ensure_iptables_chain(self):
        """Ensure RPT-SWI chain exists in iptables"""
        try:
            # Check if chain exists
            subprocess.run(
                ['iptables', '-L', 'RPT-SWI'],
                capture_output=True,
                check=False
            )
        except:
            # Create chain
            subprocess.run(['iptables', '-N', 'RPT-SWI'], check=True)
            subprocess.run(['iptables', '-A', 'INPUT', '-j', 'RPT-SWI'], check=True)
            self.logger.log("Created RPT-SWI iptables chain")
    
    def block_device(self, device_info, permanent=True):
        """Block a device by IP and MAC"""
        ip = device_info.get('ip')
        mac = device_info.get('mac')
        
        if not ip:
            self.logger.log("Cannot block device: No IP address", level="ERROR")
            return False
        
        try:
            # Block by IP
            rule_ip = iptc.Rule()
            rule_ip.src = ip
            rule_ip.target = iptc.Target(rule_ip, "DROP")
            
            chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), "RPT-SWI")
            chain.insert_rule(rule_ip)
            
            # Block by MAC if available
            if mac:
                rule_mac = iptc.Rule()
                rule_mac.src = ip
                rule_mac.add_match('mac', {'mac-source': mac})
                rule_mac.target = iptc.Target(rule_mac, "DROP")
                chain.insert_rule(rule_mac)
            
            # Save rule
            self._save_rule({
                'type': 'block',
                'ip': ip,
                'mac': mac,
                'timestamp': time.time(),
                'permanent': permanent,
                'device_info': device_info
            })
            
            # Update device status in database
            self.db.update_device_status(ip, 'blocked')
            
            self.logger.log(f"Blocked device: {ip} ({mac or 'No MAC'})")
            
            # Send notification
            notification = {
                'type': 'device_blocked',
                'ip': ip,
                'mac': mac,
                'hostname': device_info.get('hostname'),
                'timestamp': time.time()
            }
            self.db.add_notification(notification)
            
            return True
            
        except Exception as e:
            self.logger.log(f"Failed to block device {ip}: {str(e)}", level="ERROR")
            return False
    
    def block_ip(self, ip_address, comment=""):
        """Block specific IP address"""
        try:
            rule = iptc.Rule()
            rule.src = ip_address
            rule.target = iptc.Target(rule, "DROP")
            
            chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), "RPT-SWI")
            chain.insert_rule(rule)
            
            self._save_rule({
                'type': 'block_ip',
                'ip': ip_address,
                'comment': comment,
                'timestamp': time.time()
            })
            
            self.logger.log(f"Blocked IP: {ip_address} - {comment}")
            return True
            
        except Exception as e:
            self.logger.log(f"Failed to block IP {ip_address}: {str(e)}", level="ERROR")
            return False
    
    def block_port(self, port, protocol='tcp', direction='input'):
        """Block specific port"""
        try:
            rule = iptc.Rule()
            rule.protocol = protocol
            
            match = rule.create_match(protocol)
            if protocol == 'tcp':
                match.dport = str(port)
            elif protocol == 'udp':
                match.dport = str(port)
            
            rule.target = iptc.Target(rule, "DROP")
            
            chain_name = "INPUT" if direction == 'input' else "OUTPUT"
            chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), chain_name)
            chain.insert_rule(rule)
            
            self._save_rule({
                'type': 'block_port',
                'port': port,
                'protocol': protocol,
                'direction': direction,
                'timestamp': time.time()
            })
            
            self.logger.log(f"Blocked port: {port}/{protocol} ({direction})")
            return True
            
        except Exception as e:
            self.logger.log(f"Failed to block port {port}: {str(e)}", level="ERROR")
            return False
    
    def unblock_device(self, device_info):
        """Unblock a device"""
        ip = device_info.get('ip')
        
        if not ip:
            return False
        
        try:
            # Remove all rules for this IP
            table = iptc.Table(iptc.Table.FILTER)
            chain = iptc.Chain(table, "RPT-SWI")
            
            rules_to_remove = []
            for rule in chain.rules:
                if rule.src and rule.src.split('/')[0] == ip:
                    rules_to_remove.append(rule)
            
            for rule in rules_to_remove:
                chain.delete_rule(rule)
            
            # Remove from saved rules
            self._remove_rule(ip)
            
            # Update database
            self.db.update_device_status(ip, 'allowed')
            
            self.logger.log(f"Unblocked device: {ip}")
            return True
            
        except Exception as e:
            self.logger.log(f"Failed to unblock device {ip}: {str(e)}", level="ERROR")
            return False
    
    def unblock_ip(self, ip_address):
        """Unblock specific IP"""
        try:
            table = iptc.Table(iptc.Table.FILTER)
            chain = iptc.Chain(table, "RPT-SWI")
            
            removed = False
            for rule in chain.rules:
                if rule.src and rule.src.split('/')[0] == ip_address:
                    chain.delete_rule(rule)
                    removed = True
            
            if removed:
                self._remove_rule(ip_address)
                self.logger.log(f"Unblocked IP: {ip_address}")
            
            return removed
            
        except Exception as e:
            self.logger.log(f"Failed to unblock IP {ip_address}: {str(e)}", level="ERROR")
            return False
    
    def get_blocked_devices(self):
        """Get list of all blocked devices"""
        try:
            table = iptc.Table(iptc.Table.FILTER)
            chain = iptc.Chain(table, "RPT-SWI")
            
            blocked = []
            for rule in chain.rules:
                if rule.src and rule.target.name == "DROP":
                    blocked.append({
                        'ip': rule.src.split('/')[0],
                        'target': rule.target.name
                    })
            
            return blocked
            
        except Exception as e:
            self.logger.log(f"Failed to get blocked devices: {str(e)}", level="ERROR")
            return []
    
    def get_firewall_status(self):
        """Get comprehensive firewall status"""
        status = {
            'total_rules': 0,
            'blocked_ips': 0,
            'blocked_ports': [],
            'chain_exists': False
        }
        
        try:
            # Check if chain exists
            result = subprocess.run(
                ['iptables', '-L', 'RPT-SWI', '-n'],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                status['chain_exists'] = True
                
                # Parse output
                lines = result.stdout.strip().split('\n')
                if len(lines) > 2:
                    status['total_rules'] = len(lines) - 2
                    
                    for line in lines[2:]:
                        if 'DROP' in line:
                            parts = line.split()
                            if len(parts) > 3:
                                source = parts[3]
                                if source != '0.0.0.0/0':
                                    status['blocked_ips'] += 1
            
            # Get saved rules
            saved_rules = self._load_rules()
            status['saved_rules_count'] = len(saved_rules)
            
        except Exception as e:
            self.logger.log(f"Failed to get firewall status: {str(e)}", level="ERROR")
        
        return status
    
    def backup_rules(self, backup_file=None):
        """Backup current iptables rules"""
        try:
            if not backup_file:
                backup_dir = Path.home() / '.config' / 'rpt-swi' / 'backups'
                backup_dir.mkdir(exist_ok=True)
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                backup_file = backup_dir / f"iptables_backup_{timestamp}.rules"
            
            # Save iptables rules
            with open(backup_file, 'w') as f:
                subprocess.run(['iptables-save'], stdout=f, check=True)
            
            self.logger.log(f"Firewall rules backed up to: {backup_file}")
            return str(backup_file)
            
        except Exception as e:
            self.logger.log(f"Failed to backup rules: {str(e)}", level="ERROR")
            return None
    
    def restore_rules(self, backup_file):
        """Restore iptables rules from backup"""
        try:
            if not Path(backup_file).exists():
                self.logger.log(f"Backup file not found: {backup_file}", level="ERROR")
                return False
            
            # Restore rules
            with open(backup_file, 'r') as f:
                subprocess.run(['iptables-restore'], stdin=f, check=True)
            
            self.logger.log(f"Firewall rules restored from: {backup_file}")
            return True
            
        except Exception as e:
            self.logger.log(f"Failed to restore rules: {str(e)}", level="ERROR")
            return False
    
    def _save_rule(self, rule_data):
        """Save rule to file"""
        try:
            rules = self._load_rules()
            rules.append(rule_data)
            
            with open(self.rules_file, 'w') as f:
                json.dump(rules, f, indent=2)
                
        except Exception as e:
            self.logger.log(f"Failed to save rule: {str(e)}", level="ERROR")
    
    def _load_rules(self):
        """Load rules from file"""
        try:
            if self.rules_file.exists():
                with open(self.rules_file, 'r') as f:
                    return json.load(f)
        except:
            pass
        return []
    
    def _remove_rule(self, ip_address):
        """Remove rule from file"""
        try:
            rules = self._load_rules()
            new_rules = [r for r in rules if r.get('ip') != ip_address]
            
            with open(self.rules_file, 'w') as f:
                json.dump(new_rules, f, indent=2)
                
        except Exception as e:
            self.logger.log(f"Failed to remove rule: {str(e)}", level="ERROR")
    
    def schedule_block(self, ip_address, start_time, end_time):
        """Schedule blocking for specific time period"""
        # Implementation for scheduled blocking
        pass
    
    def whitelist_device(self, device_info):
        """Add device to whitelist (never block)"""
        self.db.add_trusted_device(device_info)
        self.logger.log(f"Added to whitelist: {device_info.get('ip')}")
    
    def create_quarantine_zone(self, network):
        """Create quarantine zone for suspicious devices"""
        # Advanced feature: Isolate devices in separate network
        pass
