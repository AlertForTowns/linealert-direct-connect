from datetime import datetime
from cart import Cart, Train

# Initialize a Train instance for this Modbus server
train = Train(id="modbus_001", role_id="sensor_data")

def process_modbus_data(sensor_data):
    # Convert the received sensor data into a Cart instance
    cart = Cart(sensor_data)
    
    # Push the Cart into the Train instance
    train.push(cart)
    
    # After pushing the Cart, you can access its metadata
    print(f"Drift score for current snapshot: {cart.meta['drift_score']}")
    print(f"Label: {cart.meta['label']}")  # Green, Yellow, or Red
    
    # You can now send this data to your LineAlert agent
    send_alert_to_backend(cart)

def send_alert_to_backend(cart):
    import requests
    backend_url = "http://127.0.0.1:5007/alert"  # Backend URL
    
    # Prepare data to send
    alert_data = {
        "message": cart.data,  # Sensor data
        "severity": cart.meta["label"],  # Green, Yellow, or Red
        "timestamp": cart.timestamp,
    }

    # Send POST request to Flask backend
    response = requests.post(backend_url, json=alert_data)
    print(f"Alert sent to backend: {response.status_code}")
