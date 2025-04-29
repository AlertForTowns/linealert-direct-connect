# linealert_cli.py
import os
import argparse
from capture.serial_capture import open_serial_port, capture_serial_data
from snapshot.snapshot_writer import write_snapshot
from profile.auto_profiler import generate_profile
from profile.compare_profiles import compare_profiles

def run_capture_and_snapshot(port, max_lines):
    print(f"[+] Starting capture on {port}...")
    ser = open_serial_port(port=port)
    data = capture_serial_data(ser, max_lines=max_lines)
    ser.close()
    print("[+] Capture complete. Writing snapshot...")
    return write_snapshot(data)

def run_profile(snapshot_path, output_path):
    print(f"[+] Generating profile from {snapshot_path}...")
    import json
    with open(snapshot_path, "r") as f:
        snap = json.load(f)
    profile = generate_profile(snap)
    with open(output_path, "w") as f:
        json.dump(profile, f, indent=2)
    print(f"[+] Profile saved to {output_path}")
    return profile

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LineAlert CLI")
    parser.add_argument("--port", type=str, default="/dev/ttyUSB0", help="Serial port")
    parser.add_argument("--max", type=int, default=100, help="Max lines to capture")
    parser.add_argument("--baseline", type=str, help="Path to baseline profile")
    args = parser.parse_args()

    snap_path = run_capture_and_snapshot(args.port, args.max)
    profile_path = snap_path.replace(".lasnap", ".profile.json")
    new_profile = run_profile(snap_path, profile_path)

    if args.baseline:
        from profile.compare_profiles import load_profile
        old_profile = load_profile(args.baseline)
        print("[+] Comparing to baseline...")
        results = compare_profiles(old_profile, new_profile)
        print("\n".join(results))
