# profile/auto_profiler.py
import json
import re
from collections import Counter
from datetime import datetime

def load_snapshot(path):
    with open(path, "r") as f:
        return json.load(f)

def extract_registers(data):
    # Example: Parse register IDs from raw Panasonic/Modbus messages
    # You can refine this with regex specific to your protocol
    register_pattern = re.compile(r"D(\d+)", re.IGNORECASE)
    registers = []
    for pkt in data:
        match = register_pattern.search(pkt.get("raw", ""))
        if match:
            registers.append(match.group(1))
    return registers

def compute_intervals(timestamps):
    times = [datetime.fromisoformat(ts["ts"].replace("Z", "+00:00")) for ts in timestamps]
    deltas = [
        (t2 - t1).total_seconds() * 1000
        for t1, t2 in zip(times[:-1], times[1:])
    ]
    return deltas

def generate_profile(snapshot):
    data = snapshot["data"]
    if len(data) < 2:
        return {"error": "Not enough data"}

    registers = extract_registers(data)
    deltas = compute_intervals(data)

    profile = {
        "summary": {
            "total_packets": len(data),
            "time_span_sec": (datetime.fromisoformat(data[-1]["ts"].replace("Z", "+00:00")) -
                              datetime.fromisoformat(data[0]["ts"].replace("Z", "+00:00"))).total_seconds()
        },
        "polling_interval_ms": {
            "mean": round(sum(deltas) / len(deltas), 2),
            "min": round(min(deltas), 2),
            "max": round(max(deltas), 2),
            "variance": round(sum((x - sum(deltas)/len(deltas))**2 for x in deltas) / len(deltas), 2)
        },
        "registers_accessed": dict(Counter(registers)),
        "unique_register_count": len(set(registers))
    }

    return profile

# Example test
if __name__ == "__main__":
    snapshot = load_snapshot("snapshots/snapshot_test.lasnap")
    profile = generate_profile(snapshot)
    print(json.dumps(profile, indent=2))
