#!/usr/bin/env python3

import json
import argparse
from pathlib import Path
from colorama import Fore, Style, init

init(autoreset=True)

SNAPSHOT_DIR = Path(__file__).resolve().parent.parent / "snapshot"

def load_snapshot(filepath):
    with open(filepath, "r") as f:
        return json.load(f)

def print_metadata(metadata):
    print(Fore.YELLOW + "📌 Metadata")
    for key, value in metadata.items():
        print(f"{Fore.CYAN}- {key}: {Style.RESET_ALL}{value}")
    print()

def print_summary(data):
    print(Fore.YELLOW + "📊 Traffic Summary")
    summary = data.get("traffic_summary", {})
    for key, value in summary.items():
        print(f"{Fore.CYAN}- {key}: {Style.RESET_ALL}{value}")
    print()

def print_protocols(data):
    print(Fore.YELLOW + "🔍 Protocols Observed")
    protocols = data.get("traffic_summary", {}).get("protocols", [])
    for p in protocols:
        print(f"{Fore.CYAN}- {p}")
    print()

def main():
    parser = argparse.ArgumentParser(description="View contents of a .lasnap file.")
    parser.add_argument("filename", help="Name of the .lasnap file (in /snapshot)")
    args = parser.parse_args()

    path = SNAPSHOT_DIR / args.filename
    if not path.exists():
        print(f"❌ File not found: {path}")
        return

    content = load_snapshot(path)

    # Check if it's tagged (has metadata + snapshot keys)
    if "metadata" in content and "snapshot" in content:
        print_metadata(content["metadata"])
        snapshot_data = content["snapshot"]
    else:
        snapshot_data = content

    print_summary(snapshot_data.get("data", {}))
    print_protocols(snapshot_data.get("data", {}))

if __name__ == "__main__":
    main()
