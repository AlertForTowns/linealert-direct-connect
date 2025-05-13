from pymodbus.client.sync import ModbusTcpClient

# Connect to Modbus server
client = ModbusTcpClient('127.0.0.1', port=15022)
client.connect()

# Try reading the first 5 registers starting from address 0
result = client.read_holding_registers(0, 5, unit=1)

# Check if the result contains an error
if result.isError():
    print(f"Error reading registers: {result}")
else:
    print(f"Registers read successfully: {result.registers}")

client.close()
