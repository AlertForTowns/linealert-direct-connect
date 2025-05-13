# modules/afib_drift_detector.py

import numpy as np

class AFibDriftDetector:
    def __init__(self, window_size=5, jitter_threshold=0.15):
        self.stddev_window = []
        self.window_size = window_size
        self.jitter_threshold = jitter_threshold

    def update(self, registers):
        snapshot = np.array(list(registers.values()))
        stddev = np.std(snapshot)
        self.stddev_window.append(stddev)

        if len(self.stddev_window) > self.window_size:
            self.stddev_window.pop(0)

        return self.detect_quivering()

    def detect_quivering(self):
        if len(self.stddev_window) < self.window_size:
            return {"afib_score": 0.0, "label": "insufficient_data"}

        diffs = np.diff(self.stddev_window)
        jitter = np.std(diffs)

        afib_score = float(np.clip(jitter / self.jitter_threshold, 0, 1))

        if afib_score > 0.8:
            label = "quivering"
        elif afib_score > 0.5:
            label = "unstable"
        else:
            label = "stable"

        return {"afib_score": round(afib_score, 3), "label": label}
