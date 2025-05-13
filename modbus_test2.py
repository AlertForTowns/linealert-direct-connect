import modbus_tk
import modbus_tk.modbus_tcp as modbus_tcp
import logging

# Set up logging for better visibility
logging.basicConfig(level=logging.DEBUG)

MODBUS_IP = "192.168.0.16"  # Server IP address (or use 172.17.0.2)
MODBUS_PORT = 502           # Port for Modbus TCP

def test_modbus():
    try:
        # Set up Modbus TCP client
        client = modbus_tcp.TcpMaster(MODBUS_IP, MODBUS_PORT)
        client.set_timeout(5.0)  # Timeout for requests
        logging.info(f"Connected to Modbus server at {MODBUS_IP}:{MODBUS_PORT}")

        # Test reading Holding Registers
        for address in [0, 10, 50, 100, 200]:
            try:
                logging.info(f"Reading Holding Registers starting at address {address}...")
                result = client.execute(1, modbus_tk.defines.READ_HOLDING_REGISTERS, address, 10)
                logging.info(f"Data read from address {address}: {result}")
                if all(value == 0 for value in result):
                    logging.warning(f"Warning: All values returned 0 for address {address} with Holding Registers.")
            except Exception as e:
                logging.error(f"Failed to read Holding Registers from address {address}: {e}")

        # Test reading Input Registers
        for address in [0, 10, 50, 100, 200]:
            try:
                logging.info(f"Reading Input Registers starting at address {address}...")
                result = client.execute(1, modbus_tk.defines.READ_INPUT_REGISTERS, address, 10)
                logging.info(f"Data read from address {address}: {result}")
                if all(value == 0 for value in result):
                    logging.warning(f"Warning: All values returned 0 for address {address} with Input Registers.")
            except Exception as e:
                logging.error(f"Failed to read Input Registers from address {address}: {e}")

    except modbus_tk.modbus.ModbusError as e:
        logging.error(f"Modbus error: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")

if __name__ == "__main__":
    test_modbus()
