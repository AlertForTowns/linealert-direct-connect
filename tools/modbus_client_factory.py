from pymodbus.client.sync import ModbusTcpClient, ModbusSerialClient

def get_modbus_client(mode, ip=None, port=502, serial_port=None, baudrate=9600):
    if mode == "tcp":
        return ModbusTcpClient(ip, port=port)
    elif mode == "rtu":
        return ModbusSerialClient(
            method='rtu',
            port=serial_port,
            baudrate=baudrate,
            timeout=1,
            stopbits=1,
            bytesize=8,
            parity='N'
        )
    else:
        raise ValueError("MODE must be 'tcp' or 'rtu'")
