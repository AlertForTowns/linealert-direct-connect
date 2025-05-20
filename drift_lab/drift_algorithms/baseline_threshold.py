
def detect_drift(data):
    metrics = data['metrics']
    context = data['context']
    drift_score = 0

    if metrics['temperature'] > 50:
        drift_score += 2
    if metrics['pressure'] > 120 or metrics['pressure'] < 90:
        drift_score += 1
    if metrics['flow'] < 200:
        drift_score += 1
    if metrics['rpm'] < 1300:
        drift_score += 1

    return {
        "drift_score": drift_score,
        "explanation": f"Detected drift with score {drift_score} based on pressure, temp, and RPM",
        "context_considered": context
    }
