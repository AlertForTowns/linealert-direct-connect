import os
import json
from datetime import datetime

# Placeholder paths (can be overridden later)
TRAIN_DIR = "/home/vboxuser/linealert-direct-connect/data/trains"

def load_train(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def print_cart(cart, index):
    print(f"─── Cart [{index}] @ {cart.get('timestamp', 'unknown')} ───")
    for k, v in cart.get('data', {}).items():
        print(f"{k}: {v}")
    meta = cart.get('meta', {})
    print(f"Drift Score: {meta.get('drift_score')} | Stddev Δ: {meta.get('stddev_delta')} | Label: {meta.get('label')}")
    print("")

def list_trains():
    files = [f for f in os.listdir(TRAIN_DIR) if f.endswith('.json')]
    return sorted(files)

def main():
    print("📦 LineAlert Train Viewer")
    trains = list_trains()

    if not trains:
        print("No train files found.")
        return

    for i, f in enumerate(trains):
        print(f"[{i}] {f}")

    choice = input("Select train to view [index]: ").strip()
    if not choice.isdigit() or int(choice) >= len(trains):
        print("Invalid selection.")
        return

    selected = trains[int(choice)]
    train_data = load_train(os.path.join(TRAIN_DIR, selected))

    print(f"\n=== Viewing Train: {selected} ===")
    for i, cart in enumerate(train_data.get('carts', [])):
        print_cart(cart, i)

if __name__ == "__main__":
    main()
