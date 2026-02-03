#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
import threading

class DeviceDatabase:
    def __init__(self, db_path=None):
        if not db_path:
            config_dir = Path.home() / '.config' / 'rpt-swi'
            config_dir.mkdir(parents=True, exist_ok=True)
            db_path = config_dir / 'devices.db'
        
        self.db_path = db_path
        self.lock = threading.Lock()
        
        # Setup logger
        self.logger = logging.getLogger('rpt_swi_db')
        if not self.logger.handlers:
            self.logger.setLevel(logging.INFO)
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        
        self._init_database()
    
    def log(self, message, level='info'):
        """Log a message"""
        if level == 'info':
            self.logger.info(message)
        elif level == 'error':
            self.logger.error(message)
        elif level == 'warning':
            self.logger.warning(message)
        elif level == 'debug':
            self.logger.debug(message)
    
    def _init_database(self):
        """Initialize database tables"""
        with self.lock:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Devices table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS devices (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ip TEXT UNIQUE NOT NULL,
                    mac TEXT,
                    hostname TEXT,
                    vendor TEXT,
                    first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status TEXT DEFAULT 'unknown',
                    trusted BOOLEAN DEFAULT 0
                )
            ''')
            
            # Network scans table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS scans (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    scan_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    devices_found INTEGER,
                    duration_seconds REAL
                )
            ''')
            
            # Create indexes
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_devices_ip ON devices(ip)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_devices_mac ON devices(mac)')
            
            conn.commit()
            conn.close()
            
            self.log("Database initialized", "info")
    
    def add_or_update_device(self, device_info):
        """Add or update device information"""
        with self.lock:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Check if device exists
            cursor.execute('SELECT id FROM devices WHERE ip = ?', (device_info['ip'],))
            existing = cursor.fetchone()
            
            if existing:
                # Update existing device
                cursor.execute('''
                    UPDATE devices SET
                        mac = COALESCE(?, mac),
                        hostname = COALESCE(?, hostname),
                        vendor = COALESCE(?, vendor),
                        last_seen = ?
                    WHERE ip = ?
                ''', (
                    device_info.get('mac'),
                    device_info.get('hostname'),
                    device_info.get('vendor'),
                    datetime.now(),
                    device_info['ip']
                ))
            else:
                # Insert new device
                cursor.execute('''
                    INSERT INTO devices 
                    (ip, mac, hostname, vendor, first_seen, last_seen)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    device_info['ip'],
                    device_info.get('mac'),
                    device_info.get('hostname'),
                    device_info.get('vendor'),
                    datetime.now(),
                    datetime.now()
                ))
            
            conn.commit()
            conn.close()
            
            self.log(f"Device {'updated' if existing else 'added'}: {device_info['ip']}", "info")
    
    def get_all_devices(self):
        """Get all devices"""
        with self.lock:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM devices ORDER BY last_seen DESC')
            columns = [desc[0] for desc in cursor.description]
            devices = [dict(zip(columns, row)) for row in cursor.fetchall()]
            
            conn.close()
            return devices
    
    def update_device_status(self, ip, status):
        """Update device status"""
        with self.lock:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                'UPDATE devices SET status = ? WHERE ip = ?',
                (status, ip)
            )
            
            conn.commit()
            conn.close()
            
            self.log(f"Updated device status: {ip} -> {status}", "info")
    
    def close(self):
        """Close database connection"""
        self.log("Database connection closed", "info")
