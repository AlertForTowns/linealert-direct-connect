# train_utils.py

import math

def calculate_drift_score(current_snapshot, previous_snapshot):
    """
    Calculates a drift score based on the difference between the current and previous snapshots.
    Returns a tuple: (drift_score, stddev_delta)
    """
    drift_score = 0.0
    stddev_delta = 0.0

    try:
        deltas = []
        for key in current_snapshot:
            current = current_snapshot.get(key, 0)
            previous = previous_snapshot.get(key, 0)
            deltas.append(abs(current - previous))

        if deltas:
            drift_score = sum(deltas) / len(deltas)
            mean = drift_score
            variance = sum((x - mean) ** 2 for x in deltas) / len(deltas)
            stddev_delta = math.sqrt(variance)

    except Exception as e:
        print(f"[ERROR] Drift calc failed: {e}")

    return drift_score, stddev_delta

def label_drift(score):
    """
    Classifies the drift score into human-readable labels.
    """
    if score < 0.05:
        return "stable"
    elif score < 0.2:
        return "warning"
    else:
        return "critical"
