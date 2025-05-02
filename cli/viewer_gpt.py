# cli/viewer_gpt.py
import os
import json
from colorama import Fore, Style, init

init(autoreset=True)

TRAIN_PATH = "../data/trains/train_panasonic_modbus_annotated.json"

def color_label(label):
    if label == "stable":
        return Fore.GREEN + label + Style.RESET_ALL
    elif label == "warning":
        return Fore.YELLOW + label + Style.RESET_ALL
    elif label == "critical":
        return Fore.RED + label + Style.RESET_ALL
    else:
        return Fore.CYAN + label + Style.RESET_ALL

def list_available_labels(carts):
    labels = set()
    for cart in carts:
        label = cart.get("meta", {}).get("gpt_label", "unlabeled")
        labels.add(label)
    return sorted(labels)

def view_annotated_train():
    if not os.path.exists(TRAIN_PATH):
        print(Fore.RED + f"[!] Annotated train file not found at {TRAIN_PATH}")
        return

    with open(TRAIN_PATH, "r") as f:
        train = json.load(f)

    carts = train.get("carts", [])
    labels = list_available_labels(carts)

    print(Fore.MAGENTA + "\n🧠 GPT-Annotated Train Viewer")
    print(Fore.WHITE + f"Loaded {len(carts)} carts from: {TRAIN_PATH}")
    print(Fore.CYAN + f"Available labels: {', '.join(labels)}")
    selected = input(Fore.YELLOW + "Filter by label (or press Enter to view all): ").strip().lower()

    print()

    for i, cart in enumerate(carts):
        meta = cart.get("meta", {})
        gpt_label = meta.get("gpt_label", "unlabeled").lower()

        if selected and gpt_label != selected:
            continue

        gpt_reason = meta.get("gpt_reason", "No reason provided.")
        drift = meta.get("drift_score", 0.0)

        print(Fore.WHITE + f"─── Cart [{i}] @ {cart['timestamp']} ───")
        print("Drift Score:", round(drift, 3), "| Label:", color_label(gpt_label))
        print(Fore.CYAN + "GPT Reason:", gpt_reason)
        print()

if __name__ == "__main__":
    view_annotated_train()
