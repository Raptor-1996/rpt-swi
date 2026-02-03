#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from colorama import init, Fore, Back, Style
import sys

# Initialize colorama
init(autoreset=True)

class Colors:
    """کلاس مدیریت رنگ‌های ترمینال"""
    
    # رنگ‌های متن
    BLACK = Fore.BLACK
    RED = Fore.RED
    GREEN = Fore.GREEN
    YELLOW = Fore.YELLOW
    BLUE = Fore.BLUE
    MAGENTA = Fore.MAGENTA
    CYAN = Fore.CYAN
    WHITE = Fore.WHITE
    RESET = Fore.RESET
    
    # رنگ‌های پس‌زمینه
    BG_BLACK = Back.BLACK
    BG_RED = Back.RED
    BG_GREEN = Back.GREEN
    BG_YELLOW = Back.YELLOW
    BG_BLUE = Back.BLUE
    BG_MAGENTA = Back.MAGENTA
    BG_CYAN = Back.CYAN
    BG_WHITE = Back.WHITE
    BG_RESET = Back.RESET
    
    # استایل‌ها
    BRIGHT = Style.BRIGHT
    DIM = Style.DIM
    NORMAL = Style.NORMAL
    RESET_ALL = Style.RESET_ALL
    
    # رنگ‌های مخصوص برنامه
    HEADER = CYAN + BRIGHT
    SUCCESS = GREEN + BRIGHT
    WARNING = YELLOW + BRIGHT
    ERROR = RED + BRIGHT
    INFO = BLUE + BRIGHT
    HIGHLIGHT = MAGENTA + BRIGHT
    DEBUG = DIM + WHITE
    
    @staticmethod
    def colorize(text: str, color: str) -> str:
        """رنگی کردن متن"""
        return f"{color}{text}{Colors.RESET_ALL}"
    
    @staticmethod
    def print_color(text: str, color: str, **kwargs):
        """چاپ متن رنگی"""
        print(f"{color}{text}{Colors.RESET_ALL}", **kwargs)
    
    @staticmethod
    def print_header(text: str):
        """چاپ هدر"""
        width = min(80, Colors.get_terminal_width() - 4)
        line = "=" * width
        print(f"\n{Colors.HEADER}{line}")
        print(f"{text.center(width)}")
        print(f"{line}{Colors.RESET_ALL}\n")
    
    @staticmethod
    def print_success(text: str):
        """چاپ پیام موفقیت"""
        print(f"{Colors.SUCCESS}✓ {text}{Colors.RESET_ALL}")
    
    @staticmethod
    def print_error(text: str):
        """چاپ پیام خطا"""
        print(f"{Colors.ERROR}✗ {text}{Colors.RESET_ALL}")
    
    @staticmethod
    def print_warning(text: str):
        """چاپ پیام هشدار"""
        print(f"{Colors.WARNING}⚠ {text}{Colors.RESET_ALL}")
    
    @staticmethod
    def print_info(text: str):
        """چاپ پیام اطلاعاتی"""
        print(f"{Colors.INFO}ℹ {text}{Colors.RESET_ALL}")
    
    @staticmethod
    def print_debug(text: str):
        """چاپ پیام دیباگ"""
        print(f"{Colors.DEBUG}🐛 {text}{Colors.RESET_ALL}")
    
    @staticmethod
    def print_table(headers: list, rows: list, color: str = None):
        """چاپ جدول رنگی"""
        from tabulate import tabulate
        
        if color:
            colored_headers = [Colors.colorize(h, color) for h in headers]
            colored_rows = []
            for row in rows:
                colored_row = [Colors.colorize(str(cell), color) if i == 0 else str(cell) 
                              for i, cell in enumerate(row)]
                colored_rows.append(colored_row)
            
            print(tabulate(colored_rows, headers=colored_headers, tablefmt="grid"))
        else:
            print(tabulate(rows, headers=headers, tablefmt="grid"))
    
    @staticmethod
    def get_terminal_width() -> int:
        """دریافت عرض ترمینال"""
        try:
            return os.get_terminal_size().columns
        except:
            return 80
    
    @staticmethod
    def get_terminal_height() -> int:
        """دریافت ارتفاع ترمینال"""
        try:
            return os.get_terminal_size().rows
        except:
            return 24
    
    @staticmethod
    def gradient(text: str, start_color: tuple, end_color: tuple) -> str:
        """ایجاد گرادیان روی متن"""
        import math
        
        if len(text) == 0:
            return text
        
        # تبدیل RGB به کد رنگ ترمینال
        def rgb_to_term(r, g, b):
            return f"\033[38;2;{r};{g};{b}m"
        
        result = []
        length = len(text)
        
        for i, char in enumerate(text):
            # محاسبه رنگ میانی
            ratio = i / max(1, length - 1)
            r = int(start_color[0] + (end_color[0] - start_color[0]) * ratio)
            g = int(start_color[1] + (end_color[1] - start_color[1]) * ratio)
            b = int(start_color[2] + (end_color[2] - start_color[2]) * ratio)
            
            # اضافه کردن کاراکتر با رنگ
            result.append(f"{rgb_to_term(r, g, b)}{char}")
        
        result.append(Colors.RESET_ALL)
        return ''.join(result)
    
    @staticmethod
    def print_banner():
        """چاپ بنر برنامه"""
        banner = f"""
{Colors.HEADER}
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║   {Colors.gradient("RPT See Who Is In", (0, 200, 255), (0, 100, 255))}                               ║
║   {Colors.gradient("Professional Network Security Tool", (100, 200, 255), (50, 150, 255))}           ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
{Colors.RESET_ALL}
        """
        print(banner)
    
    @staticmethod
    def print_status(status: str, message: str):
        """چاپ وضعیت"""
        status_colors = {
            'running': Colors.GREEN,
            'stopped': Colors.RED,
            'warning': Colors.YELLOW,
            'error': Colors.RED + Style.BRIGHT,
            'info': Colors.BLUE,
            'success': Colors.GREEN + Style.BRIGHT
        }
        
        color = status_colors.get(status.lower(), Colors.WHITE)
        print(f"{color}[{status.upper():^8}]{Colors.RESET_ALL} {message}")

# Alias برای راحتی استفاده
C = Colors
