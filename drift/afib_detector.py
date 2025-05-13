import numpy as np

class AFIBDriftDetector:
    def __init__(self, window_size=10, threshold=10):
        self.window_size = window_size  # Rolling window to track signal changes
        self.threshold = threshold  # Drift threshold percentage
        self.previous_values = []  # To store past values for comparison
    
    def detect_drift(self, current_value):
        """
        Detects drift by comparing current value to past values within a window.
        Returns the drift percentage and alerts if drift exceeds the threshold.
        """
        # Append the current value to the previous values list
        self.previous_values.append(current_value)

        # Maintain the rolling window
        if len(self.previous_values) > self.window_size:
            self.previous_values.pop(0)

        # Calculate the average of the past values
        avg_past_values = np.mean(self.previous_values)

        # Calculate drift percentage
        drift_percentage = ((current_value - avg_past_values) / avg_past_values) * 100

        # Check if drift exceeds the threshold
        if abs(drift_percentage) > self.threshold:
            alert_level = "RED" if abs(drift_percentage) > 25 else "YELLOW"
            alert_message = f"Drift detected! Previous avg: {avg_past_values:.2f}, Current value: {current_value:.2f}, Drift: {drift_percentage:.2f}%"
            return alert_level, alert_message

        return "GREEN", f"System stable, drift: {drift_percentage:.2f}%"
        
    def reset(self):
        """Reset the drift detector for a new session."""
        self.previous_values = []

# Example usage
if __name__ == "__main__":
    detector = AFIBDriftDetector(window_size=10, threshold=10)
    
    # Simulate new data coming in
    data_stream = [100, 101, 103, 105, 107, 120, 130, 140, 150, 160]  # Simulating drift data
    for value in data_stream:
        alert_level, alert_message = detector.detect_drift(value)
        print(f"{alert_level}: {alert_message}")
