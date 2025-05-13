from pymodbus.server.sync import StartTcpServer
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.datastore.store import ModbusSequentialDataBlock
from pymodbus.device import ModbusDeviceIdentification
import threading
import random
import time

# --- Driftable Holding Register block ---
class DriftingDataBlock(ModbusSequentialDataBlock):
    def __init__(self, address, values):
        super().__init__(address, values)
        self.lock = threading.Lock()
        print(f"🧪 Initial values: {self.values}")
        self._start_drift_thread()

    def _start_drift_thread(self):
        def drift():
            while True:
                with self.lock:
                    for i in range(len(self.values)):
                        change = random.choice([-1, 0, 1])
                        self.values[i] = max(0, self.values[i] + change)
                time.sleep(1)
        t = threading.Thread(target=drift, daemon=True)
        t.start()

# --- Data store and context ---
block = DriftingDataBlock(0, [random.randint(90, 130) for _ in range(10)])
store = ModbusSlaveContext(hr=block)
context = ModbusServerContext(slaves=store, single=True)  # ✅ use single=True

# --- Identity metadata ---
identity = ModbusDeviceIdentification()
identity.VendorName = "LineAlertSim"
identity.ProductCode = "LA"
identity.VendorUrl = "http://linealert.dev"
identity.ProductName = "LineAlert Fake PLC"
identity.ModelName = "DriftSim"
identity.MajorMinorRevision = "1.0"

# --- Start TCP server ---
PORT = 5021
print(f"🚀 Simulated Modbus TCP server with drift on port {PORT}")
StartTcpServer(context, identity=identity, address=("127.0.0.1", PORT))
