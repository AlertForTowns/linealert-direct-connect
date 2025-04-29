# alert/webhook_sender.py
import requests

def send_alert_webhook(message, webhook_url):
    payload = {"text": message}
    try:
        r = requests.post(webhook_url, json=payload)
        if r.status_code == 200:
            print("[✅] Webhook alert sent.")
        else:
            print(f"[!] Webhook error: {r.status_code}")
    except Exception as e:
        print(f"[X] Failed to send alert: {e}")

# Test
if __name__ == "__main__":
    test_message = "🚨 Test alert from LineAlert Direct-Connect"
    test_webhook = "https://hooks.slack.com/services/your/webhook/url"
    send_alert_webhook(test_message, test_webhook)
