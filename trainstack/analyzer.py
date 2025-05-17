class DriftAnalyzer:
    def __init__(self, threshold=10):
        self.threshold = threshold

    def detect_drift(self, history):
        if not history or len(history) < 2:
            return False
        diffs = [abs(history[i] - history[i - 1]) for i in range(1, len(history))]
        avg_drift = sum(diffs) / len(diffs)
        return avg_drift > self.threshold
