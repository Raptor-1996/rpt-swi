#!/usr/bin/env python3
# -*- coding: utf-8 -*-

MAC_VENDORS = {
    '00:00:00': 'XEROX CORPORATION',
    '00:00:01': 'XEROX CORPORATION',
    '00:00:02': 'XEROX CORPORATION',
    '00:00:03': 'XEROX CORPORATION',
    '00:00:04': 'XEROX CORPORATION',
    '00:00:05': 'XEROX CORPORATION',
    '00:00:06': 'XEROX CORPORATION',
    '00:00:07': 'XEROX CORPORATION',
    '00:00:08': 'XEROX CORPORATION',
    '00:00:09': 'XEROX CORPORATION',
    '00:00:0A': 'OMRON TATEISI ELECTRONICS CO.',
    '00:00:0B': 'MATRIX CORPORATION',
    '00:00:0C': 'CISCO SYSTEMS, INC.',
    '00:00:0D': 'FIBRONICS LTD.',
    '00:00:0E': 'FUJITSU LIMITED',
    '00:00:0F': 'NEXT, INC.',
    '00:00:10': 'SYTEK INC.',
    '00:00:11': 'NORMEREL SYSTEMES',
    '00:00:12': 'INFORMATION TECHNOLOGY LIMITED',
    '00:00:13': 'CAMEX',
    '00:00:14': 'NETRONIX',
    '00:00:15': 'DATAPOINT CORPORATION',
    '00:00:16': 'DU PONT PIXEL SYSTEMS',
    '00:00:17': 'Oracle',
    '00:00:18': 'WEBSTER COMPUTER CORPORATION',
    '00:00:19': 'APPLIED DYNAMICS INTERNATIONAL',
    '00:00:1A': 'ADVANCED MICRO DEVICES',
    '00:00:1B': 'NOVEL INC.',
    '00:00:1C': 'BELL TECHNOLOGIES',
    '00:00:1D': 'CABLE AND WIRELESS',
    '00:00:1E': 'TELSIST INDUSTRIA ELECTRONICA',
    '00:00:1F': 'Telco Systems, Inc.',
    '00:00:20': 'DATAINDUSTRIER DIAB',
    '00:00:21': 'SUREMAN COMP. & COMMUN. CORP.',
    '00:00:22': 'VISUAL TECHNOLOGY INC.',
    '00:00:23': 'ABB INDUSTRIAL SYSTEMS AB',
    '00:00:24': 'CONNECT AS',
    '00:00:25': 'RAMTEK CORP.',
    '00:00:26': 'SHA-KEN CO., LTD.',
    '00:00:27': 'JAPAN RADIO COMPANY',
    '00:00:28': 'PRODIGY SYSTEMS CORPORATION',
    '00:00:29': 'IMC NETWORKS CORP.',
    '00:00:2A': 'TRW - SEDD/INP',
    '00:00:2B': 'CRISP AUTOMATION, INC',
    '00:00:2C': 'AUTOTOTE LIMITED',
    '00:00:2D': 'CHROMATICS INC.',
    '00:00:2E': 'SOCIETE EVIRA',
    '00:00:2F': 'TIMEPLEX INC.',
    '00:00:30': 'VG LABORATORY SYSTEMS LTD',
    '00:00:31': 'QPSX COMMUNICATIONS PTY LTD',
    '00:00:32': 'Marconi plc',
    '00:00:33': 'EASYNET LTD',
    '00:00:34': 'NETWORK CONTROLS INTNATL INC.',
    '00:00:35': 'LITTON SYSTEMS, INC.',
    '00:00:36': 'INTERFACE CO.',
    '00:00:37': 'RICHARD HIRSCHMANN GMBH & CO.',
    '00:00:38': 'WYSE TECHNOLOGY',
    '00:00:39': 'SGS-THOMSON MICROELECTRONICS',
    '00:00:3A': 'BIOMATION',
    '00:00:3B': 'SILEX TECHNOLOGY, INC.',
    '00:00:3C': 'YOKOGAWA DIGITAL COMPUTER CORP',
    '00:00:3D': 'NETWORK GENERAL CORPORATION',
    '00:00:3E': 'TALARIS SYSTEMS, INC.',
    '00:00:3F': 'SOFTCOM A/S',
    '00:00:40': 'NETWORK COMPUTING DEVICES INC.',
    '00:00:41': 'GAMMA LINK',
    '00:00:42': 'ABB Signal AB',
    '00:00:43': 'ASCOM INFRASYS AG',
    '00:00:44': 'NIPPON STEEL CORPORATION',
    '00:00:45': 'ONLINE COMPUTER INC.',
    '00:00:46': 'CUSTOM SYSTEMS',
    '00:00:47': 'HOB ELECTRONIC GMBH & CO. KG',
    '00:00:48': 'FERRANTI COMPUTER SYS. LIMITED',
    '00:00:49': 'RACAL-MILGO INFORMATION SYS..',
    '00:00:4A': 'JAPAN MACNICS CO., LTD.',
    '00:00:4B': 'PIXEL COMPUTER INC.',
    '00:00:4C': 'DAVID SYSTEMS INC.',
    '00:00:4D': 'CONCURRENT COMPUTER CORP.',
    '00:00:4E': 'Sony',
    '00:00:4F': 'SEXANT TECHNOLOGIES',
    '00:00:50': 'IMAGEN CORPORATION',
    '00:00:51': 'SYSTEMS MANAGEMENT ARTS',
    '00:00:52': 'TELMAT INFORMATIQUE',
    '00:00:53': 'NETWORK APPLICATION TECHNOLOGY',
    '00:00:54': 'SYSTEMS & PROCESSES ENGINEERING',
    '00:00:55': 'CHUO ELECTRONICS CO., LTD.',
    '00:00:56': 'FUJITSU LIMITED',
    '00:00:57': 'COMPUTER LABS AND SOFTWARE',
    '00:00:58': 'BRAND COMMUNICATIONS, LTD.',
    '00:00:59': 'JUSTSYSTEM CORPORATION',
    '00:00:5A': 'LUXCOM, INC.',
    '00:00:5B': 'Compaq',
    '00:00:5C': 'DIGITAL EQUIPMENT CORPORATION',
    '00:00:5D': 'RICOH COMPANY LTD.',
    '00:00:5E': 'NEC CORPORATION',
    '00:00:5F': 'DCI CORPORATION',
    '00:00:60': 'AMPEX CORPORATION',
    '00:00:61': 'LOGICRAFT, INC.',
    '00:00:62': 'RADISYS CORPORATION',
    '00:00:63': 'HOB ELECTRONIC GMBH & CO. KG',
    '00:00:64': 'INTEGRATED SOLUTIONS INC.',
    '00:00:65': 'FIBRONICS LTD.',
    '00:00:66': 'MC DATA LIMITED',
    '00:00:67': 'PHOENIX DATA COMMUNICATIONS CORP',
    '00:00:68': 'RAYTHEON CORPORATION',
    '00:00:69': 'SUN MICROSYSTEMS, INC.',
    '00:00:6A': 'TELEBIT CORPORATION',
    '00:00:6B': 'DIGITAL BIOLOGICS INC.',
    '00:00:6C': 'Rainbow Technologies, Inc.',
    '00:00:6D': 'Tellabs Operations, Inc.',
    '00:00:6E': 'YOKOGAWA ELECTRIC CORPORATION',
    '00:00:6F': 'NETWORK GENERAL CORPORATION',
    '00:00:70': 'TALARIS SYSTEMS, INC.',
    '00:00:71': 'SOFTCOM A/S',
    '00:00:72': 'NETWORK COMPUTING DEVICES INC.',
    '00:00:73': 'GAMMA LINK',
    '00:00:74': 'ABB Signal AB',
    '00:00:75': 'ASCOM INFRASYS AG',
    '00:00:76': 'NIPPON STEEL CORPORATION',
    '00:00:77': 'ONLINE COMPUTER INC.',
    '00:00:78': 'CUSTOM SYSTEMS',
    '00:00:79': 'HOB ELECTRONIC GMBH & CO. KG',
    '00:00:7A': 'FERRANTI COMPUTER SYS. LIMITED',
    '00:00:7B': 'RACAL-MILGO INFORMATION SYS..',
    '00:00:7C': 'JAPAN MACNICS CO., LTD.',
    '00:00:7D': 'PIXEL COMPUTER INC.',
    '00:00:7E': 'DAVID SYSTEMS INC.',
    '00:00:7F': 'CONCURRENT COMPUTER CORP.',
    
    # Apple MAC addresses (partial list)
    '00:03:93': 'Apple',
    '00:05:02': 'Apple',
    '00:0A:27': 'Apple',
    '00:0A:95': 'Apple',
    '00:0D:93': 'Apple',
    '00:10:FA': 'Apple',
    '00:11:24': 'Apple',
    '00:14:51': 'Apple',
    '00:16:CB': 'Apple',
    '00:17:F2': 'Apple',
    '00:19:E3': 'Apple',
    '00:1B:63': 'Apple',
    '00:1D:4F': 'Apple',
    '00:1E:52': 'Apple',
    '00:1E:C2': 'Apple',
    '00:1F:5B': 'Apple',
    '00:1F:F3': 'Apple',
    '00:21:E9': 'Apple',
    '00:22:41': 'Apple',
    '00:23:12': 'Apple',
    '00:23:32': 'Apple',
    '00:23:6C': 'Apple',
    '00:23:DF': 'Apple',
    '00:24:36': 'Apple',
    '00:24:A5': 'Apple',
    '00:25:00': 'Apple',
    '00:25:4B': 'Apple',
    '00:25:BC': 'Apple',
    '00:26:08': 'Apple',
    '00:26:4A': 'Apple',
    '00:26:B0': 'Apple',
    '00:26:BB': 'Apple',
    '00:30:65': 'Apple',
    '00:3A:99': 'Apple',
    '00:3A:9D': 'Apple',
    '00:3A:A1': 'Apple',
    '00:3E:E1': 'Apple',
    '00:50:E4': 'Apple',
    '00:56:CD': 'Apple',
    '00:61:71': 'Apple',
    '00:6D:52': 'Apple',
    '00:88:65': 'Apple',
    '00:A0:40': 'Apple',
    '00:C6:10': 'Apple',
    '00:CD:FE': 'Apple',
    '04:0C:CE': 'Apple',
    '04:15:52': 'Apple',
    '04:1E:64': 'Apple',
    '04:26:65': 'Apple',
    '04:48:9A': 'Apple',
    '04:4B:ED': 'Apple',
    '04:52:F3': 'Apple',
    '04:54:53': 'Apple',
    '04:69:F8': 'Apple',
    '04:D3:CF': 'Apple',
    '04:D4:C4': 'Apple',
    '04:E5:36': 'Apple',
    '04:F1:3E': 'Apple',
    '04:F7:E4': 'Apple',
    '08:00:07': 'Apple',
    '08:66:98': 'Apple',
    '08:6D:41': 'Apple',
    '08:70:45': 'Apple',
    '08:74:02': 'Apple',
    
    # سایر سازندگان معروف
    '00:50:56': 'VMware, Inc.',
    '00:0C:29': 'VMware, Inc.',
    '00:1C:14': 'VMware, Inc.',
    '00:05:69': 'VMware, Inc.',
    
    '08:00:27': 'Oracle VirtualBox',
    
    '00:1D:0F': 'Cisco Systems',
    '00:1E:13': 'Cisco Systems',
    '00:1E:4A': 'Cisco Systems',
    '00:1E:7D': 'Cisco Systems',
    '00:1F:6C': 'Cisco Systems',
    '00:21:1B': 'Cisco Systems',
    '00:22:55': 'Cisco Systems',
    '00:23:04': 'Cisco Systems',
    '00:23:EB': 'Cisco Systems',
    '00:24:14': 'Cisco Systems',
    '00:25:84': 'Cisco Systems',
    '00:26:0B': 'Cisco Systems',
    '00:26:F2': 'Cisco Systems',
    
    '00:1A:11': 'Google, Inc.',
    '00:1A:6B': 'Google, Inc.',
    '00:1A:6C': 'Google, Inc.',
    '00:1B:11': 'Google, Inc.',
    '00:1C:11': 'Google, Inc.',
    '00:1D:3A': 'Google, Inc.',
    '00:1E:68': 'Google, Inc.',
    
    '00:24:E4': 'Dell Inc.',
    '00:1D:09': 'Dell Inc.',
    '00:1E:4F': 'Dell Inc.',
    '00:21:70': 'Dell Inc.',
    '00:22:19': 'Dell Inc.',
    '00:23:AE': 'Dell Inc.',
    '00:24:B8': 'Dell Inc.',
    '00:26:B9': 'Dell Inc.',
    
    '00:13:D4': 'Intel Corporate',
    '00:14:4D': 'Intel Corporate',
    '00:15:00': 'Intel Corporate',
    '00:15:17': 'Intel Corporate',
    '00:16:6F': 'Intel Corporate',
    '00:16:76': 'Intel Corporate',
    '00:16:EA': 'Intel Corporate',
    '00:17:31': 'Intel Corporate',
    '00:18:DE': 'Intel Corporate',
    '00:19:D1': 'Intel Corporate',
    '00:1B:21': 'Intel Corporate',
    '00:1B:77': 'Intel Corporate',
    '00:1C:BF': 'Intel Corporate',
    '00:1D:E0': 'Intel Corporate',
    '00:1E:67': 'Intel Corporate',
    '00:1F:3B': 'Intel Corporate',
    '00:20:7C': 'Intel Corporate',
    '00:21:5C': 'Intel Corporate',
    '00:22:FA': 'Intel Corporate',
    '00:23:14': 'Intel Corporate',
    '00:24:D6': 'Intel Corporate',
    '00:25:00': 'Intel Corporate',
    
    '00:0F:B0': 'Samsung Electronics',
    '00:12:47': 'Samsung Electronics',
    '00:13:77': 'Samsung Electronics',
    '00:15:99': 'Samsung Electronics',
    '00:16:32': 'Samsung Electronics',
    '00:16:6B': 'Samsung Electronics',
    '00:16:6C': 'Samsung Electronics',
    '00:16:DB': 'Samsung Electronics',
    '00:17:9E': 'Samsung Electronics',
    '00:17:C5': 'Samsung Electronics',
    '00:18:AF': 'Samsung Electronics',
    '00:19:4E': 'Samsung Electronics',
    '00:1A:8A': 'Samsung Electronics',
    '00:1B:98': 'Samsung Electronics',
    '00:1C:43': 'Samsung Electronics',
    '00:1D:25': 'Samsung Electronics',
    '00:1D:FA': 'Samsung Electronics',
    '00:1E:7D': 'Samsung Electronics',
    '00:1F:CC': 'Samsung Electronics',
    '00:20:3F': 'Samsung Electronics',
    '00:21:4C': 'Samsung Electronics',
    '00:22:47': 'Samsung Electronics',
    '00:23:39': 'Samsung Electronics',
    '00:24:54': 'Samsung Electronics',
    '00:25:38': 'Samsung Electronics',
    '00:26:37': 'Samsung Electronics',
    
    '00:1E:68': 'HTC Corporation',
    '00:23:76': 'HTC Corporation',
    '00:25:61': 'HTC Corporation',
    '00:26:51': 'HTC Corporation',
    
    '00:1B:DC': 'Nokia Corporation',
    '00:1C:35': 'Nokia Corporation',
    '00:1C:9A': 'Nokia Corporation',
    '00:1D:3B': 'Nokia Corporation',
    '00:1D:E1': 'Nokia Corporation',
    '00:1E:3B': 'Nokia Corporation',
    '00:1E:A4': 'Nokia Corporation',
    '00:1F:01': 'Nokia Corporation',
    '00:1F:5D': 'Nokia Corporation',
    '00:1F:DF': 'Nokia Corporation',
    '00:20:3E': 'Nokia Corporation',
    '00:21:FC': 'Nokia Corporation',
    '00:22:FC': 'Nokia Corporation',
    '00:23:B3': 'Nokia Corporation',
    '00:24:03': 'Nokia Corporation',
    '00:24:7F': 'Nokia Corporation',
    '00:25:CF': 'Nokia Corporation',
    '00:26:6E': 'Nokia Corporation',
}

def get_vendor_from_mac(mac_address):
    """دریافت نام سازنده از آدرس MAC"""
    if not mac_address:
        return "Unknown"
    
    # نرمال‌سازی MAC
    mac = mac_address.upper().replace(':', '').replace('-', '')
    
    # جستجو بر اساس prefixهای مختلف
    for prefix_len in [6, 4, 2]:  # ابتدا ۳ بایت، سپس ۲ بایت، سپس ۱ بایت
        prefix = mac[:prefix_len]
        for vendor_prefix, vendor_name in MAC_VENDORS.items():
            vendor_hex = vendor_prefix.replace(':', '')
            if vendor_hex.startswith(prefix):
                return vendor_name
    
    return "Unknown Manufacturer"

def load_vendor_database(file_path=None):
    """بارگذاری دیتابیس سازندگان از فایل"""
    import json
    from pathlib import Path
    
    if not file_path:
        file_path = Path(__file__).parent / 'mac_vendors_db.json'
    
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # اگر فایل وجود نداشت، از دیتابیس داخلی استفاده کن
        return MAC_VENDORS
    except Exception as e:
        print(f"Error loading vendor database: {e}")
        return MAC_VENDORS

def update_vendor_database():
    """به‌روزرسانی دیتابیس سازندگان از اینترنت"""
    import requests
    
    try:
        # دانلود آخرین دیتابیس از IEEE
        response = requests.get(
            "http://standards-oui.ieee.org/oui/oui.txt",
            timeout=10
        )
        
        if response.status_code == 200:
            vendors = {}
            for line in response.text.split('\n'):
                if '(base 16)' in line:
                    parts = line.split('(base 16)')
                    if len(parts) == 2:
                        prefix = parts[0].strip().upper()
                        vendor = parts[1].strip()
                        vendors[prefix] = vendor
            
            # ذخیره در فایل
            import json
            with open('mac_vendors_db.json', 'w') as f:
                json.dump(vendors, f, indent=2)
            
            return True, f"Database updated with {len(vendors)} vendors"
        else:
            return False, "Failed to download database"
            
    except Exception as e:
        return False, f"Error: {str(e)}"
