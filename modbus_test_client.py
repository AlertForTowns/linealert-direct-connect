from pymodbus.client import ModbusTcpClient

client = ModbusTcpClient("localhost", port=5020)
client.connect()

response = client.read_holding_registers(address=0, count=10, slave=0)
if response.isError():
    print("Error reading registers:", response)
else:
    print("Read Holding Registers:", response.registers)

client.close()
