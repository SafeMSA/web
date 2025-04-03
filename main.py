from flask import Flask, request, jsonify
import aiohttp
import asyncio
from datetime import datetime

id = 0
app = Flask(__name__)

# Async function to forward the request
async def forward_request_async(incoming_data):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post('http://localhost:9092', json=incoming_data) as response:
                if response.status == 200:
                    return await response.json(), response.status
                else:
                    return {"error": f"Failed with status code {response.status}"}, response.status
    except Exception as e:
        print(f"Failed to POST: {e}")
        return {"error": f"Failed to forward request: {str(e)}"}, 500

@app.route('/', methods=['POST'])
async def forward_request():
    global id

    # Extract data from incoming POST request
    incoming_data = await request.get_json()

    # Add additional data to the incoming request
    incoming_data['time_sent'] = datetime.now().isoformat()
    incoming_data['id'] = id
    id += 1

    # Forward the request asynchronously
    result, status_code = await forward_request_async(incoming_data)

    return jsonify(result), status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9091, debug=True)