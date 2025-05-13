import requests
from datetime import datetime

def send_alert_to_backend(cart):
    """Send a drift alert to the Flask backend."""
    backend_url = "http://127.0.0.1:5007/alert"
    
    alert_data = {
        "message": cart.data,
        "severity": cart.meta.get("label", "green"),
        "timestamp": cart.timestamp or datetime.utcnow().isoformat()
    }

    try:
        response = requests.post(backend_url, json=alert_data)
        if response.status_code == 200:
            print(f"[✓] Alert sent: {alert_data}")
        else:
            print(f"[!] Alert failed with status {response.status_code}: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"[X] Failed to send alert: {e}")

# Optional: Example cart object for testing
class Cart:
    def __init__(self, data, label, timestamp=None):
        self.data = data
        self.meta = {"label": label}
        self.timestamp = timestamp or datetime.utcnow().isoformat()

# Run test when executing this file directly
if __name__ == "__main__":
    example_cart = Cart(data="PLC1 temp spike to 85C", label="red")
    send_alert_to_backend(example_cart)
