from flask import Flask, render_template_string, jsonify, request as flask_request
import subprocess

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
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: #f4f6fb;
                margin: 0;
                padding: 0;
                transition: background 0.3s, color 0.3s;
            }
            .dark-mode body {
                background: #181c23;
                color: #e0e0e0;
            }
            .container {
                max-width: 400px;
                margin: 60px auto 20px auto;
                background: #fff;
                border-radius: 12px;
                box-shadow: 0 4px 16px rgba(0,0,0,0.08);
                padding: 32px 24px 24px 24px;
                text-align: center;
                transition: background 0.3s, color 0.3s;
            }
            .dark-mode .container {
                background: #23272f;
                color: #e0e0e0;
            }
            h1 {
                color: #2d3a4b;
                margin-bottom: 16px;
            }
            .dark-mode h1 {
                color: #e0e0e0;
            }
            p {
                font-size: 1.1em;
                margin-bottom: 24px;
                color: #444;
            }
            .dark-mode p {
                color: #e0e0e0;
            }
            .status-running {
                color: #27ae60;
                font-weight: bold;
            }
            .status-stopped {
                color: #e74c3c;
                font-weight: bold;
            }
            .button-group {
                margin-bottom: 18px;
            }
            button, .config-btn {
                background: #2d3a4b;
                color: #fff;
                border: none;
                border-radius: 6px;
                padding: 10px 22px;
                font-size: 1em;
                cursor: pointer;
                transition: background 0.2s;
                margin: 0 8px 12px 8px;
            }
            button:hover, .config-btn:hover {
                background: #1a222c;
            }
            .dark-mode button, .dark-mode .config-btn {
                background: #444b5a;
                color: #fff;
            }
            .notif {
                margin: 0 auto 16px auto;
                padding: 10px 18px;
                border-radius: 6px;
                font-size: 1em;
                display: none;
                max-width: 350px;
            }
            .notif-success {
                background: #eafaf1;
                color: #27ae60;
                border: 1px solid #b7e4c7;
            }
            .notif-error {
                background: #fff0f0;
                color: #e74c3c;
                border: 1px solid #f5b7b1;
            }
            .dark-mode .notif-success {
                background: #1e2d24;
                color: #27ae60;
                border: 1px solid #27ae60;
            }
            .dark-mode .notif-error {
                background: #2d1e1e;
                color: #e74c3c;
                border: 1px solid #e74c3c;
            }
            .log-container {
                max-width: 800px;
                margin: 0 auto 40px auto;
                background: #222;
                color: #e0e0e0;
                border-radius: 8px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.10);
                padding: 18px 16px;
                font-family: 'Fira Mono', 'Consolas', monospace;
                font-size: 0.98em;
                height: 320px;
                overflow-y: auto;
                white-space: pre-wrap;
                text-align: left;
                transition: background 0.3s, color 0.3s;
            }
            .dark-mode .log-container {
                background: #181c23;
                color: #e0e0e0;
            }
            .log-title {
                color: #2d3a4b;
                margin: 0 0 8px 0;
                font-size: 1.1em;
                font-weight: bold;
            }
            .dark-mode .log-title {
                color: #e0e0e0;
            }
            .config-section {
                max-width: 800px;
                margin: 32px auto 0 auto;
                background: #fff;
                border-radius: 10px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.08);
                padding: 24px 20px 20px 20px;
                transition: background 0.3s, color 0.3s;
            }
            .dark-mode .config-section {
                background: #23272f;
                color: #e0e0e0;
            }
            .config-title {
                color: #2d3a4b;
                font-size: 1.1em;
                font-weight: bold;
                margin-bottom: 10px;
            }
            .dark-mode .config-title {
                color: #e0e0e0;
            }
            .config-upload {
                margin-bottom: 18px;
            }
            .config-editor {
                width: 100%;
                min-height: 220px;
                font-family: 'Fira Mono', 'Consolas', monospace;
                font-size: 1em;
                border-radius: 6px;
                border: 1px solid #bbb;
                padding: 10px;
                margin-bottom: 10px;
                background: #f8f9fa;
                color: #222;
                resize: vertical;
                transition: background 0.3s, color 0.3s;
            }
            .dark-mode .config-editor {
                background: #23272f;
                color: #e0e0e0;
                border: 1px solid #444b5a;
            }
            .stats-section {
                max-width: 800px;
                margin: 24px auto 0 auto;
                background: #fff;
                border-radius: 10px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.08);
                padding: 18px 20px 14px 20px;
                color: #222;
                font-size: 1.04em;
            }
            .dark-mode .stats-section {
                background: #23272f;
                color: #e0e0e0;
            }
            .stats-title {
                color: #2d3a4b;
                font-size: 1.08em;
                font-weight: bold;
                margin-bottom: 8px;
            }
            .dark-mode .stats-title {
                color: #e0e0e0;
            }
            .stats-list {
                margin: 0;
                padding: 0;
                list-style: none;
            }
            .stats-list li {
                margin-bottom: 4px;
            }
            .autostart-section {
                max-width: 800px;
                margin: 18px auto 0 auto;
                background: #fff;
                border-radius: 10px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.08);
                padding: 14px 20px 10px 20px;
                color: #222;
                font-size: 1.04em;
                display: flex;
                align-items: center;
                justify-content: space-between;
            }
            .dark-mode .autostart-section {
                background: #23272f;
                color: #e0e0e0;
            }
            .autostart-status {
                font-weight: bold;
                margin-right: 16px;
            }
            .autostart-btn {
                background: #2d3a4b;
                color: #fff;
                border: none;
                border-radius: 6px;
                padding: 7px 18px;
                font-size: 1em;
                cursor: pointer;
                margin-left: 8px;
            }
            .autostart-btn:hover {
                background: #1a222c;
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
            window.onload = function() {
                updateStatus();
                updateLog();
                fetchConfig();
                updateStats();
                updateAutostart();
                // Set dark mode dari localStorage
                if (localStorage.getItem('mihomo-darkmode') === '1') {
                    setDarkMode(true);
                    document.getElementById('darkmode-toggle').checked = true;
                }
            };
        </script>
    </head>
    <body>
        <div class="container">
            <h1>Mihomo Web Interface</h1>
            <div style="text-align:right; margin-bottom:10px;">
                <label style="font-size:0.98em; cursor:pointer;">
                    <input type="checkbox" id="darkmode-toggle" onclick="toggleDarkMode()" style="vertical-align:middle; margin-right:6px;"> Dark Mode
                </label>
            </div>
            <div id="notif" class="notif"></div>
            <p>Status: <span id="status-span" class="{{ 'status-running' if status == 'Mihomo is running' else 'status-stopped' }}">{{ status }}</span></p>
            <div class="button-group">
                <button onclick="startMihomo()">Start Mihomo</button>
                <button onclick="stopMihomo()">Stop Mihomo</button>
                <button onclick="restartMihomo()">Restart Mihomo</button>
                <button onclick="clearLog()">Clear Log</button>
            </div>
        </div>
        <div class="autostart-section">
            <span class="autostart-status" id="autostart-status">-</span>
            <button class="autostart-btn" id="autostart-btn">...</button>
        </div>
        <div class="stats-section">
            <div class="stats-title">Statistik Mihomo</div>
            <ul class="stats-list">
                <li><b>Status:</b> <span id="stat-active">-</span></li>
                <li><b>Uptime:</b> <span id="stat-uptime">-</span></li>
                <li><b>Waktu Aktif Sejak:</b> <span id="stat-activesince">-</span></li>
                <li><b>Waktu Start Terakhir:</b> <span id="stat-laststart">-</span></li>
            </ul>
        </div>
        <div class="log-container">
            <div class="log-title">Log Mihomo (real-time)</div>
            <div id="log-box" style="height:260px; overflow-y:auto; background:transparent;"></div>
        </div>
        <div class="config-section">
            <div class="config-title">Config Mihomo (config.yaml)</div>
            <div class="config-upload">
                <input type="file" id="config-upload" accept=".yaml,.yml" />
                <button class="config-btn" onclick="uploadConfig()">Upload Config</button>
            </div>
            <textarea id="config-editor" class="config-editor" spellcheck="false"></textarea><br>
            <button class="config-btn" onclick="saveConfig()">Simpan Config</button>
            <button class="config-btn" onclick="fetchConfig()">Reload Config</button>
        </div>
    </body>
    </html>
    """
    return render_template_string(html, status=status_message)


# Rute untuk memulai Mihomo
@app.route('/start', methods=['POST'])
def start():
    subprocess.run(['sudo', 'systemctl', 'start', 'mihomo'])
    subprocess.run(['sudo', 'journalctl', '--rotate'])
    subprocess.run(['sudo', 'journalctl', '--vacuum-time=1s'])
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
    subprocess.run(['sudo', 'systemctl', 'restart', 'mihomo'])
    subprocess.run(['sudo', 'journalctl', '--rotate'])
    subprocess.run(['sudo', 'journalctl', '--vacuum-time=1s'])
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

# Jalankan aplikasi web Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5010, debug=True)

