import logging
from pymodbus.client.sync import ModbusTcpClient as ModbusClient

# Set up logging for easier debugging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger()

# Modbus Server Info
MODBUS_HOST = '192.168.0.16'  # IP Address of the Modbus Server
MODBUS_PORT = 5020            # Port for Modbus connection

def write_register(client, register, value):
    """
    Write a value to a specified register and log the result.
    """
    result = client.write_register(register, value, unit=1)
    if result.isError():
        log.error(f"Error writing to register {register}")
    else:
        log.info(f"Successfully wrote value {value} to register {register}")

def read_register(client, register):
    """
    Read the value from a specified register and log the result.
    """
    result = client.read_holding_registers(register, 1, unit=1)
    if result.isError():
        log.error(f"Error reading register {register}")
        return None
    else:
        value = result.registers[0]
        log.info(f"Register {register} value: {value}")
        return value

def main():
    """
    Main function to perform Modbus operations: writing and reading registers.
    """
    # Create Modbus TCP client
    client = ModbusClient(MODBUS_HOST, port=MODBUS_PORT)

    # Connect to Modbus server
    log.info(f"Connecting to Modbus server at {MODBUS_HOST}:{MODBUS_PORT}...")
    if client.connect():
        log.info("Successfully connected to Modbus server")
    else:
        log.error("Failed to connect to Modbus server")
        return

    # Example: Write a value to register 1 and verify it
    write_register(client, 1, 9999)  # Write 9999 to register 1
    read_register(client, 1)         # Read back the value of register 1

    # Additional operation: Write and read from more registers
    write_register(client, 10, 12345)  # Write 12345 to register 10
    read_register(client, 10)           # Read back the value of register 10

    # Close the Modbus connection
    client.close()

if __name__ == "__main__":
    main()
