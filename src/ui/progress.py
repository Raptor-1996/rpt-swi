#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import time
import threading
from typing import Optional, Callable
from colorama import Fore, Style

class ProgressBar:
    """کلاس نمایش نوار پیشرفت"""
    
    def __init__(self, 
                 total: int = 100,
                 prefix: str = 'Progress',
                 suffix: str = 'Complete',
                 length: int = 50,
                 fill: str = '█',
                 color: str = 'green'):
        """
        آرگومان‌ها:
            total: مقدار کل
            prefix: متن قبل از نوار
            suffix: متن بعد از نوار
            length: طول نوار
            fill: کاراکتر پرکننده
            color: رنگ نوار
        """
        self.total = total
        self.prefix = prefix
        self.suffix = suffix
        self.length = length
        self.fill = fill
        self.color = color
        self.current = 0
        self.start_time = None
        self.running = False
        self.thread = None
        
        # رنگ‌ها
        self.colors = {
            'red': Fore.RED,
            'green': Fore.GREEN,
            'yellow': Fore.YELLOW,
            'blue': Fore.BLUE,
            'magenta': Fore.MAGENTA,
            'cyan': Fore.CYAN,
            'white': Fore.WHITE
        }
    
    def start(self):
        """شروع نمایش نوار پیشرفت"""
        self.start_time = time.time()
        self.running = True
        self.thread = threading.Thread(target=self._animate)
        self.thread.daemon = True
        self.thread.start()
    
    def update(self, value: int):
        """به‌روزرسانی مقدار فعلی"""
        self.current = min(value, self.total)
    
    def increment(self, amount: int = 1):
        """افزایش مقدار فعلی"""
        self.current = min(self.current + amount, self.total)
    
    def finish(self):
        """پایان نمایش نوار پیشرفت"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=1)
        self.current = self.total
        self._print_bar()
        print()
    
    def _animate(self):
        """انیمیشن نوار پیشرفت"""
        while self.running and self.current < self.total:
            self._print_bar()
            time.sleep(0.1)
    
    def _print_bar(self):
        """چاپ نوار پیشرفت"""
        percent = f"{100 * (self.current / float(self.total)):.1f}"
        filled_length = int(self.length * self.current // self.total)
        bar = self.fill * filled_length + '-' * (self.length - filled_length)
        
        # محاسبه زمان باقی‌مانده
        if self.current > 0:
            elapsed = time.time() - self.start_time
            eta = (elapsed / self.current) * (self.total - self.current)
            time_str = f"ETA: {self._format_time(eta)}"
        else:
            time_str = "ETA: Calculating..."
        
        # انتخاب رنگ
        color_code = self.colors.get(self.color, Fore.GREEN)
        
        # چاپ نوار
        bar_str = f'\r{self.prefix} |{color_code}{bar}{Style.RESET_ALL}| {percent}% | {self.suffix} | {time_str}'
        sys.stdout.write(bar_str)
        sys.stdout.flush()
    
    def _format_time(self, seconds: float) -> str:
        """فرمت‌دهی زمان"""
        if seconds < 60:
            return f"{seconds:.0f}s"
        elif seconds < 3600:
            minutes = seconds / 60
            return f"{minutes:.0f}m {seconds%60:.0f}s"
        else:
            hours = seconds / 3600
            minutes = (seconds % 3600) / 60
            return f"{hours:.0f}h {minutes:.0f}m"

class Spinner:
    """کلاس نمایش اسپینر"""
    
    def __init__(self, message: str = "Loading", delay: float = 0.1):
        self.message = message
        self.delay = delay
        self.spinner_chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        self.running = False
        self.thread = None
    
    def start(self):
        """شروع اسپینر"""
        self.running = True
        self.thread = threading.Thread(target=self._spin)
        self.thread.daemon = True
        self.thread.start()
    
    def stop(self):
        """توقف اسپینر"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=0.5)
        sys.stdout.write('\r' + ' ' * (len(self.message) + 10) + '\r')
        sys.stdout.flush()
    
    def _spin(self):
        """انیمیشن اسپینر"""
        i = 0
        while self.running:
            sys.stdout.write(f'\r{self.message} {self.spinner_chars[i]} ')
            sys.stdout.flush()
            time.sleep(self.delay)
            i = (i + 1) % len(self.spinner_chars)

class MultiProgress:
    """کلاس نمایش چندین نوار پیشرفت همزمان"""
    
    def __init__(self):
        self.bars = {}
        self.lock = threading.Lock()
    
    def add_bar(self, name: str, total: int, **kwargs):
        """افزودن نوار پیشرفت جدید"""
        with self.lock:
            self.bars[name] = {
                'bar': ProgressBar(total, **kwargs),
                'current': 0,
                'total': total
            }
    
    def update(self, name: str, value: int):
        """به‌روزرسانی نوار خاص"""
        with self.lock:
            if name in self.bars:
                self.bars[name]['current'] = value
                self._render()
    
    def increment(self, name: str, amount: int = 1):
        """افزایش نوار خاص"""
        with self.lock:
            if name in self.bars:
                self.bars[name]['current'] += amount
                self._render()
    
    def finish(self, name: str):
        """پایان نوار خاص"""
        with self.lock:
            if name in self.bars:
                self.bars[name]['current'] = self.bars[name]['total']
                self._render()
                del self.bars[name]
    
    def _render(self):
        """رندر همه نوارها"""
        sys.stdout.write('\033[2J\033[H')  # پاک کردن صفحه
        print("RPT SWI - Progress Monitor\n")
        
        for name, data in self.bars.items():
            bar = data['bar']
            current = data['current']
            total = data['total']
            
            percent = 100 * (current / float(total))
            filled_length = int(bar.length * current // total)
            progress_bar = bar.fill * filled_length + '-' * (bar.length - filled_length)
            
            color_code = bar.colors.get(bar.color, Fore.GREEN)
            
            print(f"{name}:")
            print(f"  [{color_code}{progress_bar}{Style.RESET_ALL}] {percent:.1f}% ({current}/{total})")
            print()

def show_progress(message: str, func: Callable, *args, **kwargs):
    """نمایش پیشرفت برای یک تابع"""
    spinner = Spinner(message)
    spinner.start()
    
    try:
        result = func(*args, **kwargs)
        spinner.stop()
        print(f"\r{message} ✓")
        return result
    except Exception as e:
        spinner.stop()
        print(f"\r{message} ✗ Error: {e}")
        raise
