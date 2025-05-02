# capture/serial_capture.py
from pymodbus.server import StartTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext
from pymodbus.device import ModbusDeviceIdentification
import logging
import time
import math
import random
import threading

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

def update_registers(context):
    t = 0
    while True:
        if t < 50:
            # Smooth drift simulation
            new_values = [
                int(50 + 10 * math.sin((t + i) / 10.0) + random.randint(-1, 1))
                for i in range(10)
            ]
        else:
            # Sudden anomaly
            new_values = [999 for _ in range(10)]
            print("[ALERT] Injected anomaly into holding registers")

        context[0].setValues(3, 0, new_values)
        print(f"[DEBUG] Registers at t={t}: {new_values}")
        t += 1
        time.sleep(3)

def open_serial_port(port_name):
    print(f"[DEBUG] Simulated port '{port_name}' opened.")
    return True

def capture_serial_data(serial_port, max_packets):
    print(f"[DEBUG] Starting Modbus TCP Server to simulate data...")

    store = ModbusSlaveContext(
        di=ModbusSequentialDataBlock(0, [17]*100),
        co=ModbusSequentialDataBlock(0, [17]*100),
        hr=ModbusSequentialDataBlock(0, [17]*100),
        ir=ModbusSequentialDataBlock(0, [17]*100)
    )
    context = ModbusServerContext(slaves=store, single=True)

    identity = ModbusDeviceIdentification()
    identity.VendorName = 'LineAlert'
    identity.ProductCode = 'LA'
    identity.VendorUrl = 'http://alertfortowns.org'
    identity.ProductName = 'LineAlert Sim PLC'
    identity.ModelName = 'SimPLC'
    identity.MajorMinorRevision = '1.0'

    updater_thread = threading.Thread(target=update_registers, args=(context,))
    updater_thread.daemon = True
    updater_thread.start()

    StartTcpServer(context, identity=identity, address=("localhost", 5020))
