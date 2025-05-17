from flask import Flask, jsonify
import threading
import time
import os
import random
import argparse
import sys

# Add the parent directory to the system path to import trainstack modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from trainstack.trainstack_manager import TrainStack
from trainstack.analyzer import detect_drift

# Argument parser for command-line overrides
parser = argparse.ArgumentParser()
parser.add_argument("--port", type=int, default=int(os.getenv("PORT", 15021)))
parser.add_argument("--start-reg", type=int, default=int(os.getenv("START_REG", 0)))
parser.add_argument("--reg-count", type=int, default=int(os.getenv("REG_COUNT", 5)))
parser.add_argument("--drift-register", type=int, default=int(os.getenv("DRIFT_REGISTER", -1)))
parser.add_argument("--drift-type", type=str, default=os.getenv("DRIFT_TYPE", "none"))
parser.add_argument("--drift-interval", type=int, default=int(os.getenv("DRIFT_INTERVAL", 10)))
parser.add_argument("--drift-amount", type=int, default=int(os.getenv("DRIFT_AMOUNT", 1)))
args = parser.parse_args()

app = Flask(__name__)

# Config
START_REG = args.start_reg
REG_COUNT = args.reg_count
PORT = args.port
DRIFT_REGISTER = args.drift_register
DRIFT_TYPE = args.drift_type
DRIFT_INTERVAL = args.drift_interval
DRIFT_AMOUNT = args.drift_amount

# Holding registers and thread-safe lock
holding_registers = [100 + i for i in range(START_REG, START_REG + REG_COUNT)]
lock = threading.Lock()

# Initialize TrainStack
train_stack = TrainStack(max_trains=10)

def drift_loop():
    last_drift = time.time()
    while True:
        time.sleep(0.1)
        now = time.time()
        if DRIFT_REGISTER >= 0 and DRIFT_REGISTER < REG_COUNT and (now - last_drift) >= DRIFT_INTERVAL:
            with lock:
                if DRIFT_TYPE == "increment":
                    holding_registers[DRIFT_REGISTER] += DRIFT_AMOUNT
                elif DRIFT_TYPE == "decrement":
                    holding_registers[DRIFT_REGISTER] -= DRIFT_AMOUNT
                elif DRIFT_TYPE == "random":
                    holding_registers[DRIFT_REGISTER] += random.choice([-DRIFT_AMOUNT, DRIFT_AMOUNT])
            last_drift = now

def snapshot_loop():
    while True:
        time.sleep(1)  # Snapshot every 1 second
        with lock:
            snapshot = list(holding_registers)
        train_stack.add_train(snapshot)
        # Optional: Analyze drift
        drifts = detect_drift(train_stack.get_all_trains())
        if drifts:
            latest_drift = drifts[-1]
            print(f"Drift detected from {latest_drift['from']} to {latest_drift['to']}: {latest_drift['drift_flags']}")

@app.route("/read_holding_registers")
def read_holding_registers():
    with lock:
        return jsonify({"holding_registers": holding_registers})

@app.route("/trainstack")
def get_trainstack():
    return jsonify(train_stack.get_all_trains())

@app.route("/high_water_marks")
def get_high_water_marks():
    return jsonify(train_stack.get_high_water_marks())

if __name__ == "__main__":
    threading.Thread(target=drift_loop, daemon=True).start()
    threading.Thread(target=snapshot_loop, daemon=True).start()
    app.run(host="0.0.0.0", port=PORT)

