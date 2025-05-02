import json
import sys
import os

# Add the current directory to sys.path so Python can find 'tools'
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from tools import linealert_cli as cli

def load_settings(path="settings.json"):
    with open(path, "r") as f:
        return json.load(f)

def run():
    settings = load_settings()

    class Args:
        port = settings["serial_port"]
        max = settings["max_packets"]
        encrypt = settings["encrypt_snapshot"]
        password = settings["encryption_password"]
        baseline = settings.get("baseline_profile")
        webhook = settings.get("webhook_url")

    cli.args = Args()
    cli.main()

if __name__ == "__main__":
    run()
