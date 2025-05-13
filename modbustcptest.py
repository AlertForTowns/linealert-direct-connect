import modbus_tk
import modbus_tk.modbus_tcp as modbus_tcp

# Modbus server settings
MODBUS_IP = "192.168.0.16"
MODBUS_PORT = 502
SLAVE_ID = 1  # Replace with the correct slave ID if different

# Create Modbus TCP client
client = modbus_tcp.TcpMaster(MODBUS_IP, MODBUS_PORT)
client.set_timeout(5.0)

def read_modbus_registers(start_address, count):
    try:
        # Read Holding Registers
        result = client.execute(SLAVE_ID, modbus_tk.defines.READ_HOLDING_REGISTERS, start_address, count)
        print(f"Data read from address {start_address}: {result}")
        return result
    except modbus_tk.modbus.ModbusError as e:
        print(f"Error reading Modbus registers: {e}")
        return None

if __name__ == "__main__":
    print(f"Connecting to Modbus server at {MODBUS_IP}:{MODBUS_PORT}...")
    
    # Test reading holding registers at different addresses
    for address in [0, 10, 50, 100, 200]:
        print(f"\nTesting address {address}...")
        result = read_modbus_registers(address, 10)
        if result:
            if all(value == 0 for value in result):
                print(f"Warning: All values returned 0 for address {address}")
            else:
                print(f"Successfully read data from address {address}: {result}")
        else:
            print(f"Failed to read data from address {address}.")
