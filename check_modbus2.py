import modbus_tk
import modbus_tk.modbus_tcp as modbus_tcp
import time

def check_modbus_server(ip, port):
    try:
        # Set up client
        client = modbus_tcp.TcpMaster(ip, port)
        client.set_timeout(5.0)
        print(f"Connected to Modbus server at {ip}:{port}")
        
        # Define test parameters
        test_addresses = [0, 10, 100, 200, 300, 400]  # Multiple register addresses to test
        num_registers = 10  # Number of registers to read in each test
        read_functions = [
            ("Holding Registers", modbus_tk.defines.READ_HOLDING_REGISTERS),
            ("Input Registers", modbus_tk.defines.READ_INPUT_REGISTERS),
            ("Discrete Inputs", modbus_tk.defines.READ_DISCRETE_INPUTS),
        ]
        
        # Loop through read functions and test with different register addresses
        for func_name, func_code in read_functions:
            print(f"\nTesting {func_name}:")

            for addr in test_addresses:
                print(f"Reading {num_registers} registers starting at address {addr} using {func_name}:")
                
                try:
                    result = client.execute(1, func_code, addr, num_registers)
                    print(f"Result: {result}")

                    # Check if all values are zero
                    if all(value == 0 for value in result):
                        print(f"Warning: All registers returned 0 for address {addr} with {func_name}.")
                    else:
                        print(f"Successfully read data from address {addr} using {func_name}.")

                except modbus_tk.modbus.ModbusError as e:
                    print(f"Modbus Error: {e}")
                    print(f"Failed to read from address {addr} using {func_name}.")

                time.sleep(1)  # Optional: sleep between tests to avoid overwhelming the server
        
        # Check server responsiveness and return results
        print("\nTesting completed.")
    
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
