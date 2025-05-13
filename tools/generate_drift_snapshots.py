import json
from pathlib import Path
from datetime import datetime, timedelta

snapshot_dir = Path(__file__).resolve().parent.parent / "linealert" / "snapshot"
snapshot_dir.mkdir(parents=True, exist_ok=True)

base_time = datetime.utcnow()

for i in range(4):
    drift_snapshot = {
        "snapshot_id": f"drift_snapshot_{i+1}",
        "captured_at": (base_time + timedelta(minutes=i)).isoformat() + "Z",
        "agent_version": "v1.0.0-drift",
        "data": {
            "packets": [
                {
                    "timestamp": (base_time + timedelta(minutes=i)).isoformat() + "Z",
                    "src": "10.0.0.5",
                    "dst": "10.0.0.10",
                    "protocol": "ModbusTCP",
                    "function_code": 3,
                    "register": 40001,
                    "value": 100 + (i * 10)
                }
            ],
            "traffic_summary": {
                "total_packets": 1,
                "protocols": ["ModbusTCP"]
            }
        }
    }

    filename = snapshot_dir / f"drift_snapshot_{i+1}.lasnap"
    with open(filename, "w") as f:
        json.dump(drift_snapshot, f, indent=2)

print("✅ Drift snapshots generated.")
