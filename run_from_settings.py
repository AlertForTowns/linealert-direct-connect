# run_from_settings.py
import json
import linealert_cli

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

    # Emulate argparse args for CLI compatibility
    linealert_cli.args = Args()
    linealert_cli.main()

if __name__ == "__main__":
    run()
