
def detect_drift(data):
    metrics = data['metrics']
    context = data['context']
    drift_score = 0
    notes = []

    # Basic forward/backward edge check simulation
    baseline = {
        "pressure": 110,
        "temperature": 45,
        "flow": 220,
        "rpm": 1440
    }

    for k in baseline:
        change = abs(metrics[k] - baseline[k])
        if change > 15:
            drift_score += 1
            notes.append(f"{k} drifted by {change} units")

    if drift_score > 2:
        notes.append("Possible recursive edge state")

    return {
        "drift_score": drift_score,
        "explanation": " | ".join(notes),
        "context_considered": context
    }
