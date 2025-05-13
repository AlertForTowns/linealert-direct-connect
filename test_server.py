from pymodbus.server.sync import StartTcpServer
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.datastore.store import ModbusSequentialDataBlock
from pymodbus.device import ModbusDeviceIdentification

block = ModbusSequentialDataBlock(0, [123] * 10)
store = ModbusSlaveContext(hr=block)
context = ModbusServerContext(slaves=store, single=True)

identity = ModbusDeviceIdentification()
identity.VendorName = "TestPLC"
identity.ProductCode = "TP01"
identity.ProductName = "SimpleServer"
identity.ModelName = "Sim1"
identity.MajorMinorRevision = "1.0"

print("✅ Minimal Modbus server running on 0.0.0.0:5021")
StartTcpServer(context, identity=identity, address=("0.0.0.0", 5021))
