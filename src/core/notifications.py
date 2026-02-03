#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import smtplib
import json
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Union
import logging

class NotificationSystem:
    """سیستم ارسال اعلان‌ها"""
    
    def __init__(self, settings):
        self.settings = settings
        self.logger = logging.getLogger('rpt_swi_notifications')
        self.notifications_dir = Path.home() / '.config' / 'rpt-swi' / 'notifications'
        self.notifications_dir.mkdir(parents=True, exist_ok=True)
        
        # تاریخچه اعلان‌ها
        self.history_file = self.notifications_dir / 'history.json'
        self.history = self._load_history()
    
    def _load_history(self) -> List[Dict]:
        """بارگذاری تاریخچه اعلان‌ها"""
        try:
            if self.history_file.exists():
                with open(self.history_file, 'r') as f:
                    return json.load(f)
        except:
            pass
        return []
    
    def _save_history(self):
        """ذخیره تاریخچه اعلان‌ها"""
        try:
            # محدود کردن تعداد رکوردها
            max_history = 1000
            if len(self.history) > max_history:
                self.history = self.history[-max_history:]
            
            with open(self.history_file, 'w') as f:
                json.dump(self.history, f, indent=2, default=str)
        except Exception as e:
            self.logger.error(f"Failed to save notification history: {e}")
    
    def send_notification(self, 
                         notification_type: str,
                         message: str,
                         data: Optional[Dict] = None,
                         priority: str = 'normal') -> bool:
        """
        ارسال اعلان
        
        آرگومان‌ها:
            notification_type: نوع اعلان
            message: متن پیام
            data: داده‌های اضافی
            priority: اولویت (low, normal, high, critical)
        
        بازگشت:
            bool: موفقیت یا شکست
        """
        timestamp = datetime.now().isoformat()
        notification = {
            'type': notification_type,
            'message': message,
            'data': data or {},
            'priority': priority,
            'timestamp': timestamp,
            'sent': False,
            'channels': []
        }
        
        success = True
        
        # ارسال از طریق کانال‌های فعال
        if self.settings.notification.email_notifications:
            if self._send_email(notification):
                notification['channels'].append('email')
            else:
                success = False
        
        if self.settings.notification.telegram_notifications:
            if self._send_telegram(notification):
                notification['channels'].append('telegram')
            else:
                success = False
        
        # ذخیره در فایل
        if self.settings.notification.enabled:
            self._save_to_file(notification)
        
        # افزودن به تاریخچه
        notification['sent'] = success
        self.history.append(notification)
        self._save_history()
        
        self.logger.info(f"Notification sent: {notification_type} - {message}")
        return success
    
    def _send_email(self, notification: Dict) -> bool:
        """ارسال اعلان از طریق ایمیل"""
        if not self.settings.notification.email_config:
            return False
        
        try:
            config = self.settings.notification.email_config
            
            msg = MIMEMultipart()
            msg['From'] = config.get('smtp_user')
            msg['To'] = config.get('recipient')
            msg['Subject'] = f"RPT SWI Alert: {notification['type'].upper()}"
            
            # ساخت body
            body = f"""
RPT See Who Is In - Security Notification
=========================================

Type: {notification['type']}
Priority: {notification['priority'].upper()}
Time: {notification['timestamp']}

Message:
{notification['message']}

"""
            
            # اضافه کردن داده‌های اضافی
            if notification['data']:
                body += "\nAdditional Data:\n"
                for key, value in notification['data'].items():
                    body += f"  {key}: {value}\n"
            
            msg.attach(MIMEText(body, 'plain'))
            
            # اتصال به سرور SMTP
            with smtplib.SMTP(config.get('smtp_server'), 
                            config.get('smtp_port', 587)) as server:
                server.starttls()
                server.login(config.get('smtp_user'), 
                           config.get('smtp_password'))
                server.send_message(msg)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to send email: {e}")
            return False
    
    def _send_telegram(self, notification: Dict) -> bool:
        """ارسال اعلان از طریق تلگرام"""
        if not self.settings.notification.telegram_config:
            return False
        
        try:
            config = self.settings.notification.telegram_config
            bot_token = config.get('bot_token')
            chat_id = config.get('chat_id')
            
            if not bot_token or not chat_id:
                return False
            
            # ساخت متن پیام
            emoji = {
                'low': '📊',
                'normal': 'ℹ️',
                'high': '⚠️',
                'critical': '🚨'
            }.get(notification['priority'], '📨')
            
            message = f"{emoji} *RPT SWI Alert*\n\n"
            message += f"*Type:* {notification['type']}\n"
            message += f"*Priority:* {notification['priority'].upper()}\n"
            message += f"*Time:* {notification['timestamp']}\n\n"
            message += f"*Message:*\n{notification['message']}\n"
            
            # اضافه کردن داده‌های اضافی
            if notification['data']:
                message += "\n*Additional Data:*\n"
                for key, value in notification['data'].items():
                    message += f"  • *{key}:* {value}\n"
            
            # ارسال درخواست به API تلگرام
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            payload = {
                'chat_id': chat_id,
                'text': message,
                'parse_mode': 'Markdown'
            }
            
            response = requests.post(url, json=payload, timeout=10)
            return response.status_code == 200
            
        except Exception as e:
            self.logger.error(f"Failed to send Telegram message: {e}")
            return False
    
    def _save_to_file(self, notification: Dict):
        """ذخیره اعلان در فایل"""
        try:
            # فایل مخصوص هر روز
            date_str = datetime.now().strftime('%Y-%m-%d')
            log_file = self.notifications_dir / f"notifications_{date_str}.log"
            
            with open(log_file, 'a') as f:
                f.write(f"[{notification['timestamp']}] ")
                f.write(f"[{notification['priority'].upper()}] ")
                f.write(f"[{notification['type']}] ")
                f.write(f"{notification['message']}\n")
                
                if notification['data']:
                    f.write(f"Data: {json.dumps(notification['data'], default=str)}\n")
                
                f.write("-" * 80 + "\n")
                
        except Exception as e:
            self.logger.error(f"Failed to save notification to file: {e}")
    
    def send_new_device_alert(self, devices: List[Dict]):
        """ارسال اعلان برای دستگاه‌های جدید"""
        if not self.settings.notification.new_device_alert:
            return
        
        device_list = "\n".join([
            f"  • {d.get('ip', 'Unknown')} ({d.get('mac', 'Unknown')}) - {d.get('vendor', 'Unknown')}"
            for d in devices[:10]  # محدود کردن تعداد
        ])
        
        if len(devices) > 10:
            device_list += f"\n  • ... and {len(devices) - 10} more devices"
        
        message = f"New devices detected on network:\n{device_list}"
        
        self.send_notification(
            notification_type='new_device',
            message=message,
            data={'device_count': len(devices)},
            priority='high' if len(devices) > 5 else 'normal'
        )
    
    def send_block_alert(self, device: Dict, action: str = 'blocked'):
        """ارسال اعلان برای مسدودسازی دستگاه"""
        if not self.settings.notification.block_alert:
            return
        
        message = f"Device {action}: {device.get('ip', 'Unknown')} ({device.get('mac', 'Unknown')})"
        
        self.send_notification(
            notification_type=f'device_{action}',
            message=message,
            data={
                'ip': device.get('ip'),
                'mac': device.get('mac'),
                'hostname': device.get('hostname'),
                'vendor': device.get('vendor'),
                'action': action
            },
            priority='high'
        )
    
    def send_scan_complete_alert(self, scan_result: Dict):
        """ارسال اعلان برای اتمام اسکن"""
        if not self.settings.notification.scan_complete_alert:
            return
        
        message = f"Network scan completed: Found {scan_result.get('device_count', 0)} devices"
        
        self.send_notification(
            notification_type='scan_complete',
            message=message,
            data=scan_result,
            priority='low'
        )
    
    def send_security_alert(self, alert_type: str, details: Dict):
        """ارسال اعلان امنیتی"""
        message = f"Security alert: {alert_type}"
        
        self.send_notification(
            notification_type='security_alert',
            message=message,
            data=details,
            priority='critical'
        )
    
    def get_notification_history(self, 
                                limit: int = 50,
                                notification_type: Optional[str] = None) -> List[Dict]:
        """دریافت تاریخچه اعلان‌ها"""
        filtered = self.history
        
        if notification_type:
            filtered = [n for n in filtered if n['type'] == notification_type]
        
        return filtered[-limit:] if limit > 0 else filtered
    
    def clear_notification_history(self, older_than_days: int = 30):
        """پاک کردن تاریخچه اعلان‌های قدیمی"""
        try:
            cutoff_date = datetime.now().timestamp() - (older_than_days * 86400)
            
            new_history = []
            for notification in self.history:
                try:
                    timestamp = datetime.fromisoformat(notification['timestamp']).timestamp()
                    if timestamp > cutoff_date:
                        new_history.append(notification)
                except:
                    pass
            
            self.history = new_history
            self._save_history()
            
            # حذف فایل‌های log قدیمی
            for log_file in self.notifications_dir.glob('notifications_*.log'):
                try:
                    file_date = datetime.strptime(log_file.stem[14:], '%Y-%m-%d')
                    if (datetime.now() - file_date).days > older_than_days:
                        log_file.unlink()
                except:
                    pass
            
            self.logger.info(f"Cleared notifications older than {older_than_days} days")
            
        except Exception as e:
            self.logger.error(f"Failed to clear notification history: {e}")
