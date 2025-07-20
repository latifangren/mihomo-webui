#!/bin/bash

SERVICE_NAME="mihomo-webui"
SERVICE_FILE="/etc/systemd/system/$SERVICE_NAME.service"

# Cek apakah service sudah ada
if systemctl list-units --full -all | grep -q "$SERVICE_NAME.service"; then
    echo "Service $SERVICE_NAME sudah terinstall."
    STATUS=$(systemctl is-active $SERVICE_NAME)
    echo "Status saat ini: $STATUS"
    echo "Pilih opsi:"
    echo "  1) Restart service"
    echo "  2) Stop service"
    echo "  3) Uninstall service"
    echo "  4) Lewati (tidak melakukan apa-apa)"
    read -p "Masukkan pilihan [1-4]: " PILIH
    case $PILIH in
        1)
            sudo systemctl restart $SERVICE_NAME
            echo "Service direstart."
            exit 0
            ;;
        2)
            sudo systemctl stop $SERVICE_NAME
            echo "Service distop."
            exit 0
            ;;
        3)
            sudo systemctl stop $SERVICE_NAME
            sudo systemctl disable $SERVICE_NAME
            sudo rm -f $SERVICE_FILE
            sudo systemctl daemon-reload
            echo "Service dihapus. Lanjut instalasi baru."
            ;;
        4)
            echo "Tidak melakukan perubahan."
            exit 0
            ;;
        *)
            echo "Pilihan tidak valid."
            exit 1
            ;;
    esac
fi

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
sudo tee $SERVICE_FILE > /dev/null <<EOF
[Unit]
Description=Mihomo WebUI Flask Service
After=network.target

[Service]
User=$(whoami)
WorkingDirectory=$PROJECT_DIR
ExecStart=$PROJECT_DIR/venv/bin/python $PROJECT_DIR/mihomo_web_interface.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# 4. Reload systemd, enable & start service
sudo systemctl daemon-reload
sudo systemctl enable $SERVICE_NAME
sudo systemctl restart $SERVICE_NAME

echo "Mihomo WebUI sudah otomatis jalan sebagai service!" 