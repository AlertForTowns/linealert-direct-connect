from pymodbus.client.sync import ModbusTcpClient as ModbusClient
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

# Config for Modbus server
MODBUS_SERVER = '172.17.0.2'  # Change to your server IP if needed
MODBUS_PORT = 5020  # The port you're connecting to
START_ADDRESS = 0  # Starting register address to test
NUM_REGISTERS = 10  # Number of registers to read

client = ModbusClient(MODBUS_SERVER, port=MODBUS_PORT)

# Connect to the Modbus server
client.connect()

# Attempt to read holding registers
try:
    result = client.read_holding_registers(START_ADDRESS, NUM_REGISTERS, unit=1)

    if result.isError():
        logging.error(f"Error reading holding registers: {result}")
    else:
        logging.info(f"Data read from address {START_ADDRESS}: {result.registers}")
        # Check if the values are within the acceptable range
        for i, value in enumerate(result.registers):
            if value > 65535 or value < 0:
                logging.error(f"Register {START_ADDRESS + i} has an invalid value: {value}")
            else:
                logging.info(f"Register {START_ADDRESS + i} value: {value}")
except Exception as e:
    logging.error(f"Exception occurred: {e}")
finally:
    client.close()

