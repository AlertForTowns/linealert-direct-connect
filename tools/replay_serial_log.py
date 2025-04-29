# tools/replay_serial_log.py
import time
from datetime import datetime

def replay_log(file_path, delay_ms=1000):
    with open(file_path, "r") as f:
        lines = f.readlines()

    for raw in lines:
        ts = datetime.utcnow().isoformat() + "Z"
        print(f'{{"ts": "{ts}", "raw": "{raw.strip()}"}}')
        time.sleep(delay_ms / 1000)

if __name__ == "__main__":
    replay_log("test_data/example_serial_log.txt", delay_ms=1000)
