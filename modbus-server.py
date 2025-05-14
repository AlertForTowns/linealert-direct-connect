from pymodbus.server.sync import StartTcpServer
from pymodbus.datastore import ModbusSparseDataBlock
from pymodbus.datastore import ModbusServerContext
from pymodbus.device import ModbusDeviceIdentification

# Define the registers (e.g., Holding Registers at address 0)
data = {
    0: 25.5,   # Example value (can be updated dynamically)
    1: 32.1,
    2: 45.0
}

# Create a Modbus data block and assign it to a Modbus context
store = ModbusSparseDataBlock(data)
context = ModbusServerContext(historian=store, single=True)

# Set up the Modbus TCP server on port 5020
identity = ModbusDeviceIdentification()
identity.VendorName = 'Your Company'
identity.ProductCode = 'Modbus Server'

# Start the server
StartTcpServer(context, identity=identity, address=("0.0.0.0", 5020))
