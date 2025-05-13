#!/usr/bin/env python3

import json
import argparse
from pathlib import Path

SNAPSHOT_DIR = Path(__file__).resolve().parent.parent / "linealert" / "snapshot"
PROFILE_PATH = Path(__file__).resolve().parent.parent / "linealert" / "profiles" / "HVAC_Controller_01.json"

def load_profile():
    if PROFILE_PATH.exists():
        with open(PROFILE_PATH, "r") as f:
            return json.load(f)
    print("❌ Profile not found.")
    exit(1)

def extract_registers(snapshot_path):
    with open(snapshot_path, "r") as f:
        content = json.load(f)
        if "snapshot" in content:
            content = content["snapshot"]
        packets = content.get("data", {}).get("packets", [])
        for p in packets:
            if p.get("protocol") == "ModbusTCP" and "register" in p and "value" in p:
                yield str(p["register"]), p["value"]

def test_snapshot(snapshot_filename):
    profile = load_profile()
    snapshot_path = SNAPSHOT_DIR / snapshot_filename
    if not snapshot_path.exists():
        print(f"❌ Snapshot not found: {snapshot_filename}")
        return

    print(f"\n📂 Playback Test: {snapshot_filename}")
    passed = True

    for reg_id, value in extract_registers(snapshot_path):
        entry = profile.get(reg_id)
        if not entry:
            print(f"❓ {reg_id} not in profile → can't validate")
            passed = False
            continue

        if entry["min"] <= value <= entry["max"]:
            print(f"✅ Register {reg_id} = {value} is within range [{entry['min']}, {entry['max']}]")
        else:
            print(f"🚨 Register {reg_id} = {value} OUT OF RANGE [{entry['min']}, {entry['max']}]")
            passed = False

    if passed:
        print("🎉 Snapshot PASSED validation.")
    else:
        print("❌ Snapshot FAILED validation.")

def main():
    parser = argparse.ArgumentParser(description="Playback test: Validate snapshot against behavior profile.")
    parser.add_argument("filename", help="Snapshot file in /snapshot to test")
    args = parser.parse_args()

    test_snapshot(args.filename)

if __name__ == "__main__":
    main()

