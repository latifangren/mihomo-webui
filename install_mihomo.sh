#!/bin/bash

set -e

ARCH="linux-amd64"
INSTALL_DIR="/usr/local/bin"
CONFIG_DIR="/etc/mihomo"
LOG_DIR="/var/log/mihomo"
SERVICE_FILE="/etc/systemd/system/mihomo.service"

# Ambil versi terbaru dari Github API
echo "=== Mencari versi Mihomo terbaru... ==="
LATEST_VERSION=$(curl -s https://api.github.com/repos/MetaCubeX/mihomo/releases/latest | grep tag_name | cut -d '"' -f4)
echo "Versi terbaru: $LATEST_VERSION"

DOWNLOAD_URL="https://github.com/MetaCubeX/mihomo/releases/download/${LATEST_VERSION}/mihomo-${ARCH}.tar.gz"

echo "=== Download Mihomo $LATEST_VERSION ($ARCH) ==="
curl -L "$DOWNLOAD_URL" -o /tmp/mihomo.tar.gz

echo "=== Ekstrak dan install ==="
tar -xzf /tmp/mihomo.tar.gz -C /tmp
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