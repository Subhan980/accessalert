#!/usr/bin/env python3

import os
import getpass
import psutil
import smtplib
import socket
from email.message import EmailMessage
from datetime import datetime


EMAIL = "muhammadsubhank045@gmail.com"
APP_PASSWORD = "gvbchoreaxpffymw"   
SEND_TO = "muhammasdsubhank045@gmail.com"


IMAGE = "/tmp/capture.jpg"
os.system(f"fswebcam -r 640x480 --no-banner {IMAGE}")

if not os.path.exists(IMAGE):
    print("❌ Image not created")
    exit()


username = getpass.getuser()
hostname = socket.gethostname()
time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

battery = psutil.sensors_battery()
if battery:
    percent = battery.percent
    status = "Charging" if battery.power_plugged else "Discharging"
else:
    percent = "N/A"
    status = "N/A"


msg = EmailMessage()
msg["Subject"] = "🚨 Laptop Access Alert"
msg["From"] = EMAIL
msg["To"] = SEND_TO

msg.set_content(f"""
🚨 Laptop Opened Alert 🚨

User: {username}
System: {hostname}
Date & Time: {time}

Battery: {percent}%
Status: {status}
""")


with open(IMAGE, "rb") as f:
    msg.add_attachment(
        f.read(),
        maintype="image",
        subtype="jpeg",
        filename="user.jpg"
    )


try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL, APP_PASSWORD)
        server.send_message(msg)
    print(" Alert Email Sent Successfully")
except Exception as e:
    print(f"Email Failed: {e}")
