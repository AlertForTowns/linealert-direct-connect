# linealert_cli.py

import os
import argparse
import json
from capture.serial_capture import open_serial_port, capture_serial_data
from snapshot.snapshot_writer import write_snapshot
from profile.auto_profiler import generate_profile
from profile.compare_profiles import compare_profiles
from alert.webhook_sender import send_alert_webhook
from security.encryptor import encrypt_lasnap

def run_capture_and_snapshot(port, max_lines, encrypt, password):
    print(f"[+] Starting capture on {port}...")
    ser = open_serial_port(port=port)
    data = capture_serial_data(ser, max_lines=max_lines)
    ser.close()

    print("[+] Capture complete. Writing snapshot...")
    snap_path = write_snapshot(data)

    if encrypt:
        enc_path = snap_path.replace(".lasnap", ".enc")
        encrypt_lasnap(snap_path, enc_path, password)
        print(f"[🔒] Encrypted snapshot saved: {enc_path}")
        return enc_path
    else:
        return snap_path

def run_profile(snapshot_path, save_path):
    print(f"[+] Generating profile from {snapshot_path}...")
    with open(snapshot_path, "r") as f:
        snap = json.load(f)
    profile = generate_profile(snap)
    with open(save_path, "w") as f:
        json.dump(profile, f, indent=2)
    print(f"[+] Profile saved to {save_path}")
    return profile

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LineAlert Direct-Connect CLI")
    parser.add_argument("--port", type=str, default="/dev/ttyUSB0", help="Serial port")
    parser.add_argument("--max", type=int, default=100, help="Max packets to capture")
    parser.add_argument("--encrypt", action="store_true", help="Encrypt snapshot")
    parser.add_argument("--password", type=str, help="Encryption password")
    parser.add_argument("--baseline", type=str, help="Path to baseline profile")
    parser.add_argument("--webhook", type=str, help="Webhook URL for alerts")

    args = parser.parse_args()

    snap_path = run_capture_and_snapshot(args.port, args.max, args.encrypt, args.password or "")

    if not args.encrypt:
        profile_path = snap_path.replace(".lasnap", ".profile.json")
        new_profile = run_profile(snap_path, profile_path)

        if args.baseline:
            from profile.compare_profiles import load_profile
            old_profile = load_profile(args.baseline)
            print("[+] Comparing to baseline...")
            results = compare_profiles(old_profile, new_profile)
            print("\n".join(results))

            if args.webhook and any("⚠️" in r or "🆕" in r or "⏱" in r for r in results):
                print("[+] Sending webhook alert...")
                send_alert_webhook("\n".join(results), args.webhook)
