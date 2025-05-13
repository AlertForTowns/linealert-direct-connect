import json
import time
from pymodbus.server import StartTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext
from pymodbus.device import ModbusDeviceIdentification
from datetime import datetime
import argparse

def replay_train(template_path, interval=3):
    with open(template_path, "r") as f:
        train = json.load(f)

    carts = train.get("carts", [])
    if not carts:
        print("[!] No carts found in template.")
        return

    # Setup Modbus datastore
    store = ModbusSlaveContext(
        hr=ModbusSequentialDataBlock(0, [0]*100)
    )
    context = ModbusServerContext(slaves=store, single=True)

    identity = ModbusDeviceIdentification()
    identity.VendorName = 'LineAlert'
    identity.ProductCode = 'REPLAY'
    identity.VendorUrl = 'http://alertfortowns.org'
    identity.ProductName = 'LineAlert Replay PLC'
    identity.ModelName = 'ReplayPLC'
    identity.MajorMinorRevision = '1.0'

    def replay_loop():
        for cart in carts:
            snapshot = cart.get("data", {})
            values = [snapshot.get(f"reg_{i}", 0) for i in range(10)]
            print(f"[REPLAY] {cart['timestamp']} -> {values}")
            context[0].setValues(3, 0, values)
            time.sleep(interval)

    import threading
    thread = threading.Thread(target=replay_loop)
    thread.daemon = True
    thread.start()

    print("[*] Starting Modbus server on localhost:5021 for replay...")
    StartTcpServer(context, identity=identity, address=("localhost", 5021))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Replay drift template as Modbus TCP server")
    parser.add_argument("template", help="Path to template JSON file")
    parser.add_argument("--interval", type=int, default=3, help="Seconds between register updates")
    args = parser.parse_args()

    replay_train(args.template, interval=args.interval)
