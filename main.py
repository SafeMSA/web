from flask import Flask, request, jsonify
import requests
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import threading
import time

app = Flask(__name__)
executor = ThreadPoolExecutor(max_workers=50)
id_counter = 0

def forward_to_target(data):
    """Retries until the target service is available."""
    while True:
        try:
            response = requests.post('http://localhost:9092', json=data)
            if response.status_code == 200:
                print(f"Successfully forwarded ID {data['id']}")
                break
        except requests.exceptions.RequestException:
            print(f"Retrying ID {data['id']}...")
        time.sleep(1)  # Avoid spamming too fast

@app.route('/', methods=['POST'])
def handle_request():
    global id_counter

    data = request.get_json()
    data['time_sent'] = datetime.now().isoformat()

    
    data['id'] = id_counter
    id_counter += 1

    # Submit the forwarding job to a background thread
    executor.submit(forward_to_target, data)

    # Immediately respond to the client
    return jsonify({"status": "Accepted", "id": data['id']}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9091)
