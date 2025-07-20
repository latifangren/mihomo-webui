from flask import Flask, render_template_string, jsonify, request as flask_request
import subprocess
import os
import yaml

app = Flask(__name__)

# Halaman utama yang menampilkan status Mihomo
@app.route('/')
def index():
    # Periksa status Mihomo
    status = subprocess.run(['systemctl', 'is-active', '--quiet', 'mihomo'], capture_output=True, text=True)
    if status.returncode == 0:
        status_message = "Mihomo is running"
    else:
        status_message = "Mihomo is stopped"
    
    # Template HTML untuk menampilkan status
    html = """
    <html>
    <head>
        <title>Mihomo Web Interface</title>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
        <style>
            :root {
                --primary-yellow: #FECA0A;
                --primary-yellow2: #FFD600;
                --bg-main: #000;
                --bg-card: #1a1a1a;
                --bg-log: #111;
                --text-main: #F1F1F1;
                --text-secondary: #aaaaaa;
                --border: #333;
                --shadow: rgba(0,0,0,0.18);
                --success: #27ae60;
                --danger: #F44336;
                --info: #2196F3;
                --white: #fff;
            }
            body {
                font-family: 'Inter', Arial, sans-serif;
                background: var(--bg-main);
                margin: 0;
                padding: 0;
                color: var(--text-main);
            }
            .header {
                display: flex;
                flex-direction: column;
                align-items: center;
                background: var(--bg-card);
                color: var(--primary-yellow);
                padding: 28px 0 18px 0;
                box-shadow: 0 4px 16px var(--shadow);
                margin-bottom: 18px;
                border-bottom: 2px solid var(--primary-yellow);
            }
            .header h1 {
                font-size: 2em;
                font-weight: 700;
                margin: 0 0 6px 0;
                letter-spacing: 1px;
                color: var(--primary-yellow);
                text-shadow: 0 2px 8px #0008;
            }
            .header .subtitle {
                font-size: 1em;
                font-weight: 400;
                opacity: 0.85;
                color: var(--text-secondary);
            }
            .container {
                max-width: 900px;
                margin: 0 auto;
                padding: 0 10px;
            }
            .card {
                background: var(--bg-card);
                border-radius: 12px;
                box-shadow: 0 2px 10px var(--shadow);
                margin-bottom: 18px;
                padding: 22px 16px 16px 16px;
                border: 1px solid var(--border);
            }
            .card:last-child { margin-bottom: 0; }
            .status-row {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
                gap: 10px;
                margin-bottom: 14px;
            }
            .status-label {
                font-size: 1.08em;
                font-weight: 600;
                color: var(--primary-yellow);
            }
            .status-running {
                color: var(--success);
                font-weight: bold;
            }
            .status-stopped {
                color: var(--danger);
                font-weight: bold;
            }
            .button-group {
                margin-bottom: 10px;
                display: flex;
                flex-wrap: wrap;
                gap: 10px;
            }
            button, .config-btn, .autostart-btn, .external-ui-btn {
                background: var(--bg-main);
                color: var(--primary-yellow);
                border: 2px solid var(--primary-yellow);
                border-radius: 22px;
                padding: 12px 28px;
                font-size: 1.08em;
                font-weight: 600;
                cursor: pointer;
                transition: background 0.2s, color 0.2s, box-shadow 0.2s;
                box-shadow: 0 2px 8px var(--shadow);
                display: flex;
                align-items: center;
                gap: 8px;
                outline: none;
            }
            .btn-start { color: var(--white); background: var(--success); border-color: var(--success); }
            .btn-start:hover { background: var(--white); color: var(--success); }
            .btn-stop { color: var(--white); background: var(--danger); border-color: var(--danger); }
            .btn-stop:hover { background: var(--white); color: var(--danger); }
            .btn-restart { color: var(--white); background: var(--info); border-color: var(--info); }
            .btn-restart:hover { background: var(--white); color: var(--info); }
            .btn-clear { color: var(--bg-main); background: var(--primary-yellow2); border-color: var(--primary-yellow2); }
            .btn-clear:hover { background: var(--white); color: var(--primary-yellow2); }
            .external-ui-info {
                margin: 0 auto 12px auto;
                max-width: 800px;
                text-align: center;
                font-size: 1.08em;
            }
            .external-ui-btn {
                margin-left: 10px;
                font-size: 1em;
                padding: 10px 22px;
            }
            .autostart-section, .stats-section, .log-container, .config-section {
                margin-bottom: 16px;
            }
            .autostart-section, .stats-section {
                background: var(--bg-card);
                border-radius: 10px;
                padding: 14px 14px 8px 14px;
                color: var(--primary-yellow2);
                font-size: 1.01em;
                display: flex;
                align-items: center;
                justify-content: space-between;
                box-shadow: 0 1px 4px var(--shadow);
                border: 1px solid var(--primary-yellow2);
            }
            .stats-title {
                color: var(--primary-yellow2);
                font-size: 1.05em;
                font-weight: bold;
                margin-bottom: 8px;
            }
            .stats-list {
                margin: 0;
                padding: 0;
                list-style: none;
            }
            .stats-list li {
                margin-bottom: 4px;
            }
            .log-container {
                background: var(--bg-log);
                color: var(--white);
                border-radius: 10px;
                box-shadow: 0 2px 8px var(--shadow);
                padding: 12px 10px;
                font-family: 'Fira Mono', 'Consolas', monospace;
                font-size: 0.98em;
                height: 220px;
                overflow-y: auto;
                white-space: pre-wrap;
                text-align: left;
                border: 1px solid var(--primary-yellow2);
            }
            .log-title {
                color: var(--primary-yellow2);
                margin: 0 0 8px 0;
                font-size: 1.05em;
                font-weight: bold;
            }
            .config-section {
                background: var(--bg-card);
                border-radius: 10px;
                box-shadow: 0 2px 8px var(--shadow);
                padding: 18px 14px 14px 14px;
                border: 1px solid var(--primary-yellow2);
            }
            .config-title {
                color: var(--primary-yellow2);
                font-size: 1.05em;
                font-weight: bold;
                margin-bottom: 10px;
            }
            .config-upload {
                margin-bottom: 12px;
            }
            .config-editor {
                width: 100%;
                min-height: 160px;
                font-family: 'Fira Mono', 'Consolas', monospace;
                font-size: 1em;
                border-radius: 8px;
                border: 1.5px solid var(--primary-yellow2);
                padding: 8px;
                margin-bottom: 10px;
                background: var(--bg-log);
                color: var(--white);
                resize: vertical;
                transition: background 0.3s, color 0.3s;
            }
            .notif {
                position: fixed;
                top: 24px;
                right: 24px;
                z-index: 9999;
                min-width: 220px;
                max-width: 350px;
                padding: 14px 22px;
                border-radius: 8px;
                font-size: 1.08em;
                font-weight: 600;
                display: none;
                box-shadow: 0 4px 16px var(--primary-yellow2);
            }
            .notif-success {
                background: var(--bg-card);
                color: var(--success);
                border: 1.5px solid var(--success);
            }
            .notif-error {
                background: #2d1e1e;
                color: var(--danger);
                border: 1.5px solid var(--danger);
            }
            @media (max-width: 700px) {
                .container, .header, .card, .autostart-section, .stats-section, .log-container, .config-section {
                    padding-left: 4px !important;
                    padding-right: 4px !important;
                }
                .header h1 { font-size: 1.1em; }
                .button-group { flex-direction: column; gap: 8px; }
            }
        </style>
        <script>
            function updateStatus() {
                fetch('/api/status')
                    .then(response => response.json())
                    .then(data => {
                        const statusText = data.status === 'running' ? 'Mihomo is running' : 'Mihomo is stopped';
                        const statusClass = data.status === 'running' ? 'status-running' : 'status-stopped';
                        const statusSpan = document.getElementById('status-span');
                        statusSpan.textContent = statusText;
                        statusSpan.className = statusClass;
                    });
            }
            setInterval(updateStatus, 3000);

            function updateLog() {
                fetch('/api/log')
                    .then(response => response.text())
                    .then(data => {
                        const logBox = document.getElementById('log-box');
                        logBox.textContent = data;
                        logBox.scrollTop = logBox.scrollHeight;
                    });
            }
            setInterval(updateLog, 3000);

            function showNotif(msg, isSuccess) {
                const notif = document.getElementById('notif');
                notif.textContent = msg;
                notif.className = 'notif ' + (isSuccess ? 'notif-success' : 'notif-error');
                notif.style.display = 'block';
                setTimeout(() => { notif.style.display = 'none'; }, 3000);
            }

            function startMihomo() {
                fetch('/start', {method: 'POST'})
                    .then(response => response.text())
                    .then(data => {
                        showNotif('Mihomo is starting...', true);
                        setTimeout(updateStatus, 1000);
                    })
                    .catch(() => showNotif('Gagal menjalankan Mihomo!', false));
            }
            function stopMihomo() {
                fetch('/stop', {method: 'POST'})
                    .then(response => response.text())
                    .then(data => {
                        showNotif('Mihomo is stopping...', true);
                        setTimeout(updateStatus, 1000);
                    })
                    .catch(() => showNotif('Gagal menghentikan Mihomo!', false));
            }
            function restartMihomo() {
                fetch('/restart', {method: 'POST'})
                    .then(response => {
                        if (response.status === 204) {
                            showNotif('Mihomo is restarting...', true);
                            setTimeout(updateStatus, 1000);
                        } else {
                            showNotif('Gagal restart Mihomo!', false);
                        }
                    })
                    .catch(() => showNotif('Gagal restart Mihomo!', false));
            }
            function clearLog() {
                fetch('/clear_log', {method: 'POST'})
                    .then(response => {
                        if (response.status === 204) {
                            showNotif('Log Mihomo berhasil dihapus.', true);
                            setTimeout(updateLog, 1000);
                        } else {
                            response.text().then(msg => showNotif(msg, false));
                        }
                    })
                    .catch(() => showNotif('Gagal menghapus log!', false));
            }
            function fetchConfig() {
                fetch('/get_config')
                    .then(response => response.text())
                    .then(data => {
                        document.getElementById('config-editor').value = data;
                    });
            }
            function saveConfig() {
                const content = document.getElementById('config-editor').value;
                const formData = new FormData();
                formData.append('content', content);
                fetch('/edit_config', {method: 'POST', body: formData})
                    .then(response => {
                        if (response.status === 204) {
                            showNotif('Config.yaml berhasil disimpan.', true);
                        } else {
                            response.text().then(msg => showNotif(msg, false));
                        }
                    })
                    .catch(() => showNotif('Gagal menyimpan config.yaml!', false));
            }
            function uploadConfig() {
                const fileInput = document.getElementById('config-upload');
                if (!fileInput.files.length) return;
                const formData = new FormData();
                formData.append('config', fileInput.files[0]);
                fetch('/upload_config', {method: 'POST', body: formData})
                    .then(response => {
                        if (response.status === 204) {
                            showNotif('Config.yaml berhasil di-upload.', true);
                            fetchConfig();
                        } else {
                            response.text().then(msg => showNotif(msg, false));
                        }
                    })
                    .catch(() => showNotif('Gagal upload config.yaml!', false));
            }
            function setDarkMode(enabled) {
                if (enabled) {
                    document.documentElement.classList.add('dark-mode');
                    localStorage.setItem('mihomo-darkmode', '1');
                } else {
                    document.documentElement.classList.remove('dark-mode');
                    localStorage.setItem('mihomo-darkmode', '0');
                }
                // force update log/config colors
            }
            function toggleDarkMode() {
                const enabled = !document.documentElement.classList.contains('dark-mode');
                setDarkMode(enabled);
            }
            function updateStats() {
                fetch('/api/stats')
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById('stat-uptime').textContent = data.uptime || '-';
                        document.getElementById('stat-laststart').textContent = data.last_start || '-';
                        document.getElementById('stat-active').textContent = data.active_state || '-';
                        document.getElementById('stat-activesince').textContent = data.active_since || '-';
                    });
            }
            setInterval(updateStats, 3000);
            function updateAutostart() {
                fetch('/api/autostart')
                    .then(response => response.json())
                    .then(data => {
                        const statusSpan = document.getElementById('autostart-status');
                        const btn = document.getElementById('autostart-btn');
                        if (data.enabled) {
                            statusSpan.textContent = 'Aktif (enabled)';
                            statusSpan.style.color = '#27ae60';
                            btn.textContent = 'Nonaktifkan Autostart';
                            btn.onclick = disableAutostart;
                        } else {
                            statusSpan.textContent = 'Tidak Aktif (disabled)';
                            statusSpan.style.color = '#e74c3c';
                            btn.textContent = 'Aktifkan Autostart';
                            btn.onclick = enableAutostart;
                        }
                    });
            }
            function enableAutostart() {
                const formData = new FormData();
                formData.append('action', 'enable');
                fetch('/api/autostart', {method: 'POST', body: formData})
                    .then(response => {
                        if (response.status === 204) {
                            showNotif('Autostart Mihomo berhasil diaktifkan.', true);
                            updateAutostart();
                        } else {
                            response.text().then(msg => showNotif(msg, false));
                        }
                    })
                    .catch(() => showNotif('Gagal mengaktifkan autostart!', false));
            }
            function disableAutostart() {
                const formData = new FormData();
                formData.append('action', 'disable');
                fetch('/api/autostart', {method: 'POST', body: formData})
                    .then(response => {
                        if (response.status === 204) {
                            showNotif('Autostart Mihomo berhasil dinonaktifkan.', true);
                            updateAutostart();
                        } else {
                            response.text().then(msg => showNotif(msg, false));
                        }
                    })
                    .catch(() => showNotif('Gagal menonaktifkan autostart!', false));
            }
            function updateExternalUiInfo() {
                fetch('/api/external_ui_url')
                    .then(response => response.json())
                    .then(data => {
                        const url = data.url;
                        document.getElementById('external-ui-link').href = url;
                        document.getElementById('external-ui-link').textContent = url;
                    });
            }
            window.onload = function() {
                updateStatus();
                updateLog();
                fetchConfig();
                updateStats();
                updateAutostart();
                updateExternalUiInfo();
                // Set dark mode dari localStorage
                if (localStorage.getItem('mihomo-darkmode') === '1') {
                    setDarkMode(true);
                    document.getElementById('darkmode-toggle').checked = true;
                }
            };
        </script>
    </head>
    <body>
        <div class="header">
            <h1>🚀 Mihomo Web Interface</h1>
            <div class="subtitle">Kelola layanan Clash Meta Mihomo dengan mudah & modern</div>
        </div>
        <div class="container">
            <div class="card">
                <div class="status-row">
                    <span class="status-label">Status Mihomo:</span>
                    <span id="status-span" class="{{ 'status-running' if status == 'Mihomo is running' else 'status-stopped' }}">{{ status }}</span>
                </div>
                <div class="button-group">
                    <button onclick="startMihomo()" class="btn-start">▶️ Start</button>
                    <button onclick="stopMihomo()" class="btn-stop">⏹️ Stop</button>
                    <button onclick="restartMihomo()" class="btn-restart">🔄 Restart</button>
                    <button onclick="clearLog()" class="btn-clear">🧹 Clear Log</button>
                </div>
            </div>
            <div class="external-ui-info card">
                <span>🌐 UI External Mihomo:</span>
                <a id="external-ui-link" class="external-ui-btn" href="#" target="_blank">Buka UI Mihomo</a>
            </div>
            <div class="autostart-section card">
                <span class="autostart-status" id="autostart-status">-</span>
                <button class="autostart-btn" id="autostart-btn">...</button>
            </div>
            <div class="stats-section card">
                <div class="stats-title">📊 Statistik Mihomo</div>
                <ul class="stats-list">
                    <li><b>Status:</b> <span id="stat-active">-</span></li>
                    <li><b>Uptime:</b> <span id="stat-uptime">-</span></li>
                    <li><b>Waktu Aktif Sejak:</b> <span id="stat-activesince">-</span></li>
                    <li><b>Waktu Start Terakhir:</b> <span id="stat-laststart">-</span></li>
                </ul>
            </div>
            <div class="log-container card">
                <div class="log-title">📝 Log Mihomo (real-time)</div>
                <div id="log-box" style="height:260px; overflow-y:auto; background:transparent;"></div>
            </div>
            <div class="config-section card">
                <div class="config-title">⚙️ Config Mihomo (config.yaml)</div>
                <div class="config-upload">
                    <input type="file" id="config-upload" accept=".yaml,.yml" />
                    <button class="config-btn" onclick="uploadConfig()">⬆️ Upload Config</button>
                </div>
                <textarea id="config-editor" class="config-editor" spellcheck="false"></textarea><br>
                <button class="config-btn" onclick="saveConfig()">💾 Simpan Config</button>
                <button class="config-btn" onclick="fetchConfig()">🔄 Reload Config</button>
            </div>
        </div>
        <div id="notif" class="notif"></div>
    </body>
    </html>
    """
    return render_template_string(html, status=status_message)


# Rute untuk memulai Mihomo
@app.route('/start', methods=['POST'])
def start():
    subprocess.run(['sudo', 'journalctl', '--rotate'])
    subprocess.run(['sudo', 'journalctl', '--vacuum-time=1s'])
    subprocess.run(['sudo', 'systemctl', 'start', 'mihomo'])
    # Cek status Mihomo
    status = subprocess.run(['systemctl', 'is-active', '--quiet', 'mihomo'])
    if status.returncode == 0:
        return '', 204
    else:
        return 'Gagal menjalankan Mihomo!', 500

# Rute untuk menghentikan Mihomo
@app.route('/stop', methods=['POST'])
def stop():
    subprocess.run(['sudo', 'systemctl', 'stop', 'mihomo'])
    return "Mihomo is stopping... <br> <a href='/'>Go Back</a>"

# Rute untuk me-restart Mihomo
@app.route('/restart', methods=['POST'])
def restart():
    subprocess.run(['sudo', 'journalctl', '--rotate'])
    subprocess.run(['sudo', 'journalctl', '--vacuum-time=1s'])
    subprocess.run(['sudo', 'systemctl', 'restart', 'mihomo'])
    # Cek status Mihomo
    status = subprocess.run(['systemctl', 'is-active', '--quiet', 'mihomo'])
    if status.returncode == 0:
        return '', 204
    else:
        return 'Gagal restart Mihomo!', 500

# Rute untuk clear log Mihomo (systemd journal)
@app.route('/clear_log', methods=['POST'])
def clear_log():
    try:
        # Rotate dan vacuum log Mihomo
        subprocess.run(['sudo', 'journalctl', '--rotate'], check=True)
        subprocess.run(['sudo', 'journalctl', '--vacuum-time=1s'], check=True)
        return '', 204
    except Exception as e:
        return f'Gagal menghapus log: {e}', 500

# Rute untuk memeriksa status Mihomo
@app.route('/status', methods=['GET'])
def check_status():
    status = subprocess.run(['systemctl', 'is-active', '--quiet', 'mihomo'], capture_output=True, text=True)
    if status.returncode == 0:
        return "Mihomo is running <br> <a href='/'>Go Back</a>"
    else:
        return "Mihomo is stopped <br> <a href='/'>Go Back</a>"

# Endpoint API untuk status Mihomo (JSON)
@app.route('/api/status', methods=['GET'])
def api_status():
    status = subprocess.run(['systemctl', 'is-active', '--quiet', 'mihomo'], capture_output=True, text=True)
    if status.returncode == 0:
        return jsonify({"status": "running"})
    else:
        return jsonify({"status": "stopped"})

# Endpoint API untuk mengambil 200 baris terakhir log Mihomo dari systemd journal
@app.route('/api/log', methods=['GET'])
def api_log():
    try:
        result = subprocess.run(['journalctl', '-u', 'mihomo', '--no-pager', '-n', '200'], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout, 200, {'Content-Type': 'text/plain; charset=utf-8'}
        else:
            return f'Gagal membaca log: {result.stderr}', 500, {'Content-Type': 'text/plain; charset=utf-8'}
    except Exception as e:
        return f'Gagal membaca log: {e}', 500, {'Content-Type': 'text/plain; charset=utf-8'}

# Endpoint API untuk statistik Mihomo (uptime, waktu terakhir start)
@app.route('/api/stats', methods=['GET'])
def api_stats():
    try:
        # Ambil info dari systemctl show
        result = subprocess.run(['systemctl', 'show', 'mihomo', '--property=ActiveEnterTimestamp,ActiveState,ExecMainStartTimestamp,ExecMainPID'], capture_output=True, text=True)
        lines = result.stdout.splitlines()
        stats = {}
        for line in lines:
            if '=' in line:
                k, v = line.split('=', 1)
                stats[k] = v
        # Hitung uptime jika PID ada
        uptime = ''
        if stats.get('ExecMainPID') and stats.get('ExecMainPID') != '0':
            try:
                pid = stats['ExecMainPID']
                with open(f'/proc/{pid}/stat', 'r') as f:
                    fields = f.read().split()
                    start_time_ticks = int(fields[21])
                import os
                import time
                clk_tck = os.sysconf(os.sysconf_names['SC_CLK_TCK'])
                boot_time = 0
                with open('/proc/stat', 'r') as f:
                    for line in f:
                        if line.startswith('btime'):
                            boot_time = int(line.strip().split()[1])
                            break
                start_time = boot_time + (start_time_ticks // clk_tck)
                uptime_sec = int(time.time()) - start_time
                hours = uptime_sec // 3600
                minutes = (uptime_sec % 3600) // 60
                seconds = uptime_sec % 60
                uptime = f"{hours}h {minutes}m {seconds}s"
            except Exception:
                uptime = ''
        return jsonify({
            'active_state': stats.get('ActiveState', ''),
            'active_since': stats.get('ActiveEnterTimestamp', ''),
            'last_start': stats.get('ExecMainStartTimestamp', ''),
            'uptime': uptime
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Endpoint API untuk cek dan atur autostart Mihomo
@app.route('/api/autostart', methods=['GET', 'POST'])
def api_autostart():
    if flask_request.method == 'GET':
        # Cek status enable/disable
        result = subprocess.run(['systemctl', 'is-enabled', 'mihomo'], capture_output=True, text=True)
        status = result.stdout.strip()
        return jsonify({'enabled': status == 'enabled', 'raw': status})
    else:
        # POST: enable/disable
        action = flask_request.form.get('action', '')
        if action == 'enable':
            result = subprocess.run(['sudo', 'systemctl', 'enable', 'mihomo'], capture_output=True, text=True)
            if result.returncode == 0:
                return '', 204
            else:
                return result.stderr, 500
        elif action == 'disable':
            result = subprocess.run(['sudo', 'systemctl', 'disable', 'mihomo'], capture_output=True, text=True)
            if result.returncode == 0:
                return '', 204
            else:
                return result.stderr, 500
        else:
            return 'Invalid action', 400

# Endpoint untuk upload config.yaml
@app.route('/upload_config', methods=['POST'])
def upload_config():
    if 'config' not in flask_request.files:
        return 'No file part', 400
    file = flask_request.files['config']
    if file.filename == '':
        return 'No selected file', 400
    if file:
        file.save('/etc/mihomo/config.yaml')
        return '', 204
    return 'Upload failed', 400

# Endpoint untuk mengambil isi config.yaml
@app.route('/get_config', methods=['GET'])
def get_config():
    try:
        with open('/etc/mihomo/config.yaml', 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        return content, 200, {'Content-Type': 'text/plain; charset=utf-8'}
    except Exception as e:
        return f'Gagal membaca config: {e}', 500

# Endpoint untuk edit config.yaml (POST, menerima teks)
@app.route('/edit_config', methods=['POST'])
def edit_config():
    try:
        new_content = flask_request.form.get('content', '')
        with open('/etc/mihomo/config.yaml', 'w', encoding='utf-8') as f:
            f.write(new_content)
        return '', 204
    except Exception as e:
        return f'Gagal menyimpan config: {e}', 500

EXTERNAL_UI_FILE = os.path.join(os.path.dirname(__file__), 'external_ui_url.txt')

def get_external_ui_url():
    if os.path.exists(EXTERNAL_UI_FILE):
        with open(EXTERNAL_UI_FILE, 'r') as f:
            return f.read().strip()
    return "http://192.168.100.50:9090/ui/"  # default

def set_external_ui_url(url):
    with open(EXTERNAL_UI_FILE, 'w') as f:
        f.write(url.strip())

@app.route('/api/external_ui_url', methods=['GET'])
def api_external_ui_url():
    # Baca config.yaml Mihomo
    config_path = '/etc/mihomo/config.yaml'
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        ext_ctrl = config.get('external-controller', '0.0.0.0:9090')
        ext_ui = config.get('external-ui', './ui')
        # Ambil port dari external-controller
        port = ext_ctrl.split(':')[-1]
        # Asumsi path UI: /ui/ (atau dari ext_ui jika ingin lebih dinamis)
        url = f"http://{flask_request.host.split(':')[0]}:{port}/ui/"
        return jsonify({'url': url})
    except Exception as e:
        # Jika gagal, fallback ke default
        return jsonify({'url': 'http://127.0.0.1:9090/ui/', 'error': str(e)}), 200

# Jalankan aplikasi web Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5010, debug=True)

