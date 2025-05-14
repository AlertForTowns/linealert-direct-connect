import random
import requests
import time
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger()

def send_drift_data(drift_data):
    host_ip = '192.168.0.16'  # Use the host's IP address
    url = f'http://{host_ip}:5007/drift'  # Use host IP address to connect to Flask backend
    
    # Setup retries for HTTP requests
    session = requests.Session()
    retry = Retry(
        total=5,  # Number of retries before failing
        backoff_factor=1,  # Exponential backoff between retries
        status_forcelist=[500, 502, 503, 504],  # Retry for server errors
        allowed_methods=["HEAD", "GET", "POST"]  # Methods to apply retries to
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    
    try:
        log.debug("Sending drift data...")  # Debugging message
        response = session.post(url, json=drift_data)
        response.raise_for_status()  # Will raise an error for any bad status codes
        log.info(f"Drift data sent successfully. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        log.error(f"Failed to send drift data. Error: {e}")
        return

    if response:
        log.debug(f"Response: {response.text}")

def apply_drift():
    drift_data = []
    for tag in ['Pressure', 'Temperature', 'FlowRate']:
        drift_value = random.uniform(15, 50)  # Increase drift range to 15%-50% to see larger variations
        drift_data.append({
            'tag': tag,
            'value': round(random.uniform(20, 30), 2),  # Random value between 20-30
            'severity': 'Low',  # Starting as Low but should be updated based on drift
            'change': f"{drift_value:.2f}%",
            'timestamp': time.strftime('%Y-%m-%dT%H:%M:%S')  # Use current time for timestamp
        })
    log.debug("Drift data prepared:", drift_data)  # Debugging message
    send_drift_data(drift_data)

# Start sending drift data continuously
if __name__ == '__main__':
    try:
        log.info("Starting drift server...")
        while True:
            apply_drift()
            time.sleep(5)  # Wait for 5 seconds before applying drift again
    except Exception as e:
        log.error(f"An error occurred in the drift server: {e}")
