from flask import Flask, request, jsonify, render_template_string
from threading import Lock
from datetime import datetime, timedelta

app = Flask(__name__)
alert_log = []
log_lock = Lock()
pinned_red = None
pinned_time = None
PINNED_TIMEOUT_SECONDS = 120

HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <title>LineAlert Dashboard</title>
    <style>
        body { background-color: #f4f4f4; font-family: Arial, sans-serif; color: #222; padding: 20px; }
        h1 { color: #003366; }
        .view-toggle { margin-bottom: 10px; }
        .log { white-space: pre-wrap; background: #fff; padding: 10px; border-left: 5px solid #ccc; margin-bottom: 10px; border-radius: 4px; font-size: 1.2em; cursor: pointer; }
        .green { border-left-color: green; }
        .yellow { border-left-color: goldenrod; }
        .red { border-left-color: red; font-weight: bold; }
        .pinned { background: #ffe6e6; border-left: 5px solid red; padding: 10px; margin-bottom: 20px; font-weight: bold; font-size: 1.4em; }

        #red-alert-indicator {
            position: fixed;
            top: 20px;
            right: 20px;
            width: 30px;
            height: 30px;
            background-color: red;
            border-radius: 50%;
            animation: flashRed 1s infinite;
            z-index: 999;
            box-shadow: 0 0 10px red;
            display: none;
        }

        @keyframes flashRed {
            0%, 50%, 100% { opacity: 1; }
            25%, 75% { opacity: 0; }
        }

        /* Modal styles */
        .modal {
            display: none;
            position: fixed;
            z-index: 1000;
            left: 50%;
            top: 50%;
            width: 90%;
            max-width: 500px;
            transform: translate(-50%, -50%);
            background-color: #fff;
            border: 2px solid #333;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 0 15px rgba(0,0,0,0.3);
        }

        .modal h2 { margin-top: 0; }
        .modal-buttons {
            margin-top: 20px;
        }

        .overlay {
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            background: rgba(0,0,0,0.5);
            display: none;
            z-index: 999;
        }

        button {
            padding: 10px 15px;
            margin-right: 10px;
            font-size: 1em;
        }
    </style>
</head>
<body>
    <h1>📡 LineAlert Dashboard</h1>
    <div class="view-toggle">
        <label><input type="radio" name="view" value="tech" checked> Tech View</label>
        <label><input type="radio" name="view" value="engineer"> Engineer View</label>
    </div>
    <div id="pinned"></div>
    <div id="log">Waiting for alerts...</div>
    <div id="red-alert-indicator"></div>

    <!-- Modal and overlay -->
    <div class="overlay" id="overlay" onclick="closeModal()"></div>
    <div class="modal" id="alertModal">
        <h2>Alert Details</h2>
        <div id="modalContent"></div>
        <div class="modal-buttons">
            <button onclick="acknowledge()">Acknowledge</button>
            <button onclick="openKB()">View Knowledge Base</button>
            <button onclick="closeModal()">Close</button>
        </div>
    </div>

    <script>
        let latestAlerts = [];

        function renderPinned(alert) {
            const indicator = document.getElementById('red-alert-indicator');
            if (alert && alert.severity && alert.severity.toUpperCase() === 'RED') {
                let html = '<div class="pinned">';
                html += '<strong>' + (alert.message || 'Critical Alert') + '</strong><br>';
                html += 'Severity: ' + (alert.severity || 'N/A') + '<br>';
                html += 'Timestamp: ' + (alert.timestamp || 'N/A');
                html += '</div>';
                document.getElementById('pinned').innerHTML = html;
                indicator.style.display = 'block';
            } else {
                document.getElementById('pinned').innerHTML = '';
                indicator.style.display = 'none';
            }
        }

        function renderAlerts(alerts) {
            latestAlerts = alerts;
            if (!alerts || alerts.length === 0) {
                document.getElementById('log').innerText = 'Waiting for alerts...';
                return;
            }

            let html = '';
            alerts.slice().reverse().forEach((alert, index) => {
                let severity = alert.severity ? alert.severity.toLowerCase() : 'green';
                html += '<div class="log ' + severity + '" onclick="openModal(' + index + ')">';
                html += '<strong>' + (alert.message || 'No message') + '</strong><br>';
                html += 'Severity: ' + (alert.severity || 'N/A') + '<br>';
                html += 'Timestamp: ' + (alert.timestamp || 'N/A');
                html += '</div>';
            });

            document.getElementById('log').innerHTML = html;
        }

        function openModal(index) {
            const alert = latestAlerts.slice().reverse()[index];
            const modal = document.getElementById('alertModal');
            const overlay = document.getElementById('overlay');
            const content = document.getElementById('modalContent');

            content.innerHTML = `
                <p><strong>Message:</strong> ${alert.message}</p>
                <p><strong>Severity:</strong> ${alert.severity}</p>
                <p><strong>Timestamp:</strong> ${alert.timestamp}</p>
                <p><strong>Asset:</strong> ${alert.asset || 'N/A'}</p>
                <p><strong>Zone:</strong> ${alert.zone || 'N/A'}</p>
                <p><strong>Fault Code:</strong> ${alert.fault_code || 'N/A'}</p>
            `;

            modal.style.display = 'block';
            overlay.style.display = 'block';
        }

        function closeModal() {
            document.getElementById('alertModal').style.display = 'none';
            document.getElementById('overlay').style.display = 'none';
        }

        function acknowledge() {
            alert("✅ Alert acknowledged (not yet wired to backend).");
            closeModal();
        }

        function openKB() {
            alert("📖 Open Knowledge Base (not yet implemented).");
        }

        function fetchData() {
            fetch('/get_logs')
                .then(res => res.json())
                .then(data => {
                    renderAlerts(data.alerts);
                    renderPinned(data.pinned);
                })
                .catch(err => console.error('Error fetching:', err));
        }

        setInterval(fetchData, 2000);
    </script>
</body>
</html>
"""

@app.route('/')
def dashboard():
    return render_template_string(HTML_TEMPLATE)

@app.route('/alert', methods=['POST'])
def receive_alert():
    global pinned_red, pinned_time
    data = request.get_json()
    if data:
        now = datetime.utcnow()
        data['timestamp'] = now.isoformat()

        with log_lock:
            alert_log.append(data)
            if data.get('severity', '').upper() == 'RED':
                pinned_red = data
                pinned_time = now
        return 'OK', 200
    return 'Invalid data', 400

@app.route('/get_logs')
def get_logs():
    global pinned_red, pinned_time
    now = datetime.utcnow()

    with log_lock:
        # Clear pinned red alert after timeout
        if pinned_red and (now - pinned_time).total_seconds() > PINNED_TIMEOUT_SECONDS:
            pinned_red = None
            pinned_time = None

        return jsonify({
            "alerts": alert_log,
            "pinned": pinned_red
        })

if __name__ == '__main__':
    app.run(port=5006)
