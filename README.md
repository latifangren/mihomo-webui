# Mihomo WebUI

Antarmuka web sederhana dan modern untuk mengelola layanan Mihomo (Clash Mihomo) di server Linux/Ubuntu.

## Fitur
- Kontrol layanan Mihomo: Start, Stop, Restart
- Status Mihomo real-time
- Log Mihomo real-time (dari systemd journal)
- Clear log Mihomo
- Upload & edit config.yaml langsung dari web
- Statistik uptime, waktu aktif, dsb
- Dark mode
- Notifikasi status aksi
- Konfigurasi autostart Mihomo (enable/disable systemd)
- Tampilan responsif & mudah digunakan

## Prasyarat
- Python 3.7+
- Mihomo sudah terinstall dan berjalan sebagai service systemd (`mihomo.service`) #jika belum ada silahkan install dulu
- User punya akses sudo (untuk kontrol service & log)

## Cara Install Mihomo (Core) Otomatis
Script `install_mihomo.sh` akan otomatis menginstall Mihomo **versi terbaru** (auto-latest) dari Github, setup config, log, dan systemd service.

```bash
curl -O https://raw.githubusercontent.com/latifangren/mihomo-webui/main/install_mihomo.sh
chmod +x install_mihomo.sh
./install_mihomo.sh
```

- Config: `/etc/mihomo/config.yaml`
- Log: `/var/log/mihomo/mihomo.log`
- Service: `mihomo` (systemd)

## Cara Install & Setup WebUI
> **Tips:** Jalankan semua perintah di bawah ini dari direktori tempat Anda ingin menyimpan folder `mihomo-webui`.

1. **Clone repository ini dengan script helper:**
   ```bash
   curl -O https://raw.githubusercontent.com/latifangren/mihomo-webui/main/install.sh
   chmod +x install.sh
   ./install.sh
   cd mihomo-webui
   ```
   jika error jangan paste semua, tapi running 1 per 1
   > Script `install.sh` akan otomatis:
   > - Mengecek apakah folder sudah ada
   > - Menawarkan opsi hapus, rename, atau batal jika folder sudah ada
   > - Clone repo jika folder belum ada

2. **Jalankan script setup otomatis:**
   ```bash
   chmod +x setup_webui.sh
   ./setup_webui.sh
   ```
   Script ini akan:
   - Membuat virtual environment
   - Install Flask
   - Membuat systemd service `mihomo-webui`
   - Mengaktifkan autostart webui

3. **Akses WebUI:**
   Buka browser ke `http://<ip-server>:5010`

## Penggunaan
- Semua kontrol Mihomo bisa dilakukan dari web (start/stop/restart, clear log, edit config, dsb)
- Untuk keamanan, sebaiknya batasi akses port 5010 hanya dari IP tertentu (gunakan firewall/reverse proxy jika perlu)

## Konfigurasi Lanjutan
- **Port WebUI:**
  Edit file `mihomo_web_interface.py` bagian `app.run(host='0.0.0.0', port=5010, ...)` jika ingin ganti port.
- **Lokasi config.yaml:**
  Default: `/etc/mihomo/config.yaml`. Bisa diubah di backend jika perlu.
- **Autostart Mihomo:**
  Atur langsung dari WebUI (enable/disable systemd autostart)

## Uninstall
```bash
sudo systemctl stop mihomo-webui
sudo systemctl disable mihomo-webui
sudo rm /etc/systemd/system/mihomo-webui.service
sudo systemctl daemon-reload
```

## Kontribusi
Pull request & issue sangat diterima!

## Lisensi
MIT 