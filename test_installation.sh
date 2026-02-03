#!/bin/bash
Test installation script

echo "Testing RPT SWI installation..."
echo "================================"
Check root

if [ "$EUID" -ne 0 ]; then
echo "❌ Please run as root: sudo bash test_installation.sh"
exit 1
fi
Test Python

echo -n "Python 3: "
if command -v python3 &> /dev/null; then
echo "✅ $(python3 --version)"
else
echo "❌ Not found"
fi
Test dependencies

for cmd in nmap iptables; do
echo -n "$cmd: "
if command -v $cmd &> /dev/null; then
echo "✅ Found"
else
echo "❌ Not found"
fi
done
Test Python packages

echo -n "Python packages: "
if python3 -c "import scapy, iptc, netifaces" &> /dev/null; then
echo "✅ All installed"
else
echo "❌ Missing packages"
python3 -c "
import importlib
for pkg in ['scapy', 'iptc', 'netifaces']:
try:
importlib.import_module(pkg)
print(f' ✅ {pkg}')
except:
print(f' ❌ {pkg}')
"
fi
Test the program

echo -n "Program test: "
if [ -f src/main.py ]; then
timeout 5 python3 src/main.py --test 2>&1 | grep -q "DIAGNOSTIC TESTS" && echo "✅ Working" || echo "⚠ Issues"
else
echo "❌ main.py not found"
fi

echo ""
echo "Test complete!"
