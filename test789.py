import logging




from pymodbus.client.sync import ModbusTcpClient

logging.basicConfig(level=logging.DEBUG)

# Enable logging to capture Modbus client activity
logging.basicConfig(level=logging.DEBUG)

# Modbus server connection details
MODBUS_SERVER_IP = '127.0.0.1'
MODBUS_SERVER_PORT = 15022

client = ModbusTcpClient(MODBUS_SERVER_IP, port=MODBUS_SERVER_PORT)
client.connect()

# Read first 5 holding registers (addresses 0, 1, 2, 3, 4)
result = client.read_holding_registers(0, 5, unit=1)

if result.isError():
    print(f"Error reading registers: {result}")
else:
    print(f"Registers read successfully: {result.registers}")

client.close()
