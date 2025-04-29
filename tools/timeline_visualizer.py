# tools/timeline_visualizer.py
import json
import matplotlib.pyplot as plt
from datetime import datetime

def load_snapshot(path):
    with open(path, "r") as f:
        return json.load(f)["data"]

def compute_intervals(data):
    times = [datetime.fromisoformat(pkt["ts"].replace("Z", "+00:00")) for pkt in data]
    return [
        (t2 - t1).total_seconds() * 1000
        for t1, t2 in zip(times[:-1], times[1:])
    ]

if __name__ == "__main__":
    snap = load_snapshot("snapshots/example.lasnap")
    intervals = compute_intervals(snap)
    plt.plot(intervals, marker='o')
    plt.title("Polling Interval Jitter (ms)")
    plt.xlabel("Packet #")
    plt.ylabel("Interval (ms)")
    plt.grid(True)
    plt.show()
