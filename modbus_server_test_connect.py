from pymodbus.client.sync import ModbusTcpClient

# Replace with correct IP address
client = ModbusTcpClient('127.0.0.1', port=5020)
client.connect()
response = client.read_holding_registers(0, 1)  # Try reading register 0
print(response)
client.close()
