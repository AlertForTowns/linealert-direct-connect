import random
import requests
import time

def send_drift_data(drift_data):
    host_ip = '192.168.0.16'  # Use the host's IP address
    url = f'http://{host_ip}:5007/drift'  # Use host IP address to connect to Flask backend
    
    try:
        print("Sending drift data...")  # Debugging message
        response = requests.post(url, json=drift_data)
        response.raise_for_status()  # Will raise an error for any bad status codes
        print(f"Drift data sent successfully. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send drift data. Error: {e}")
        return

    if response:
        print(f"Response: {response.text}")

def apply_drift():
    drift_data = []
    for tag in ['Pressure', 'Temperature', 'FlowRate']:
        drift_value = random.uniform(15, 50)  # Increase drift range to 15%-50% to see larger variations
        drift_data.append({
            'tag': tag,
            'value': round(random.uniform(20, 30), 2),  # Random value between 20-30
            'severity': 'Low',  # Starting as Low but should be updated based on drift
            'change': f"{drift_value:.2f}%",
            'timestamp': '2025-05-12T09:15:00'
        })
    print("Drift data prepared:", drift_data)  # Debugging message
    send_drift_data(drift_data)

# Start sending drift data continuously
if __name__ == '__main__':
    try:
        print("Starting drift server...")
        while True:
            apply_drift()
            time.sleep(5)  # Wait for 5 seconds before applying drift again
    except Exception as e:
        print(f"An error occurred in the drift server: {e}")
