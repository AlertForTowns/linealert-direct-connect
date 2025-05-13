import modbus_tk
import modbus_tk.modbus_tcp as modbus_tcp
import logging

logger = modbus_tk.utils.create_logger("console")
server = modbus_tcp.TcpServer(address="0.0.0.0", port=502)
logger.info("Starting Modbus TCP server...")

try:
    server.start()
    slave = server.add_slave(1)
    slave.add_block("block1", modbus_tk.defines.HOLDING_REGISTERS, 0, 10)
    slave.set_values("block1", 0, [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000])

    logger.info("Server running...")
    server.stop()
except Exception as e:
    logger.error(f"Error starting Modbus server: {e}")
