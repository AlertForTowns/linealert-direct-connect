#!/usr/bin/env python3

import json
import argparse
from pathlib import Path
from datetime import datetime, timezone

# Adjust to point to your real snapshot folder
SNAPSHOT_DIR = Path(__file__).resolve().parent.parent / "snapshot"

def load_snapshot(filename):
    path = SNAPSHOT_DIR / filename
    if not path.exists():
        print(f"❌ File not found: {path}")
        exit(1)
    with open(path, "r") as f:
        return json.load(f)

def save_tagged_snapshot(data, metadata, original_filename):
    tagged_data = {
        "metadata": metadata,
        "snapshot": data
    }
    tagged_filename = original_filename.replace(".lasnap", "_tagged.lasnap")
    with open(SNAPSHOT_DIR / tagged_filename, "w") as f:
        json.dump(tagged_data, f, indent=2)
    print(f"✅ Tagged snapshot saved as: {tagged_filename}")

def main():
    parser = argparse.ArgumentParser(description="Tag a .lasnap snapshot with metadata.")
    parser.add_argument("filename", help="Name of the .lasnap file to tag (in /snapshot)")
    parser.add_argument("--site", required=True, help="Site name (e.g., Diamond Head Mall)")
    parser.add_argument("--device", required=True, help="Device type or ID (e.g., HVAC_Controller_01)")
    parser.add_argument("--location", default="Unknown", help="Physical location (e.g., Rooftop)")

    args = parser.parse_args()

    snapshot_data = load_snapshot(args.filename)

    metadata = {
        "tagged_at": datetime.now(timezone.utc).isoformat(),
        "site": args.site,
        "device": args.device,
        "location": args.location,
        "tagger_version": "v0.1"
    }

    save_tagged_snapshot(snapshot_data, metadata, args.filename)

if __name__ == "__main__":
    main()
