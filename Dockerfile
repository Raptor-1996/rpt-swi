FROM python:3.9-slim

LABEL maintainer="Raptor-1996 <EbiRom1996@gmail.com>"
LABEL version="2.0.0"
LABEL description="RPT See Who Is In - Network Security Tool"

# نصب وابستگی‌های سیستم
RUN apt-get update && apt-get install -y \
    nmap \
    arp-scan \
    net-tools \
    iptables \
    iproute2 \
    tcpdump \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# ایجاد کاربر غیر root
RUN useradd -m -s /bin/bash rptuser

# کپی برنامه
WORKDIR /app
COPY . .

# نصب وابستگی‌های پایتون
RUN pip install --no-cache-dir -r requirements.txt

# تنظیم مجوزها
RUN chown -R rptuser:rptuser /app
RUN chmod +x /app/src/main.py

# سوئیچ به کاربر غیر root
USER rptuser

# ایجاد volume برای ذخیره داده‌ها
VOLUME ["/home/rptuser/.config/rpt-swi"]

# نقطه ورود
ENTRYPOINT ["python", "/app/src/main.py"]
CMD ["--help"]
