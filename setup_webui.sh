#!/bin/bash

# Path ke direktori project (otomatis sesuai lokasi script dijalankan)
PROJECT_DIR="$(pwd)"

# 1. Buat virtual environment jika belum ada
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# 2. Aktifkan venv & install Flask
source venv/bin/activate
pip install --upgrade pip
pip install flask
deactivate

# 3. Buat systemd service
SERVICE_FILE="/etc/systemd/system/mihomo-webui.service"
RUN_USER=$(whoami)
sudo tee $SERVICE_FILE > /dev/null <<EOF
[Unit]
Description=Mihomo WebUI Flask Service
After=network.target

[Service]
User=$RUN_USER
WorkingDirectory=$PROJECT_DIR
ExecStart=$PROJECT_DIR/venv/bin/python $PROJECT_DIR/mihomo_web_interface.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# 4. Reload systemd, enable & start service
sudo systemctl daemon-reload
sudo systemctl enable mihomo-webui
sudo systemctl restart mihomo-webui

echo "Mihomo WebUI sudah otomatis jalan sebagai service!" 