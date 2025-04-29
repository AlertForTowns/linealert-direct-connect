# snapshot/snapshot_writer.py
import json
import os
import glob
from datetime import datetime

SNAPSHOT_DIR = "snapshots"
SNAPSHOT_PREFIX = "snapshot"
MAX_SNAPSHOTS = 20  # Keep the most recent 20

def rotate_snapshots(directory):
    files = sorted(
        glob.glob(os.path.join(directory, "*.lasnap")),
        key=os.path.getctime
    )
    if len(files) > MAX_SNAPSHOTS:
        for f in files[:-MAX_SNAPSHOTS]:
            os.remove(f)
            print(f"[–] Deleted old snapshot: {f}")

def write_snapshot(data, metadata=None):
    if not os.path.exists(SNAPSHOT_DIR):
        os.makedirs(SNAPSHOT_DIR)

    rotate_snapshots(SNAPSHOT_DIR)

    timestamp = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    filename = f"{SNAPSHOT_PREFIX}_{timestamp}.lasnap"
    filepath = os.path.join(SNAPSHOT_DIR, filename)

    snapshot = {
        "timestamp": timestamp,
        "meta": metadata or {
            "source": "serial_capture",
            "device": "pi-usb-port",
            "version": "0.1"
        },
        "data": data
    }

    with open(filepath, "w") as f:
        json.dump(snapshot, f, indent=2)

    print(f"[+] Snapshot saved: {filepath}")
    return filepath

# Test
if __name__ == "__main__":
    sample_data = [
        {"ts": "2025-04-29T15:30:00Z", "raw": "D000100000F*"},
        {"ts": "2025-04-29T15:30:01Z", "raw": "D000200000F*"},
    ]
    write_snapshot(sample_data)
