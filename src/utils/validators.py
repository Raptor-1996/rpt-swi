#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import ipaddress
import socket
from typing import Union, Tuple, Optional

class NetworkValidators:
    """کلاس اعتبارسنجی شبکه"""
    
    @staticmethod
    def validate_ip(ip_str: str) -> bool:
        """اعتبارسنجی آدرس IPv4 یا IPv6"""
        try:
            ipaddress.ip_address(ip_str)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def validate_ipv4(ip_str: str) -> bool:
        """اعتبارسنجی آدرس IPv4"""
        try:
            ipaddress.IPv4Address(ip_str)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def validate_ipv6(ip_str: str) -> bool:
        """اعتبارسنجی آدرس IPv6"""
        try:
            ipaddress.IPv6Address(ip_str)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def validate_cidr(cidr_str: str) -> bool:
        """اعتبارسنجی CIDR notation"""
        try:
            ipaddress.ip_network(cidr_str, strict=False)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def validate_mac(mac_str: str) -> bool:
        """اعتبارسنجی آدرس MAC"""
        mac_patterns = [
            r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$',
            r'^([0-9A-Fa-f]{4}\.){2}([0-9A-Fa-f]{4})$',
            r'^([0-9A-Fa-f]{12})$'
        ]
        
        for pattern in mac_patterns:
            if re.match(pattern, mac_str):
                return True
        return False
    
    @staticmethod
    def validate_port(port: Union[int, str]) -> Tuple[bool, Optional[str]]:
        """اعتبارسنجی پورت"""
        try:
            port_num = int(port)
            if 0 <= port_num <= 65535:
                return True, None
            else:
                return False, "Port must be between 0 and 65535"
        except ValueError:
            return False, "Port must be a number"
    
    @staticmethod
    def validate_hostname(hostname: str) -> bool:
        """اعتبارسنجی نام هاست"""
        if len(hostname) > 255:
            return False
        
        if hostname[-1] == ".":
            hostname = hostname[:-1]
        
        allowed = re.compile(r"(?!-)[A-Z\d\-]{1,63}(?<!-)$", re.IGNORECASE)
        return all(allowed.match(x) for x in hostname.split("."))
    
    @staticmethod
    def validate_url(url: str) -> bool:
        """اعتبارسنجی URL"""
        regex = re.compile(
            r'^(?:http|ftp)s?://'  # پروتکل
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+'
            r'(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # دامنه
            r'localhost|'  # localhost
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # IP
            r'(?::\d+)?'  # پورت
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        
        return re.match(regex, url) is not None
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """اعتبارسنجی ایمیل"""
        regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(regex, email) is not None
    
    @staticmethod
    def validate_subnet_mask(mask: str) -> bool:
        """اعتبارسنجی subnet mask"""
        try:
            # تبدیل به عدد
            octets = mask.split('.')
            if len(octets) != 4:
                return False
            
            # بررسی هر octet
            binary_mask = ''
            for octet in octets:
                num = int(octet)
                if num < 0 or num > 255:
                    return False
                binary_mask += bin(num)[2:].zfill(8)
            
            # بررسی اینکه فقط 1های پشت سر هم و بعد 0ها باشند
            found_zero = False
            for bit in binary_mask:
                if bit == '0':
                    found_zero = True
                elif found_zero and bit == '1':
                    return False
            
            return True
        except (ValueError, AttributeError):
            return False
    
    @staticmethod
    def is_private_ip(ip_str: str) -> bool:
        """بررسی اینکه IP خصوصی است یا نه"""
        try:
            ip = ipaddress.ip_address(ip_str)
            return ip.is_private
        except ValueError:
            return False
    
    @staticmethod
    def is_reserved_ip(ip_str: str) -> bool:
        """بررسی اینکه IP رزرو شده است"""
        try:
            ip = ipaddress.ip_address(ip_str)
            return ip.is_reserved
        except ValueError:
            return False
    
    @staticmethod
    def is_multicast_ip(ip_str: str) -> bool:
        """بررسی اینکه IP مالتی‌کست است"""
        try:
            ip = ipaddress.ip_address(ip_str)
            return ip.is_multicast
        except ValueError:
            return False
    
    @staticmethod
    def get_ip_version(ip_str: str) -> Optional[int]:
        """دریافت نسخه IP"""
        try:
            ip = ipaddress.ip_address(ip_str)
            return ip.version
        except ValueError:
            return None
    
    @staticmethod
    def normalize_mac(mac_str: str) -> str:
        """نرمال‌سازی آدرس MAC به فرمت استاندارد"""
        if not mac_str:
            return ''
        
        # حذف جداکننده‌ها
        mac = re.sub(r'[^A-Fa-f0-9]', '', mac_str)
        
        # اگر طول درست نبود
        if len(mac) != 12:
            return mac_str.upper()
        
        # فرمت با دو نقطه
        return ':'.join([mac[i:i+2] for i in range(0, 12, 2)]).upper()
    
    @staticmethod
    def validate_interface_name(interface: str) -> bool:
        """اعتبارسنجی نام اینترفیس"""
        # الگوهای معمول برای نام اینترفیس در لینوکس
        patterns = [
            r'^eth\d+$',      # Ethernet
            r'^en[ops]\d+$',  # Systemd naming
            r'^wlan\d+$',     # Wireless
            r'^wlp\d+s\d+$',  # Wireless PCI
            r'^lo$',          # Loopback
            r'^br\d+$',       # Bridge
            r'^bond\d+$',     # Bond
            r'^veth\d+$',     # Virtual Ethernet
            r'^tun\d+$',      # TUN/TAP
            r'^docker\d+$',   # Docker
            r'^vboxnet\d+$',  # VirtualBox
            r'^virbr\d+$',    # KVM bridge
        ]
        
        for pattern in patterns:
            if re.match(pattern, interface, re.IGNORECASE):
                return True
        
        return False
