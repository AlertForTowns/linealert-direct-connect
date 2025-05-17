from pymodbus.server.sync import ModbusTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext, ModbusSequentialDataBlock

# Create data store
store = ModbusSlaveContext(
    di=ModbusSequentialDataBlock(0, [17]*100),
    co=ModbusSequentialDataBlock(0, [17]*100),
    hr=ModbusSequentialDataBlock(0, [17]*100),
    ir=ModbusSequentialDataBlock(0, [17]*100)
)

# ✅ CORRECT CONTEXT WRAPPER
context = ModbusServerContext(slaves=store, single=True)

# Server identity (optional)
identity = ModbusDeviceIdentification()
identity.VendorName = 'PyModbus'
identity.ProductCode = 'PM'
identity.VendorUrl = 'http://github.com/pymodbus/pymodbus'
identity.ProductName = 'PyModbus Server'
identity.ModelName = 'PyModbus Model'
identity.MajorMinorRevision = '1.0'

# Start the server
server = ModbusTcpServer(context, identity=identity, address=("0.0.0.0", 5020))
server.serve_forever()
