# security/encryptor.py
from Crypto.Cipher import AES
import base64
import os
import hashlib
import sys

BLOCK_SIZE = 16

def pad(data):
    pad_len = BLOCK_SIZE - len(data) % BLOCK_SIZE
    return data + (chr(pad_len) * pad_len).encode()

def encrypt_lasnap(input_path, output_path, password):
    with open(input_path, "rb") as f:
        raw = f.read()

    key = hashlib.sha256(password.encode()).digest()
    iv = os.urandom(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(pad(raw))

    with open(output_path, "wb") as f:
        f.write(iv + encrypted)

    print(f"[🔒] Encrypted snapshot saved: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python encryptor.py <input.lasnap> <output.enc> <password>")
        sys.exit(1)

    _, input_file, output_file, password = sys.argv
    encrypt_lasnap(input_file, output_file, password)
