import modbus_tk
import modbus_tk.modbus_tcp as modbus_tcp

def check_modbus_server(ip, port):
    try:
        # Set up client
        client = modbus_tcp.TcpMaster(ip, port)
        client.set_timeout(5.0)
        print(f"Connected to Modbus server at {ip}:{port}")
        
        # Try reading holding registers from different starting addresses
        test_addresses = [0, 10, 100, 200]  # Different register addresses to test
        num_registers = 10  # Number of registers to read in each test
        
        for addr in test_addresses:
            print(f"\nReading {num_registers} registers starting at address {addr}:")
            result = client.execute(1, modbus_tk.defines.READ_HOLDING_REGISTERS, addr, num_registers)
            print(f"Result: {result}")
            if all(value == 0 for value in result):
                print(f"Warning: All registers returned 0 for address {addr}.")
            else:
                print(f"Successfully read data from address {addr}.")
                
    except modbus_tk.modbus.ModbusError as e:
        print(f"Error connecting to Modbus server: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        # Close the connection
        client.close()
        print("\nConnection closed.")

if __name__ == "__main__":
    modbus_ip = "192.168.0.16"  # The IP address of your Modbus server
    modbus_port = 502  # The port your Modbus server is listening on
    
    check_modbus_server(modbus_ip, modbus_port)
