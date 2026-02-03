#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import platform
import logging
from pathlib import Path
from datetime import datetime
import hashlib
import json
import ipaddress

def check_root():
    """بررسی دسترسی root"""
    return os.geteuid() == 0

def check_dependencies(tools):
    """بررسی نصب بودن ابزارهای مورد نیاز"""
    missing = []
    for tool in tools:
        try:
            subprocess.run(['which', tool], 
                         capture_output=True, 
                         check=True)
        except subprocess.CalledProcessError:
            missing.append(tool)
    return missing

def setup_logger(name, level=logging.INFO):
    """تنظیم logger"""
    logger = logging.getLogger(name)
    
    if logger.hasHandlers():
        return logger
    
    logger.setLevel(level)
    
    # فرمت log
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Handler برای console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Handler برای فایل
    log_dir = Path.home() / '.config' / 'rpt-swi' / 'logs'
    log_dir.mkdir(parents=True, exist_ok=True)
    
    log_file = log_dir / f'{name}.log'
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger

def validate_ip(ip_str):
    """اعتبارسنجی آدرس IP"""
    try:
        ipaddress.ip_address(ip_str)
        return True
    except ValueError:
        return False

def validate_mac(mac_str):
    """اعتبارسنجی آدرس MAC"""
    import re
    mac_pattern = r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$'
    return re.match(mac_pattern, mac_str) is not None

def get_system_info():
    """دریافت اطلاعات سیستم"""
    info = {
        'platform': platform.system(),
        'release': platform.release(),
        'version': platform.version(),
        'machine': platform.machine(),
        'processor': platform.processor(),
        'python_version': platform.python_version()
    }
    return info

def calculate_hash(data, algorithm='sha256'):
    """محاسبه هش داده‌ها"""
    if isinstance(data, str):
        data = data.encode()
    
    if algorithm == 'md5':
        return hashlib.md5(data).hexdigest()
    elif algorithm == 'sha1':
        return hashlib.sha1(data).hexdigest()
    elif algorithm == 'sha256':
        return hashlib.sha256(data).hexdigest()
    else:
        raise ValueError(f"Unsupported algorithm: {algorithm}")

def format_bytes(size):
    """فرمت کردن حجم فایل"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} PB"

def human_readable_time(seconds):
    """تبدیل زمان به فرمت قابل خواندن"""
    if seconds < 60:
        return f"{seconds:.1f} seconds"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f} minutes"
    elif seconds < 86400:
        hours = seconds / 3600
        return f"{hours:.1f} hours"
    else:
        days = seconds / 86400
        return f"{days:.1f} days"

def progress_bar(iteration, total, prefix='', suffix='', length=50, fill='█'):
    """نمایش نوار پیشرفت"""
    percent = f"{100 * (iteration / float(total)):.1f}"
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end='\r')
    
    if iteration == total:
        print()

def confirm_action(message, default=False):
    """درخواست تایید از کاربر"""
    suffix = " (Y/n)" if default else " (y/N)"
    response = input(f"{message}{suffix}: ").strip().lower()
    
    if response == '':
        return default
    elif response in ['y', 'yes']:
        return True
    elif response in ['n', 'no']:
        return False
    else:
        print("Invalid response. Please answer with 'y' or 'n'")
        return confirm_action(message, default)

def get_terminal_size():
    """دریافت اندازه ترمینال"""
    try:
        rows, columns = os.popen('stty size', 'r').read().split()
        return int(rows), int(columns)
    except:
        return 24, 80

def clear_screen():
    """پاک کردن صفحه نمایش"""
    os.system('clear' if os.name == 'posix' else 'cls')

def print_color(text, color='white', bg_color=None, style=None):
    """چاپ متن رنگی"""
    colors = {
        'black': '\033[30m',
        'red': '\033[31m',
        'green': '\033[32m',
        'yellow': '\033[33m',
        'blue': '\033[34m',
        'magenta': '\033[35m',
        'cyan': '\033[36m',
        'white': '\033[37m',
        'reset': '\033[0m'
    }
    
    bg_colors = {
        'black': '\033[40m',
        'red': '\033[41m',
        'green': '\033[42m',
        'yellow': '\033[43m',
        'blue': '\033[44m',
        'magenta': '\033[45m',
        'cyan': '\033[46m',
        'white': '\033[47m'
    }
    
    styles = {
        'bold': '\033[1m',
        'underline': '\033[4m',
        'reversed': '\033[7m'
    }
    
    output = ''
    
    if style and style in styles:
        output += styles[style]
    
    if bg_color and bg_color in bg_colors:
        output += bg_colors[bg_color]
    
    if color in colors:
        output += colors[color]
    
    output += text + colors['reset']
    print(output)

def read_json_file(file_path):
    """خواندن فایل JSON"""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        return None

def write_json_file(file_path, data, indent=2):
    """نوشتن در فایل JSON"""
    try:
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=indent, default=str)
        return True
    except Exception as e:
        print(f"Error writing JSON file: {e}")
        return False

def safe_execute(func, *args, **kwargs):
    """اجرای ایمن یک تابع با مدیریت خطا"""
    try:
        return func(*args, **kwargs)
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.error(f"Error in {func.__name__}: {e}")
        return None
