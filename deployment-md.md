# Deployment Guide

This document outlines different ways to deploy the Amul Stock Checker Bot.

## 1. Linux Server / VPS (Recommended)

### Using Systemd

1. Copy files to server:
```bash
scp -r ./* your_username@your_server_ip:/opt/stockbot/
```

2. Create systemd service:
```bash
sudo nano /etc/systemd/system/stockbot.service
```

Add the following content:
```ini
[Unit]
Description=Amul Stock Checker Telegram Bot
After=network.target

[Service]
Type=simple
User=YOUR_USERNAME
WorkingDirectory=/opt/stockbot
ExecStart=/usr/bin/python3 /opt/stockbot/bot.py
Restart=always
RestartSec=10
StandardOutput=append:/var/log/stockbot.log
StandardError=append:/var/log/stockbot.error.log

[Install]
WantedBy=multi-user.target
```

3. Enable and start service:
```bash
sudo systemctl enable stockbot
sudo systemctl start stockbot
```

## 2. PythonAnywhere (Free Option)

1. Sign up at pythonanywhere.com
2. Upload all files to your PythonAnywhere directory
3. Install requirements:
```bash
pip3 install --user -r requirements.txt
```
4. Create a new scheduled task:
   - Go to "Tasks" tab
   - Add: `python3 /home/yourusername/bot.py`

## 3. Docker Deployment

Build the image:
```bash
docker build -t stock-checker-bot .
```

Run the container:
```bash
docker run -d --name stock-checker stock-checker-bot
```

## Monitoring

Check bot status:
```bash
# For systemd
sudo systemctl status stockbot

# For docker
docker logs stock-checker
```
