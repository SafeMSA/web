from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/', methods=['POST'])
def forward_request():
    # Extract data from incoming POST request
    incoming_data = request.get_json()

    # Forward data to localhost:9092
    while True:
        try:
            response = requests.post('http://localhost:9092', json=incoming_data)

            # Return response from localhost:9092 to the client
            if response.status_code == 200:
                return jsonify(response.json()), response.status_code
            
        except requests.exceptions.RequestException as e:
            print("Failed to POST")
            #return jsonify({"error": f"Failed to forward request: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9091)
