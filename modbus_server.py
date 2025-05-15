from pymodbus.server.sync import ModbusTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSlaveContext, ModbusSequentialDataBlock  # Correct imports
from pymodbus.client.sync import ModbusTcpClient

# Initialize the datastore with sequential data blocks
store = ModbusSlaveContext(
    di=ModbusSequentialDataBlock(0, [17]*100),  # Digital Inputs
    co=ModbusSequentialDataBlock(0, [17]*100),  # Coils
    hr=ModbusSequentialDataBlock(0, [17]*100),  # Holding Registers
    ir=ModbusSequentialDataBlock(0, [17]*100)   # Input Registers
)

# Use ModbusSlaveContext instead of ModbusServerContext
context = ModbusSlaveContext(slaves=store, single=True)

# Configure server identity
identity = ModbusDeviceIdentification()
identity.VendorName = 'PyModbus'
identity.ProductCode = 'PM'
identity.VendorUrl = 'http://github.com/pymodbus/pymodbus'
identity.ProductName = 'PyModbus Server'
identity.ModelName = 'PyModbus Model'
identity.MajorMinorRevision = '1.0'

# Start the TCP server
server = ModbusTcpServer(context, identity=identity, address=("0.0.0.0", 5020))
server.serve_forever()
