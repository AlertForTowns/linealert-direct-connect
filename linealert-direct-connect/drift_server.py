from flask import Flask, jsonify
import threading, time, os, random, argparse
from trainstack import TrainStack
from afib_detector import AFIBDriftDetector

parser = argparse.ArgumentParser()
parser.add_argument("--port", type=int, default=int(os.getenv("PORT", 15021)))
parser.add_argument("--start-reg", type=int, default=int(os.getenv("START_REG", 0)))
parser.add_argument("--reg-count", type=int, default=int(os.getenv("REG_COUNT", 5)))
parser.add_argument("--drift-register", type=int, default=int(os.getenv("DRIFT_REGISTER", -1)))
parser.add_argument("--drift-type", type=str, default=os.getenv("DRIFT_TYPE", "random"))
parser.add_argument("--drift-interval", type=int, default=int(os.getenv("DRIFT_INTERVAL", 1)))
parser.add_argument("--drift-amount", type=int, default=int(os.getenv("DRIFT_AMOUNT", 10)))
args = parser.parse_args()

app = Flask(__name__)

START_REG = args.start_reg
REG_COUNT = args.reg_count
PORT = args.port
DRIFT_REGISTER = args.drift_register
DRIFT_TYPE = args.drift_type
DRIFT_INTERVAL = args.drift_interval
DRIFT_AMOUNT = args.drift_amount

holding_registers = [100 + i for i in range(START_REG, START_REG + REG_COUNT)]
lock = threading.Lock()

trainstack = TrainStack(max_trains=10, max_carts=1)
afib_detector = AFIBDriftDetector(window_size=10, threshold=5)

def drift_loop():
    last_drift = time.time()
    while True:
        time.sleep(0.1)
        now = time.time()
        with lock:
            if DRIFT_REGISTER >= 0 and DRIFT_REGISTER < REG_COUNT and (now - last_drift) >= DRIFT_INTERVAL:
                if DRIFT_TYPE == "increment":
                    holding_registers[DRIFT_REGISTER] += DRIFT_AMOUNT
                elif DRIFT_TYPE == "decrement":
                    holding_registers[DRIFT_REGISTER] -= DRIFT_AMOUNT
                elif DRIFT_TYPE == "random":
                    holding_registers[DRIFT_REGISTER] += random.choice([-DRIFT_AMOUNT, DRIFT_AMOUNT])
                last_drift = now
            value = holding_registers[DRIFT_REGISTER] if DRIFT_REGISTER >= 0 else holding_registers[0]
            trainstack.add_train(value)
            alert_level, alert_message = afib_detector.detect_drift(value)
            print(f"[{alert_level}] {alert_message}")

@app.route("/read_holding_registers")
def read_holding_registers():
    with lock:
        return jsonify({"holding_registers": holding_registers})

@app.route("/trainstack_summary")
def trainstack_summary():
    with lock:
        return jsonify({
            "train_count": len(trainstack.trains),
            "latest_train": trainstack.trains[-1] if trainstack.trains else None
        })

if __name__ == "__main__":
    threading.Thread(target=drift_loop, daemon=True).start()
    app.run(host="0.0.0.0", port=PORT)
