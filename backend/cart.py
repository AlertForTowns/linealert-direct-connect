from datetime import datetime

class Cart:
    def __init__(self, snapshot):
        self.timestamp = datetime.utcnow().isoformat()
        self.data = snapshot  # dictionary of sensor data
        self.meta = {
            "label": "unlabeled",
            "drift_score": None,
            "stddev_delta": None
        }

    @classmethod
    def from_snapshot(cls, snapshot):
        return cls(snapshot)

    def to_dict(self):
        return {
            "timestamp": self.timestamp,
            "data": self.data,
            "label": self.meta.get("label"),
            "drift_score": self.meta.get("drift_score"),
            "stddev_delta": self.meta.get("stddev_delta")
        }

class Train:
    def __init__(self, id, role_id):
        self.id = id
        self.role_id = role_id
        self.created_at = datetime.utcnow().isoformat()
        self.carts = []

    def push(self, cart):
        self.carts.append(cart)
        print(f"Pushed Cart @ {cart.timestamp}: {cart.data}")

    def to_dict(self):
        return {
            "id": self.id,
            "role_id": self.role_id,
            "created_at": self.created_at,
            "carts": [cart.to_dict() for cart in self.carts]
        }
