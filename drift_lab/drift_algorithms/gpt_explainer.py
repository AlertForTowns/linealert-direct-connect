
def detect_drift(data):
    # Stub - would connect to OpenAI API or internal GPT endpoint
    context = data.get("context", {})
    return {
        "drift_score": 1,
        "explanation": "This would be replaced by GPT-generated context summary.",
        "context_considered": context
    }
