import json
from pathlib import Path
from datetime import datetime

snapshot_dir = Path(__file__).resolve().parent.parent / "snapshot"
snapshot_dir.mkdir(parents=True, exist_ok=True)

mock_snapshot = {
    "snapshot_id": "mock_snapshot",
    "captured_at": datetime.utcnow().isoformat() + "Z",
    "agent_version": "v1.0.0",
    "data": {
        "packets": [
            {
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "src": "10.0.0.5",
                "dst": "10.0.0.10",
                "protocol": "ModbusTCP",
                "function_code": 3,
                "register": 40001,
                "value": 120
            }
        ],
        "traffic_summary": {
            "total_packets": 1,
            "protocols": ["ModbusTCP"]
        }
    }
}

filename = snapshot_dir / "mock_snapshot.lasnap"
with open(filename, "w") as f:
    json.dump(mock_snapshot, f, indent=2)

print(f"✅ Generated {filename}")
