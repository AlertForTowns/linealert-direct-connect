#!/usr/bin/env python3

import json
import argparse
from pathlib import Path
from datetime import datetime

SNAPSHOT_DIR = Path(__file__).resolve().parent.parent / "linealert" / "snapshot"
PROFILE_PATH = Path(__file__).resolve().parent.parent / "linealert" / "profiles" / "HVAC_Controller_01.json"
LOG_DIR = Path(__file__).resolve().parent.parent / "linealert" / "logs"
STABILITY_THRESHOLD = 3

def load_profile():
    if PROFILE_PATH.exists():
        with open(PROFILE_PATH, "r") as f:
            return json.load(f)
    return {}

def save_profile(profile):
    PROFILE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(PROFILE_PATH, "w") as f:
        json.dump(profile, f, indent=2)
    print(f"✅ Profile updated → {PROFILE_PATH.name}")

def extract_modbus_registers(snapshot_file):
    with open(snapshot_file, "r") as f:
        content = json.load(f)
        if "snapshot" in content:
            content = content["snapshot"]
        packets = content.get("data", {}).get("packets", [])
        for p in packets:
            if p.get("protocol") == "ModbusTCP" and "register" in p and "value" in p:
                yield str(p["register"]), p["value"]

def log_drift_event(reg_id, value, old_range):
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "register": reg_id,
        "value": value,
        "previous_range": old_range
    }
    log_file = LOG_DIR / f"drift_events.jsonl"
    with open(log_file, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

def update_profile_from_snapshots(learn_mode=False):
    profile = load_profile()

    for i in range(1, 5):
        snap_file = SNAPSHOT_DIR / f"drift_snapshot_{i}.lasnap"
        print(f"\n📦 Processing: {snap_file.name}")
        for reg_id, value in extract_modbus_registers(snap_file):
            print(f"🔧 Register {reg_id} = {value}")
            entry = profile.get(reg_id, {
                "min": None,
                "max": None,
                "last_seen": None,
                "stable_counter": 0,
                "anomaly_counter": 0
            })

            if entry["min"] is None:
                entry["min"] = entry["max"] = entry["last_seen"] = value
                entry["stable_counter"] = 1
            elif entry["min"] <= value <= entry["max"]:
                entry["stable_counter"] += 1
                entry["last_seen"] = value
            else:
                entry["anomaly_counter"] += 1
                print(f"  ⚠️ Out of range: {value} not in [{entry['min']}, {entry['max']}]")
                log_drift_event(reg_id, value, [entry["min"], entry["max"]])

                if learn_mode:
                    entry["min"] = min(entry["min"], value)
                    entry["max"] = max(entry["max"], value)
                    print(f"  🧠 Learn Mode: Expanded → [{entry['min']}, {entry['max']}]")
                elif entry["stable_counter"] >= STABILITY_THRESHOLD:
                    if value < entry["min"]:
                        entry["min"] -= 1
                    if value > entry["max"]:
                        entry["max"] += 1
                    print(f"  🔄 Adapted → [{entry['min']}, {entry['max']}]")

            profile[reg_id] = entry

    save_profile(profile)

def main():
    parser = argparse.ArgumentParser(description="Update profile from drift snapshots.")
    parser.add_argument("--learn", action="store_true", help="Enable learn mode for rapid adaptation")
    args = parser.parse_args()

    update_profile_from_snapshots(learn_mode=args.learn)

if __name__ == "__main__":
    main()

