from pymodbus.client.sync import ModbusTcpClient as ModbusClient
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

# Modbus server configuration
MODBUS_SERVER = '172.17.0.2'  # Change if necessary
MODBUS_PORT = 5020  # Port number

# Connect to the server
client = ModbusClient(MODBUS_SERVER, port=MODBUS_PORT)
client.connect()

# Writing a value to a register
write_result = client.write_register(1, 9999, unit=1)  # Write 9999 to register 1

if write_result.isError():
    logging.error(f"Error writing to register: {write_result}")
else:
    logging.info(f"Successfully wrote value to register 1: {write_result}")

# Close the connection
client.close()
