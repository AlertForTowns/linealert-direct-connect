import os
import json
import dotenv
from openai import OpenAI
from pathlib import Path

# Load API key from .env
dotenv.load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Input and output paths
TRAIN_PATH = "../data/trains/train_panasonic_modbus.json"
ANNOTATED_PATH = TRAIN_PATH.replace(".json", "_annotated.json")

def annotate_cart(cart, train_context):
    prompt = f"""
You are a drift analysis assistant for a PLC monitoring tool.

Each Cart represents a snapshot of register values at a point in time.
Below is a Cart from a Train log, followed by previous context.

Cart:
{json.dumps(cart, indent=2)}

Context:
Train ID: {train_context['id']}
Role ID: {train_context['role_id']}
Created At: {train_context['created_at']}

Label the Cart as one of:
- stable
- warning
- unstable
- anomaly

Explain in 1 sentence why.

Respond only as JSON like:
{{"label": "...", "reason": "..."}}
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a drift labeling AI."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return json.loads(response.choices[0].message.content.strip())

def main():
    if not Path(TRAIN_PATH).exists():
        print(f"[!] No train file found at {TRAIN_PATH}")
        return

    with open(TRAIN_PATH, "r") as f:
        train = json.load(f)

    annotated = []
    for cart in train["carts"]:
        enriched = annotate_cart(cart, train)
        
        if "meta" not in cart:
            cart["meta"] = {}

        cart["meta"]["gpt_label"] = enriched["label"]
        cart["meta"]["gpt_reason"] = enriched["reason"]
        annotated.append(cart)

    train["carts"] = annotated

    with open(ANNOTATED_PATH, "w") as f:
        json.dump(train, f, indent=2)

    print(f"[✓] Annotated train saved to {ANNOTATED_PATH}")

if __name__ == "__main__":
    main()
