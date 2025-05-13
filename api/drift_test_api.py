from flask import Flask, request, jsonify
import json
from pathlib import Path

app = Flask(__name__)

SNAPSHOT_DIR = Path(__file__).resolve().parent.parent / "snapshot"
PROFILE_PATH = Path(__file__).resolve().parent.parent / "profiles" / "HVAC_Controller_01.json"

def load_profile():
    if not PROFILE_PATH.exists():
        return {}
    with open(PROFILE_PATH, "r") as f:
        return json.load(f)

def extract_registers(content):
    if "snapshot" in content:
        content = content["snapshot"]
    packets = content.get("data", {}).get("packets", [])
    for p in packets:
        if p.get("protocol") == "ModbusTCP" and "register" in p and "value" in p:
            yield str(p["register"]), p["value"]

@app.route("/api/drift-test", methods=["POST"])
def drift_test():
    if 'snapshot' not in request.files:
        return jsonify({"error": "No file uploaded."}), 400

    uploaded_file = request.files['snapshot']
    print("📦 RECEIVED SIZE:", uploaded_file.content_length)

    try:
        snapshot_str = uploaded_file.stream.read().decode('utf-8')
        content = json.loads(snapshot_str)
    except Exception as e:
        return jsonify({"error": f"Invalid JSON: {str(e)}"}), 400

    profile = load_profile()
    violations = []

    for reg_id, value in extract_registers(content):
        entry = profile.get(reg_id)
        if not entry:
            violations.append({
                "register": reg_id,
                "value": value,
                "min": None,
                "max": None,
                "reason": "Not in profile"
            })
            continue

        if not (entry["min"] <= value <= entry["max"]):
            violations.append({
                "register": reg_id,
                "value": value,
                "min": entry["min"],
                "max": entry["max"]
            })

    return jsonify({
        "passed": len(violations) == 0,
        "violations": violations
    })

@app.route("/api/learn", methods=["POST"])
def learn_register():
    try:
        data = request.get_json()
        reg = str(data["register"])
        val = int(data["value"])
    except Exception as e:
        return jsonify({"error": f"Invalid input: {str(e)}"}), 400

    profile = {}
    if PROFILE_PATH.exists():
        with open(PROFILE_PATH, "r") as f:
            profile = json.load(f)

    if reg not in profile:
        profile[reg] = {"min": val, "max": val}
    else:
        profile[reg]["min"] = min(profile[reg]["min"], val)
        profile[reg]["max"] = max(profile[reg]["max"], val)

    PROFILE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(PROFILE_PATH, "w") as f:
        json.dump(profile, f, indent=2)

    return jsonify({"status": "learned", "register": reg, "value": val})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
