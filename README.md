# <img src="https://raw.githubusercontent.com/latifangren/mihomo-webui/main/logo-mihomo.png" alt="Mihomo WebUI" width="40" style="vertical-align:middle;"> Mihomo WebUI

WebUI minimalis & modern untuk mengelola layanan Clash Meta Mihomo di server Linux/Ubuntu.

---

![Python](https://img.shields.io/badge/Python-3.7%2B-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-WebUI-green?logo=flask)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## 🚀 **Fitur Utama**
- ⚡️ Kontrol layanan Mihomo: Start, Stop, Restart
- 👀 Status Mihomo real-time
- 📜 Log Mihomo real-time (systemd journal)
- 🧹 Clear log Mihomo
- 📝 Upload & edit config.yaml langsung dari web
- 📊 Statistik uptime, waktu aktif, dsb
- 🌙 Dark mode
- 🔔 Notifikasi status aksi
- 🔄 Konfigurasi autostart Mihomo (enable/disable systemd)
- 📱 Tampilan responsif & mudah digunakan

---

## 📦 **Prasyarat**
- 🐍 **Python 3.7+**
- ⚙️ Mihomo sudah terinstall & berjalan sebagai service systemd (`mihomo.service`)  
  ⚠️ *Jika belum ada, silakan install dulu dengan script di bawah!*
- 👤 User punya akses **sudo** (untuk kontrol service & log)

---

## 🛠️ **Install Mihomo (Core) Otomatis**
Script `install_mihomo.sh` akan otomatis menginstall Mihomo **versi terbaru** dari Github, setup config, log, dan systemd service.

```bash
curl -O https://raw.githubusercontent.com/latifangren/mihomo-webui/main/install_mihomo.sh
chmod +x install_mihomo.sh
./install_mihomo.sh
```

- 📄 Config: `/etc/mihomo/config.yaml`
- 🗂️ Log: `/var/log/mihomo/mihomo.log`
- 🛡️ Service: `mihomo` (systemd)

---

## 🌐 **Install & Setup WebUI Mihomo**
> 💡 **Tips:** Jalankan semua perintah di bawah ini dari direktori tempat Anda ingin menyimpan folder `mihomo-webui`.

### **1. Install WebUI cukup dengan satu perintah:**
```bash
curl -O https://raw.githubusercontent.com/latifangren/mihomo-webui/main/install.sh
chmod +x install.sh
./install.sh
```
> Script `install.sh` akan otomatis:
> - Mengecek apakah folder sudah ada
> - Menawarkan opsi hapus, rename, atau batal jika folder sudah ada
> - Clone repo jika folder belum ada
> - Masuk ke folder, menjalankan setup, dan WebUI siap digunakan

### **2. Akses WebUI:**
Buka browser ke:  
`http://<ip-server>:5010`

---

## ⚠️ **Penting!**
- **Jangan jalankan script di direktori root (`/`)**. Selalu gunakan home user atau direktori kerja yang benar.
- **Pastikan port 5010 terbuka** di firewall/server agar bisa diakses dari luar.
- **Jika menambah library Python baru, install juga di venv!**

---

## ⚙️ **Konfigurasi Lanjutan**
- **Port WebUI:**  
  Edit file `mihomo_web_interface.py` bagian `app.run(host='0.0.0.0', port=5010, ...)` jika ingin ganti port.
- **Lokasi config.yaml:**  
  Default: `/etc/mihomo/config.yaml`. Bisa diubah di backend jika perlu.
- **Autostart Mihomo:**  
  Atur langsung dari WebUI (enable/disable systemd autostart)

---

## 🧹 **Uninstall**
```bash
sudo systemctl stop mihomo-webui
sudo systemctl disable mihomo-webui
sudo rm /etc/systemd/system/mihomo-webui.service
sudo systemctl daemon-reload
```

---

## 🤝 **Kontribusi**
Pull request & issue sangat diterima!

---

## 📄 **Lisensi**
MIT 