import requests
import time

def send_webhook_message(webhook_url, message):
    payload = {'content': message}
    try:
        requests.post(webhook_url, json=payload)
    except requests.exceptions.RequestException as e:
        print(f"Failed to send webhook message: {e}")

if __name__ == "__main__":
    WEBHOOK_URL = "https://discord.com/api/webhooks/1335341177234264217/KfbTw7q3sBrWYPDwacLgF7Sl-M686NB7o59ZEoyegAzqgg3wKqB-tIID9tePm2pewpfR"

    send_webhook_message(WEBHOOK_URL, "Worker started.")

    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        pass

    send_webhook_message(WEBHOOK_URL, "Worker stopped.")
