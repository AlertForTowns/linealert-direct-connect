import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import json
import time
import logging
import datetime
from pymodbus.client import ModbusTcpClient
from trainstack import Train, Cart
from train_utils import calculate_drift_score, label_drift

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

TRAIN_PATH = "../data/trains/train_panasonic_modbus.json"
MODBUS_HOST = "localhost"
MODBUS_PORT = 5020
POLL_INTERVAL = 3  # seconds
ROLE_ID = "modbus_tcp"

def format_cart(registers, timestamp, previous_snapshot=None):
    snapshot = {f"reg_{i}": val for i, val in enumerate(registers)}
    drift_score, stddev_delta = calculate_drift_score(snapshot, previous_snapshot or snapshot)
    label = label_drift(drift_score)

    cart = Cart.from_snapshot(snapshot)
    cart.meta["label"] = label
    cart.meta["drift_score"] = drift_score
    cart.meta["stddev_delta"] = stddev_delta
    cart.timestamp = timestamp

    return cart, snapshot

def main():
    logging.info("📡 Starting Modbus poller to feed TrainStack...")

    train = Train(id="train_panasonic_modbus", role_id=ROLE_ID)
    previous_snapshot = None

    client = ModbusTcpClient(MODBUS_HOST, port=MODBUS_PORT)
    client.connect()

    try:
        while True:
            result = client.read_holding_registers(address=0, count=10, slave=0)
            if result.isError():
                logging.warning(f"[!] Modbus read failed: {result}")
                continue

            now = datetime.datetime.now(datetime.UTC).isoformat()
            cart, previous_snapshot = format_cart(result.registers, now, previous_snapshot)

            train.push(cart)
            logging.info(f"🚃 Cart @ {now} | Score: {cart.meta['drift_score']:.3f} | Label: {cart.meta['label']}")

            os.makedirs(os.path.dirname(TRAIN_PATH), exist_ok=True)
            with open(TRAIN_PATH, "w") as f:
                json.dump(train.to_dict(), f, indent=2)

            time.sleep(POLL_INTERVAL)

    except KeyboardInterrupt:
        logging.info("🛑 Interrupted by user. Saving final train...")
        os.makedirs(os.path.dirname(TRAIN_PATH), exist_ok=True)
        with open(TRAIN_PATH, "w") as f:
            json.dump(train.to_dict(), f, indent=2)
        logging.info(f"[✓] Train saved to {TRAIN_PATH}")

if __name__ == "__main__":
    main()
