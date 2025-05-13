from pymodbus.client.sync import ModbusTcpClient

def read_and_print(ip, port, unit_id, label):
    client = ModbusTcpClient(ip, port=port)
    client.connect()
    result = client.read_holding_registers(0, 5, unit=unit_id)
    if result.isError():
        print(f"❌ {label} error:", result)
    else:
        print(f"✅ {label} Register values:", result.registers)
    client.close()

# First 5 registers
read_and_print("127.0.0.1", 15021, unit_id=1, label="Drift Server A")

# Second 5 registers (you need to run this second container on port 15022)
read_and_print("127.0.0.1", 15022, unit_id=1, label="Drift Server B")
