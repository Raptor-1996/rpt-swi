#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""ثابت‌های برنامه"""

# نسخه برنامه
VERSION = "2.0.0"
AUTHOR = "Raptor-1996"
EMAIL = "EbiRom1996@gmail.com"
GITHUB_URL = "https://github.com/Raptor-1996/rpt-swi"

# پورت‌های رایج
COMMON_PORTS = {
    20: "FTP Data",
    21: "FTP Control",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    67: "DHCP Server",
    68: "DHCP Client",
    69: "TFTP",
    80: "HTTP",
    110: "POP3",
    119: "NNTP",
    123: "NTP",
    135: "MS RPC",
    137: "NetBIOS Name Service",
    138: "NetBIOS Datagram",
    139: "NetBIOS Session",
    143: "IMAP",
    161: "SNMP",
    162: "SNMP Trap",
    179: "BGP",
    194: "IRC",
    389: "LDAP",
    443: "HTTPS",
    445: "SMB",
    465: "SMTPS",
    514: "Syslog",
    515: "LPD/LPR",
    587: "SMTP Submission",
    631: "IPP",
    636: "LDAPS",
    993: "IMAPS",
    995: "POP3S",
    1433: "MSSQL",
    1521: "Oracle",
    1723: "PPTP",
    1883: "MQTT",
    1900: "UPnP",
    2082: "cPanel",
    2083: "cPanel SSL",
    2086: "WHM",
    2087: "WHM SSL",
    2095: "Webmail",
    2096: "Webmail SSL",
    2222: "DirectAdmin",
    2375: "Docker",
    2376: "Docker SSL",
    2483: "Oracle DB",
    2484: "Oracle DB SSL",
    3000: "Node.js",
    3306: "MySQL",
    3389: "RDP",
    3690: "SVN",
    4000: "Remote Anything",
    4443: "Apache Tomcat",
    4505: "SaltStack",
    4506: "SaltStack",
    4567: "Sinatra",
    4848: "GlassFish",
    5000: "UPnP",
    5432: "PostgreSQL",
    5601: "Kibana",
    5672: "RabbitMQ",
    5900: "VNC",
    5938: "TeamViewer",
    5984: "CouchDB",
    6000: "X11",
    6379: "Redis",
    6443: "Kubernetes",
    6667: "IRC",
    7000: "Cassandra",
    7001: "WebLogic",
    7077: "Spark",
    7200: "Cassandra SSL",
    7687: "Neo4j",
    7777: "Oracle Apps",
    8000: "HTTP Alt",
    8008: "HTTP Alt",
    8080: "HTTP Proxy",
    8081: "HTTP Proxy Alt",
    8088: "HTTP Alt",
    8090: "HTTP Alt",
    8091: "Couchbase",
    8140: "Puppet",
    8181: "HTTP Alt",
    8200: "GoLand",
    8443: "HTTPS Alt",
    8500: "Consul",
    8761: "Eureka",
    8888: "HTTP Alt",
    9000: "SonarQube",
    9001: "Tor",
    9042: "Cassandra",
    9092: "Kafka",
    9100: "PDL Data",
    9200: "Elasticsearch",
    9300: "Elasticsearch",
    9418: "Git",
    9999: "HTTP Alt",
    10000: "Webmin",
    11211: "Memcached",
    15672: "RabbitMQ",
    27017: "MongoDB",
    27018: "MongoDB",
    28017: "MongoDB HTTP",
    50000: "DB2",
    50030: "Hadoop",
    50070: "Hadoop",
}

# پروتکل‌های شبکه
PROTOCOLS = {
    1: "ICMP",
    6: "TCP",
    17: "UDP",
    58: "ICMPv6",
}

# انواع دستگاه‌های شبکه
DEVICE_TYPES = {
    "router": "Router/Gateway",
    "switch": "Network Switch",
    "access_point": "Wireless Access Point",
    "server": "Server",
    "workstation": "Workstation/PC",
    "laptop": "Laptop",
    "mobile": "Mobile Device",
    "iot": "IoT Device",
    "printer": "Printer",
    "camera": "Camera",
    "nas": "Network Storage",
    "voip": "VoIP Phone",
    "unknown": "Unknown Device"
}

# وضعیت دستگاه
DEVICE_STATUS = {
    "online": "Online",
    "offline": "Offline",
    "blocked": "Blocked",
    "trusted": "Trusted",
    "suspicious": "Suspicious",
    "quarantined": "Quarantined"
}

# اولویت اعلان‌ها
NOTIFICATION_PRIORITY = {
    "low": "Low",
    "normal": "Normal",
    "high": "High",
    "critical": "Critical"
}

# انواع اسکن
SCAN_TYPES = {
    "quick": "Quick Scan (ARP only)",
    "full": "Full Scan (All methods)",
    "deep": "Deep Scan (with ports)",
    "continuous": "Continuous Monitoring",
    "scheduled": "Scheduled Scan"
}

# انواع اقدامات فایروال
FIREWALL_ACTIONS = {
    "allow": "Allow",
    "drop": "Drop",
    "reject": "Reject",
    "log": "Log Only",
    "quarantine": "Quarantine"
}

# رنگ‌های وضعیت
STATUS_COLORS = {
    "online": "green",
    "offline": "gray",
    "blocked": "red",
    "trusted": "blue",
    "suspicious": "yellow",
    "quarantined": "magenta"
}

# ماژول‌های برنامه
MODULES = [
    "scanner",
    "firewall",
    "database",
    "notifications",
    "monitoring",
    "reports",
    "backup"
]

# محدودیت‌ها
LIMITS = {
    "max_devices": 10000,
    "max_scans_per_day": 1440,  # هر دقیقه
    "max_rules": 1000,
    "max_notifications": 1000,
    "max_log_size_mb": 100,
    "max_backup_files": 30
}

# پیام‌های خطا
ERROR_MESSAGES = {
    "PERMISSION_DENIED": "Permission denied. Run with sudo/administrator privileges.",
    "NETWORK_ERROR": "Network error. Check your connection.",
    "SCAN_FAILED": "Network scan failed.",
    "FIREWALL_ERROR": "Firewall operation failed.",
    "DATABASE_ERROR": "Database operation failed.",
    "CONFIG_ERROR": "Configuration error.",
    "DEPENDENCY_MISSING": "Required dependency missing: {}",
    "DEVICE_NOT_FOUND": "Device not found.",
    "INVALID_INPUT": "Invalid input.",
    "TIMEOUT": "Operation timed out.",
    "UNKNOWN_ERROR": "Unknown error occurred."
}

# پیام‌های موفقیت
SUCCESS_MESSAGES = {
    "SCAN_COMPLETE": "Network scan completed successfully.",
    "DEVICE_BLOCKED": "Device blocked successfully.",
    "DEVICE_UNBLOCKED": "Device unblocked successfully.",
    "BACKUP_CREATED": "Backup created successfully.",
    "SETTINGS_SAVED": "Settings saved successfully.",
    "UPDATE_COMPLETE": "Update completed successfully."
}

# کدهای خروجی
EXIT_CODES = {
    "SUCCESS": 0,
    "ERROR": 1,
    "PERMISSION_ERROR": 2,
    "NETWORK_ERROR": 3,
    "CONFIG_ERROR": 4,
    "DEPENDENCY_ERROR": 5,
    "DATABASE_ERROR": 6,
    "FIREWALL_ERROR": 7
}

# فرمت‌های تاریخ و زمان
TIME_FORMATS = {
    "display": "%Y-%m-%d %H:%M:%S",
    "file": "%Y%m%d_%H%M%S",
    "log": "%Y-%m-%d %H:%M:%S",
    "iso": "%Y-%m-%dT%H:%M:%S"
}

# واحدها
UNITS = {
    "bytes": ["B", "KB", "MB", "GB", "TB", "PB"],
    "time": ["s", "m", "h", "d"],
    "speed": ["bps", "Kbps", "Mbps", "Gbps"]
}

# تنظیمات پیش‌فرض
DEFAULT_SETTINGS = {
    "scanner": {
        "timeout": 30,
        "threads": 50,
        "retries": 2
    },
    "firewall": {
        "default_action": "DROP",
        "logging": True,
        "auto_backup": True
    },
    "database": {
        "cleanup_days": 30,
        "backup_hours": 24
    },
    "monitoring": {
        "interval": 300,
        "alert_on_new": True
    }
}

# ماک آدرس‌های خاص
SPECIAL_MACS = {
    "FF:FF:FF:FF:FF:FF": "Broadcast",
    "01:00:5E:00:00:00": "IPv4 Multicast",
    "33:33:00:00:00:00": "IPv6 Multicast",
    "00:00:00:00:00:00": "Invalid/Empty"
}

# رنج IP‌های خصوصی
PRIVATE_IP_RANGES = [
    "10.0.0.0/8",
    "172.16.0.0/12",
    "192.168.0.0/16",
    "169.254.0.0/16",  # Link-local
    "127.0.0.0/8"      # Loopback
]

# پورت‌های خطرناک
DANGEROUS_PORTS = [
    21,    # FTP - often misconfigured
    22,    # SSH - brute force attacks
    23,    # Telnet - unencrypted
    135,   # MS RPC - vulnerabilities
    139,   # NetBIOS - information disclosure
    445,   # SMB - worm propagation
    1433,  # MSSQL - brute force
    1521,  # Oracle - attacks
    3306,  # MySQL - brute force
    3389,  # RDP - brute force
    5900,  # VNC - unencrypted
    6379,  # Redis - unauthorized access
    27017  # MongoDB - unauthorized access
]
