
def detect_drift(data):
    metrics = data['metrics']
    context = data['context']
    drift_score = 0
    pattern_flags = []

    # Detect irregular "spikes" in data values compared to expected stability
    if abs(metrics['rpm'] - 1440) > 100:
        drift_score += 2
        pattern_flags.append("RPM arrhythmia")
    if metrics['pressure'] > 125 or metrics['pressure'] < 85:
        drift_score += 1
        pattern_flags.append("Pressure irregularity")
    if metrics['flow'] > 260 or metrics['flow'] < 150:
        drift_score += 1
        pattern_flags.append("Flow deviation")

    return {
        "drift_score": drift_score,
        "explanation": f"Afib-style drift detected: {', '.join(pattern_flags)}",
        "context_considered": context
    }
