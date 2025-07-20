#!/bin/bash

set -e

ARCH="linux-amd64"
INSTALL_DIR="/usr/local/bin"
CONFIG_DIR="/etc/mihomo"
LOG_DIR="/var/log/mihomo"
SERVICE_FILE="/etc/systemd/system/mihomo.service"

# Cek apakah binary Mihomo sudah ada
if [ -f "$INSTALL_DIR/mihomo" ]; then
    echo "Binary Mihomo sudah ada di $INSTALL_DIR/mihomo."
    read -p "Timpa/overwrite binary Mihomo yang lama? [y/N]: " OVERWRITE_BIN
    OVERWRITE_BIN="${OVERWRITE_BIN,,}" # lowercase
    if [[ "$OVERWRITE_BIN" != "y" && "$OVERWRITE_BIN" != "yes" ]]; then
        echo "Batal install. Tidak ada perubahan."
        exit 0
    fi
fi

# Cek apakah service Mihomo sudah ada
if [ -f "$SERVICE_FILE" ]; then
    echo "Service systemd Mihomo sudah ada di $SERVICE_FILE."
    read -p "Timpa/overwrite service Mihomo yang lama? [y/N]: " OVERWRITE_SVC
    OVERWRITE_SVC="${OVERWRITE_SVC,,}" # lowercase
    if [[ "$OVERWRITE_SVC" != "y" && "$OVERWRITE_SVC" != "yes" ]]; then
        echo "Batal install. Tidak ada perubahan."
        exit 0
    fi
fi

# Ambil versi terbaru dan asset URL dari Github API
echo "=== Mencari versi Mihomo terbaru... ==="
API_JSON=$(curl -s https://api.github.com/repos/MetaCubeX/mihomo/releases/latest)
LATEST_VERSION=$(echo "$API_JSON" | grep tag_name | cut -d '"' -f4)
echo "Versi terbaru: $LATEST_VERSION"

ASSET_URL=$(echo "$API_JSON" | grep browser_download_url | grep "$ARCH" | grep -E '\.gz"' | grep -v compatible | grep -v go | cut -d '"' -f4 | head -n1)

if [ -z "$ASSET_URL" ]; then
    echo "Tidak menemukan asset Mihomo untuk arsitektur $ARCH di rilis $LATEST_VERSION!"
    exit 1
fi

echo "=== Download Mihomo dari $ASSET_URL ==="
curl -L "$ASSET_URL" -o /tmp/mihomo.gz

echo "=== Ekstrak dan install ==="
gunzip -c /tmp/mihomo.gz > /tmp/mihomo
sudo mv /tmp/mihomo $INSTALL_DIR/mihomo
sudo chmod +x $INSTALL_DIR/mihomo

echo "=== Buat folder config dan log ==="
sudo mkdir -p $CONFIG_DIR
sudo mkdir -p $LOG_DIR
sudo touch $CONFIG_DIR/config.yaml
sudo chown -R $USER:$USER $CONFIG_DIR
sudo chown -R $USER:$USER $LOG_DIR

echo "=== Buat systemd service ==="
sudo tee $SERVICE_FILE > /dev/null <<EOF
[Unit]
Description=Mihomo (Clash Meta Mihomo)
After=network.target

[Service]
Type=simple
ExecStart=$INSTALL_DIR/mihomo -d $CONFIG_DIR
Restart=always
User=$USER
StandardOutput=append:$LOG_DIR/mihomo.log
StandardError=append:$LOG_DIR/mihomo.log

[Install]
WantedBy=multi-user.target
EOF

echo "=== Reload systemd, enable & start Mihomo ==="
sudo systemctl daemon-reload
sudo systemctl enable mihomo
sudo systemctl restart mihomo

echo "=== Mihomo $LATEST_VERSION berhasil diinstall dan berjalan sebagai service! ==="
echo "Edit config di: $CONFIG_DIR/config.yaml"
echo "Log di: $LOG_DIR/mihomo.log" 