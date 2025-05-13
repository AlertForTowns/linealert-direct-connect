#!/usr/bin/env python3

import json
from pathlib import Path

# Adjusted for your structure: /linealert-direct-connect/linealert/snapshot/
SNAPSHOT_DIR = Path(__file__).resolve().parent.parent / "linealert" / "snapshot"
REGISTER_TO_TRACK = 40001
DRIFT_THRESHOLD = 10  # trigger alert if register changes by 10 or more

def extract_value(snapshot_path):
    with open(snapshot_path, "r") as f:
        content = json.load(f)
        # Support both tagged and untagged snapshots
        if "snapshot" in content:
            content = content["snapshot"]
        packets = content.get("data", {}).get("packets", [])
        for packet in packets:
            if packet.get("protocol") == "ModbusTCP" and packet.get("register") == REGISTER_TO_TRACK:
                return packet.get("value"), packet.get("timestamp")
    return None, None

def detect_drift(filenames):
    last_value = None
    for fname in sorted(filenames):
        path = SNAPSHOT_DIR / fname
        if not path.exists():
            print(f"❌ Missing file: {fname}")
            continue

        value, timestamp = extract_value(path)
        if value is None:
            print(f"⚠️  No valid register data in {fname}")
            continue

        print(f"📦 {fname} @ {timestamp} → Register {REGISTER_TO_TRACK} = {value}")

        if last_value is not None:
            diff = value - last_value
            if abs(diff) >= DRIFT_THRESHOLD:
                print(f"  🚨 Drift detected! Δ = {diff} (≥ {DRIFT_THRESHOLD})")

        last_value = value

def main():
    filenames = [f"drift_snapshot_{i}.lasnap" for i in range(1, 5)]
    detect_drift(filenames)

if __name__ == "__main__":
    main()
