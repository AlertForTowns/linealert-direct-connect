import numpy as np

class AFIBDriftDetector:
    def __init__(self, window_size=10, threshold=5):
        self.window_size = window_size
        self.threshold = threshold
        self.previous_values = []

    def detect_drift(self, current_value):
        self.previous_values.append(current_value)
        if len(self.previous_values) > self.window_size:
            self.previous_values.pop(0)
        avg_past_values = np.mean(self.previous_values)
        drift_percentage = ((current_value - avg_past_values) / avg_past_values) * 100
        if abs(drift_percentage) > self.threshold:
            alert_level = "RED" if abs(drift_percentage) > 25 else "YELLOW"
            alert_message = f"Drift detected! Previous avg: {avg_past_values:.2f}, Current value: {current_value:.2f}, Drift: {drift_percentage:.2f}%"
            return alert_level, alert_message
        return "GREEN", f"System stable, drift: {drift_percentage:.2f}%"

    def reset(self):
        self.previous_values = []
