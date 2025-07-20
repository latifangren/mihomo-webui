#!/bin/bash

SERVICE_NAME="mihomo-webui"
SERVICE_FILE="/etc/systemd/system/$SERVICE_NAME.service"
REPO_URL="https://github.com/latifangren/mihomo-webui.git"
FOLDER="mihomo-webui"

# Cek apakah file service systemd benar-benar ada
if [ -f "$SERVICE_FILE" ]; then
    echo "Service $SERVICE_NAME sudah terinstall."
    STATUS=$(systemctl is-active $SERVICE_NAME 2>/dev/null || echo "not-found")
    echo "Status saat ini: $STATUS"
    echo "Pilih opsi:"
    echo "  1) Timpa (stop, hapus, dan install ulang service & webui)"
    echo "  2) Batalkan instalasi"
    read -p "Masukkan pilihan [1-2]: " PILIH
    PILIH="${PILIH//$'\r'/}"  # Hapus karakter carriage return jika ada
    case "$PILIH" in
        1)
            echo "Menghapus service dan folder project..."
            sudo systemctl stop $SERVICE_NAME
            sudo systemctl disable $SERVICE_NAME
            sudo rm -f $SERVICE_FILE
            sudo systemctl daemon-reload
            cd ..
            rm -rf "$FOLDER"
            echo "Service dan folder project dihapus. Melanjutkan clone ulang..."
            git clone "$REPO_URL"
            echo "Silakan masuk ke folder $FOLDER dan jalankan setup_webui.sh lagi:"
            echo "  cd $FOLDER && chmod +x setup_webui.sh && ./setup_webui.sh"
            exit 0
            ;;
        2)
            echo "Batal instalasi."
            exit 0
            ;;
        *)
            echo "Pilihan tidak valid: '$PILIH'"
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