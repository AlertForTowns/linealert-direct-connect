# File: linealert-direct-connect/meta_analyzer.py

import statistics
from collections import defaultdict
import time

def analyze_global_patterns(snapshot_history):
    grouped_values = defaultdict(list)
    for entry in snapshot_history:
        try:
            cart = entry["device"]
            reg = entry["register"]
            values = entry["values"]
            grouped_values[(cart, reg)].extend(values)
        except KeyError as e:
            print(f"[META ERROR] Missing key in entry: {e}")

    summary_lines = [f"\n[{time.strftime('%H:%M:%S')}] [META-ANALYZER SUMMARY]\n"]
    for (cart, reg), values in grouped_values.items():
        if len(values) < 3:
            continue
        try:
            mean = statistics.mean(values)
            stdev = statistics.stdev(values)
            slope = values[-1] - values[0]
            summary_lines.append(
                f"[META] Cart {cart} - Reg {reg} | Mean: {mean:.2f}, Stdev: {stdev:.2f}, Slope: {slope}"
            )
        except statistics.StatisticsError as e:
            print(f"[META ERROR] Stats error for Cart {cart} Reg {reg}: {e}")

    return "\n".join(summary_lines) if len(summary_lines) > 1 else "[META-ANALYZER] No data for summary."

# Optional test stub
if __name__ == "__main__":
    test_data = [
        {"timestamp": time.time(), "device": "Cart A", "register": 0, "values": [100, 101, 103], "state": "DRIFT"},
        {"timestamp": time.time(), "device": "Cart B", "register": 1, "values": [105, 105, 105], "state": "STABLE"}
    ]
    print(analyze_global_patterns(test_data))
