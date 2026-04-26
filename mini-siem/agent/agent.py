import requests
import socket
import psutil
import time

SERVER_URL = "https://your-app.onrender.com/logs"
API_KEY = "device-1-key"

def collect_data():
    return {
        "hostname": socket.gethostname(),
        "cpu": psutil.cpu_percent(),
        "memory": psutil.virtual_memory().percent,
        "processes": [p.info for p in psutil.process_iter(['pid', 'name'])][:5]
    }

while True:
    try:
        data = collect_data()
        headers = {"Authorization": API_KEY}
        requests.post(SERVER_URL, json=data, headers=headers)
    except Exception as e:
        print("Error:", e)

    time.sleep(30)
