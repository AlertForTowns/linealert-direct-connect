from pymodbus.client.sync import ModbusTcpClient

# Modbus server connection details
MODBUS_SERVER_IP = '127.0.0.1'
MODBUS_SERVER_PORT = 15022

# Create a Modbus TCP client
client = ModbusTcpClient(MODBUS_SERVER_IP, port=MODBUS_SERVER_PORT)

# Connect to the server
connection = client.connect()
if not connection:
    print("Failed to connect to Modbus server.")
else:
    # Read the first 5 holding registers (addresses 0, 1, 2, 3, 4)
    result = client.read_holding_registers(0, 5, unit=1)
    if result.isError():
        print(f"Error reading registers: {result}")
    else:
        print(f"Registers read successfully: {result.registers}")

    # Close the connection
    client.close()
