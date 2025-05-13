# tools/decrypt_lasnap.py

import os
import sys
import json
from Crypto.Cipher import AES

# --- AES Config (must match logger) ---
AES_KEY = b"ThisIsA32ByteLongSecretKeyForAES!!"
AES_IV_SIZE = 16
FALLBACK_DIRS = ["snapshots", "snapshot"]

# --- Decryption Helpers ---
def unpad(padded):
    pad_len = padded[-1]
    return padded[:-pad_len]

def decrypt_file(path):
    with open(path, "rb") as f:
        blob = f.read()
    iv = blob[:AES_IV_SIZE]
    ciphertext = blob[AES_IV_SIZE:]
    cipher = AES.new(AES_KEY, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(ciphertext)
    unpadded = unpad(decrypted)
    return json.loads(unpadded.decode("utf-8"))

# --- Utility: Find folder with .lasnap files ---
def find_snapshot_folder():
    for d in FALLBACK_DIRS:
        if os.path.isdir(d):
            return d
    return None

def list_snapshots(folder):
    print(f"\n🗂 Available snapshots in `{folder}/`:\n")
    lasnaps = [f for f in os.listdir(folder) if f.endswith(".lasnap")]
    if not lasnaps:
        print("❌ No .lasnap files found.")
        return None
    for i, f in enumerate(lasnaps):
        print(f"  [{i}] {f}")
    return lasnaps

# --- Report Writer ---
def write_report(data, filepath):
    report_path = filepath.replace(".lasnap", ".report.txt")
    with open(report_path, "w") as report:
        report.write("🔍 LineAlert Snapshot Report\n")
        report.write(f"📅 Timestamp: {data['timestamp']}\n")
        report.write(f"💓 AFib Score: {data['afib_score']} — Label: {data['afib_label']}\n")
        report.write(f"📟 Registers: {json.dumps(data['registers'], indent=2)}\n")
    print(f"📝 Human-readable report saved to {report_path}")

# --- Main ---
if __name__ == "__main__":
    if len(sys.argv) == 2:
        filepath = sys.argv[1]
        data = decrypt_file(filepath)
        print(json.dumps(data, indent=2))
        write_report(data, filepath)
    else:
        folder = find_snapshot_folder()
        if not folder:
            print("❌ Could not find 'snapshots/' or 'snapshot/' folder.")
            sys.exit(1)

        files = list_snapshots(folder)
        if not files:
            sys.exit(1)

        try:
            choice = int(input("\n🔢 Enter file number to decrypt: "))
            filename = files[choice]
            filepath = os.path.join(folder, filename)
            data = decrypt_file(filepath)
            print(f"\n✅ Decrypted: {filename}\n")
            print(json.dumps(data, indent=2))
            write_report(data, filepath)
        except (ValueError, IndexError):
            print("❌ Invalid selection.")
        except Exception as e:
            print(f"🔥 Error: {e}")
