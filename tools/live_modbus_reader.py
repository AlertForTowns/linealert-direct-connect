import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.afib_drift_detector import AFibDriftDetector
from tools.modbus_client_factory import get_modbus_client
from tools.snapshot_logger import save_snapshot

# --- Config ---
MODE = "tcp"
IP_ADDRESS = "127.0.0.1"
TCP_PORT = 5021
SERIAL_PORT = "/dev/ttyUSB0"
BAUDRATE = 9600

REGISTER_START = 0
REGISTER_COUNT = 10
POLL_INTERVAL = 2
ENABLE_SNAPSHOT_LOGGING = True
ENABLE_DUMMY_SNAPSHOT = False

afib = AFibDriftDetector()

def main():
    client = get_modbus_client(
        mode=MODE,
        ip=IP_ADDRESS,
        port=TCP_PORT,
        serial_port=SERIAL_PORT,
        baudrate=BAUDRATE
    )

    if not client.connect():
        print(f"❌ Failed to connect using {MODE.upper()}.")
        return

    print(f"✅ Connected via {MODE.upper()}")
    print("🚦 Polling begins...\n")

    try:
        while True:
            result = client.read_holding_registers(REGISTER_START, REGISTER_COUNT)

            if result.isError():
                print("⚠️  Modbus error:", result)
                time.sleep(POLL_INTERVAL)
                continue

            registers = {i: result.registers[i] for i in range(len(result.registers))}
            afib_result = afib.update(registers)

            print(f"📟 Registers: {registers}")
            print(f"💓 AFib Score: {afib_result['afib_score']} — Label: {afib_result['label']}")

            if ENABLE_SNAPSHOT_LOGGING:
                snapshot = {
                    "registers": registers,
                    "afib_score": afib_result['afib_score'],
                    "afib_label": afib_result['label'],
                    "timestamp": time.time()
                }
                print("📦 Saving encrypted snapshot...")
                save_snapshot(snapshot, prefix="linealert", encrypted=True)

            print("")
            time.sleep(POLL_INTERVAL)

    except KeyboardInterrupt:
        print("🛑 Polling stopped by user.")
    except Exception as e:
        print(f"🔥 Exception occurred: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    main()
