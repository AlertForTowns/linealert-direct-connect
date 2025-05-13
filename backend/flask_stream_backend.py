import random
import time
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Simulated drift data storage
drift_data = []

# Apply drift to the drift_data
def apply_drift():
    global drift_data
    for entry in drift_data:
        # Ensure the 'history' key exists for each entry
        if 'history' not in entry:
            entry['history'] = []
        
        previous_value = entry["value"]
        drift_percentage = random.uniform(30.0, 70.0)  # Increased drift range (30% to 70%)
        entry["value"] += entry["value"] * drift_percentage / 100  # Apply the drift

        # Store previous value to calculate the drift percentage more accurately
        entry["previous_value"] = previous_value

        # Record history for drift analysis
        entry["history"].append(previous_value)

        # Update severity based on the drift
        if drift_percentage > 50:
            entry["severity"] = "Bad"
        elif drift_percentage > 30:
            entry["severity"] = "Moderate"
        else:
            entry["severity"] = "Low"

        print(f"Tag: {entry['tag']}, Previous: {previous_value}, New Value: {entry['value']}, Change: {drift_percentage}%")

# Serve drift data
@app.route("/drift", methods=["POST"])
def post_drift_data():
    global drift_data
    drift_data = request.json  # Receive new drift data
    apply_drift()  # Apply drift after receiving new data
    return jsonify({"status": "success", "message": "Drift data received and drift applied"}), 200

# Serve the drift data to frontend
@app.route("/drift", methods=["GET"])
def get_drift_data():
    return jsonify(drift_data)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5007)
