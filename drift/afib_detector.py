# drift/afib_detector.py
import statistics

def detect_afib_timing(serial_log, expected_interval_ms=1000, threshold_jitter_ms=200):
    """
    Checks for abnormal timing jitter in a stream of timestamped packets.
    
    Args:
        serial_log (list): List of dicts with 'ts' field (ISO 8601 format).
        expected_interval_ms (int): Normal polling interval in milliseconds.
        threshold_jitter_ms (int): Acceptable variance before flagging as drift.

    Returns:
        dict: {
            "status": "stable" or "unstable",
            "variance_ms": float,
            "mean_interval_ms": float,
            "alert": True/False
        }
    """
    if len(serial_log) < 3:
        return {"status": "insufficient data", "alert": False}

    timestamps = [
        parse_iso(ts["ts"]) for ts in serial_log if "ts" in ts
    ]
    
    deltas = [
        (t2 - t1).total_seconds() * 1000
        for t1, t2 in zip(timestamps[:-1], timestamps[1:])
    ]

    variance = statistics.variance(deltas)
    mean_interval = statistics.mean(deltas)

    return {
        "status": "unstable" if variance > threshold_jitter_ms else "stable",
        "variance_ms": round(variance, 2),
        "mean_interval_ms": round(mean_interval, 2),
        "alert": variance > threshold_jitter_ms
    }

def parse_iso(iso_ts):
    from datetime import datetime
    return datetime.fromisoformat(iso_ts.replace("Z", "+00:00"))

# Example test:
if __name__ == "__main__":
    test_log = [
        {"ts": "2025-04-29T15:30:00.000Z"},
        {"ts": "2025-04-29T15:30:01.000Z"},
        {"ts": "2025-04-29T15:30:01.999Z"},
        {"ts": "2025-04-29T15:30:03.400Z"},
        {"ts": "2025-04-29T15:30:04.100Z"},
    ]
    result = detect_afib_timing(test_log)
    print(result)
