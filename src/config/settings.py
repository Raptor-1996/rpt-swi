#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import yaml
import os
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any

@dataclass
class DatabaseConfig:
    """تنظیمات پایگاه داده"""
    path: str = str(Path.home() / '.config' / 'rpt-swi' / 'devices.db')
    backup_interval: int = 24  # ساعت
    cleanup_days: int = 30
    max_history: int = 1000

@dataclass
class ScannerConfig:
    """تنظیمات اسکنر"""
    default_timeout: int = 30  # ثانیه
    max_threads: int = 50
    arp_timeout: int = 5
    nmap_timeout: int = 15
    ping_timeout: int = 2
    retry_count: int = 2

@dataclass
class FirewallConfig:
    """تنظیمات فایروال"""
    chain_name: str = "RPT-SWI"
    backup_on_change: bool = True
    auto_save_rules: bool = True
    default_action: str = "DROP"
    logging_enabled: bool = True

@dataclass
class NotificationConfig:
    """تنظیمات اعلان‌ها"""
    enabled: bool = True
    new_device_alert: bool = True
    block_alert: bool = True
    scan_complete_alert: bool = False
    email_notifications: bool = False
    telegram_notifications: bool = False
    email_config: Dict[str, str] = field(default_factory=dict)
    telegram_config: Dict[str, str] = field(default_factory=dict)

@dataclass
class UIConfig:
    """تنظیمات رابط کاربری"""
    color_enabled: bool = True
    auto_refresh: int = 10  # ثانیه
    show_progress: bool = True
    detailed_output: bool = True
    default_view: str = "table"

@dataclass
class MonitoringConfig:
    """تنظیمات مانیتورینگ"""
    enabled: bool = False
    interval: int = 300  # ثانیه
    alert_on_new: bool = True
    alert_on_disappear: bool = False
    auto_block_suspicious: bool = False
    suspicious_threshold: int = 3

@dataclass
class SecurityConfig:
    """تنظیمات امنیتی"""
    require_password: bool = True
    password_hash: Optional[str] = None
    session_timeout: int = 1800  # ثانیه
    max_login_attempts: int = 3
    log_rotation: int = 7  # روز

@dataclass
class Settings:
    """کلاس اصلی تنظیمات"""
    
    def __init__(self, config_file=None):
        if not config_file:
            config_dir = Path.home() / '.config' / 'rpt-swi'
            config_dir.mkdir(parents=True, exist_ok=True)
            config_file = config_dir / 'settings.yaml'
        
        self.config_file = Path(config_file)
        self.db = DatabaseConfig()
        self.scanner = ScannerConfig()
        self.firewall = FirewallConfig()
        self.notification = NotificationConfig()
        self.ui = UIConfig()
        self.monitoring = MonitoringConfig()
        self.security = SecurityConfig()
        
        # بارگذاری تنظیمات از فایل اگر وجود دارد
        self.load()
        
        # ذخیره تنظیمات پیش‌فرض اگر فایل وجود نداشت
        if not self.config_file.exists():
            self.save()
    
    def load(self):
        """بارگذاری تنظیمات از فایل YAML"""
        if not self.config_file.exists():
            return
        
        try:
            with open(self.config_file, 'r') as f:
                data = yaml.safe_load(f) or {}
            
            # بارگذاری تنظیمات هر بخش
            if 'database' in data:
                self.db.__dict__.update(data['database'])
            
            if 'scanner' in data:
                self.scanner.__dict__.update(data['scanner'])
            
            if 'firewall' in data:
                self.firewall.__dict__.update(data['firewall'])
            
            if 'notification' in data:
                self.notification.__dict__.update(data['notification'])
            
            if 'ui' in data:
                self.ui.__dict__.update(data['ui'])
            
            if 'monitoring' in data:
                self.monitoring.__dict__.update(data['monitoring'])
            
            if 'security' in data:
                self.security.__dict__.update(data['security'])
                
        except Exception as e:
            print(f"Warning: Could not load settings: {e}")
    
    def save(self):
        """ذخیره تنظیمات در فایل YAML"""
        try:
            data = {
                'database': self.db.__dict__,
                'scanner': self.scanner.__dict__,
                'firewall': self.firewall.__dict__,
                'notification': self.notification.__dict__,
                'ui': self.ui.__dict__,
                'monitoring': self.monitoring.__dict__,
                'security': self.security.__dict__
            }
            
            with open(self.config_file, 'w') as f:
                yaml.dump(data, f, default_flow_style=False, indent=2)
                
        except Exception as e:
            print(f"Error saving settings: {e}")
    
    def update(self, section: str, key: str, value: Any):
        """به‌روزرسانی یک تنظیم خاص"""
        try:
            if hasattr(self, section):
                section_obj = getattr(self, section)
                if hasattr(section_obj, key):
                    setattr(section_obj, key, value)
                    self.save()
                    return True
            return False
        except Exception as e:
            print(f"Error updating setting: {e}")
            return False
    
    def get(self, section: str, key: str, default=None):
        """دریافت یک تنظیم خاص"""
        try:
            if hasattr(self, section):
                section_obj = getattr(self, section)
                return getattr(section_obj, key, default)
            return default
        except:
            return default
    
    def to_dict(self):
        """تبدیل تنظیمات به دیکشنری"""
        return {
            'database': self.db.__dict__,
            'scanner': self.scanner.__dict__,
            'firewall': self.firewall.__dict__,
            'notification': self.notification.__dict__,
            'ui': self.ui.__dict__,
            'monitoring': self.monitoring.__dict__,
            'security': self.security.__dict__
        }
    
    def validate(self):
        """اعتبارسنجی تنظیمات"""
        errors = []
        
        # اعتبارسنجی تنظیمات پایگاه داده
        if self.db.backup_interval < 1:
            errors.append("Backup interval must be at least 1 hour")
        
        # اعتبارسنجی تنظیمات اسکنر
        if self.scanner.default_timeout < 5:
            errors.append("Scanner timeout must be at least 5 seconds")
        if self.scanner.max_threads < 1 or self.scanner.max_threads > 100:
            errors.append("Max threads must be between 1 and 100")
        
        # اعتبارسنجی تنظیمات مانیتورینگ
        if self.monitoring.interval < 60:
            errors.append("Monitoring interval must be at least 60 seconds")
        
        return errors
