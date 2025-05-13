# tools/snapshot_logger.py

import os
import json
from datetime import datetime
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# --- Config ---
SNAPSHOT_DIR = "snapshot"  # Match your actual folder name
AES_KEY = b"ThisIsA32ByteLongSecretKeyForAES"  # 32 bytes for AES-256
AES_IV_SIZE = 16
MAX_SNAPSHOTS = 50  # Max number of .lasnap files to retain

# --- Padding Helpers ---
def pad(data):
    pad_len = 16 - (len(data) % 16)
    return data + bytes([pad_len]) * pad_len

# --- Encryption ---
def encrypt_snapshot(data_dict):
    raw = pad(json.dumps(data_dict).encode("utf-8"))
    iv = get_random_bytes(AES_IV_SIZE)
    cipher = AES.new(AES_KEY, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(raw)
    return iv + encrypted  # prepend IV

# --- Snapshot Saver ---
def save_snapshot(data_dict, prefix="linealert", encrypted=True):
    os.makedirs(SNAPSHOT_DIR, exist_ok=True)
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    ext = ".lasnap" if encrypted else ".json"
    filename = f"{prefix}_{timestamp}{ext}"
    filepath = os.path.join(SNAPSHOT_DIR, filename)

    if encrypted:
        blob = encrypt_snapshot(data_dict)
        with open(filepath, "wb") as f:
            f.write(blob)
    else:
        with open(filepath, "w") as f:
            json.dump(data_dict, f, indent=2)

    print(f"📁 Snapshot saved to {filepath}")
    rotate_snapshots(SNAPSHOT_DIR)
    return filepath

# --- Auto-Prune Old Snapshots ---
def rotate_snapshots(directory=SNAPSHOT_DIR, keep=MAX_SNAPSHOTS):
    files = sorted(
        [f for f in os.listdir(directory) if f.endswith(".lasnap")],
        key=lambda f: os.path.getmtime(os.path.join(directory, f))
    )
    excess = len(files) - keep
    if excess > 0:
        for old_file in files[:excess]:
            os.remove(os.path.join(directory, old_file))
            print(f"🧹 Deleted old snapshot: {old_file}")
