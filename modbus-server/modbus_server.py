import argparse
import json
import logging
import os
import socket
import sys
import threading
from typing import Literal, Optional

from pymodbus.datastore import (
    ModbusSequentialDataBlock,
    ModbusServerContext,
    ModbusSlaveContext,
    ModbusSparseDataBlock,
)
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.server.sync import StartTcpServer, StartTlsServer, StartUdpServer
from flask import Flask, jsonify, request

# Default configuration file path
default_config_file = "/app/modbus_server.json"
VERSION = "1.4.0"

# Initialize logging
log = logging.getLogger()

# Flask app for drift data endpoint
app = Flask(__name__)

@app.route('/drift', methods=['POST'])
def drift():
    """
    Handle incoming drift data.
    """
    drift_data = request.json
    log.debug(f"Received drift data: {drift_data}")
    return jsonify({"status": "success", "message": "Drift data received"})

def get_ip_address() -> str:
    """
    Get the IP address of the outbound Ethernet interface
    @return: string, IP address
    """
    ipaddr = ""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ipaddr = s.getsockname()[0]
    except Exception:
        pass
    return ipaddr

def run_server(
    listener_address: str = "0.0.0.0",
    listener_port: int = 5020,
    protocol: str = "TCP",
    tls_cert: str = None,
    tls_key: str = None,
    zero_mode: bool = False,
    discrete_inputs: Optional[dict] = None,
    coils: Optional[dict] = None,
    holding_registers: Optional[dict] = None,
    input_registers: Optional[dict] = None,
):
    """
    Run the Modbus server(s)
    """
    log.debug(f"Initialize discrete input")
    di = ModbusSequentialDataBlock.create() if not discrete_inputs else ModbusSparseDataBlock(discrete_inputs)
    log.debug(f"Initialize coils")
    co = ModbusSequentialDataBlock.create() if not coils else ModbusSparseDataBlock(coils)
    log.debug(f"Initialize holding registers")
    hr = ModbusSequentialDataBlock.create() if not holding_registers else ModbusSparseDataBlock(holding_registers)
    log.debug(f"Initialize input registers")
    ir = ModbusSequentialDataBlock.create() if not input_registers else ModbusSparseDataBlock(input_registers)

    store = ModbusSlaveContext(di=di, co=co, hr=hr, ir=ir, zero_mode=zero_mode)

    log.debug(f"Define Modbus server context")
    context = ModbusServerContext(slaves=store, single=True)

    # Define Modbus server identity
    identity = ModbusDeviceIdentification()
    identity.VendorName = "Pymodbus"
    identity.ProductCode = "PM"
    identity.VendorUrl = "http://github.com/riptideio/pymodbus/"
    identity.ProductName = "Pymodbus Server"
    identity.ModelName = "Pymodbus Server"
    identity.MajorMinorRevision = "2.5.3"

    # Run the server
    if tls_cert and tls_key:
        log.info(f"Starting Modbus server with TLS on {listener_address}:{listener_port}")
        StartTlsServer(context, identity=identity, certfile=tls_cert, keyfile=tls_key, address=(listener_address, listener_port))
    else:
        if protocol == "UDP":
            log.info(f"Starting Modbus UDP server on {listener_address}:{listener_port}")
            StartUdpServer(context, identity=identity, address=(listener_address, listener_port))
        else:
            log.info(f"Starting Modbus TCP server on {listener_address}:{listener_port}")
            StartTcpServer(context, identity=identity, address=(listener_address, listener_port))

def prepare_register(register: dict, init_type: str, initialize_undefined_registers: bool = False) -> dict:
    """
    Prepare the register to have the correct data types
    """
    out_register = dict()

    if not isinstance(register, dict) or len(register) == 0:
        return out_register

    for key in register:
        key_out = int(key, 0) if isinstance(key, str) else key
        val = register[key]
        val_out = val

        if init_type == "word" and isinstance(val, str) and str(val).startswith("0x"):
            val_out = int(val, 16)
        elif init_type == "word" and isinstance(val, int) and 0 <= val <= 65535:
            val_out = val
        elif init_type == "boolean":
            val_out = bool(val) if isinstance(val, int) else val
        else:
            continue
        out_register[key_out] = val_out

    if initialize_undefined_registers:
        for r in range(0, 65536):
            if r not in out_register:
                out_register[r] = 0 if init_type == "word" else False

    return out_register

"""
###############################################################################
# M A I N
###############################################################################
"""
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Modbus TCP Server")
    group = parser.add_argument_group()
    group.add_argument("-f", "--config_file", help=f"Path to the config file (default: {default_config_file})", default=default_config_file)
    args = parser.parse_args()

    config_file = args.config_file if os.path.isfile(args.config_file) else default_config_file
    if not os.path.isfile(config_file):
        print(f"ERROR: configuration file '{config_file}' does not exist.")
        sys.exit(1)

    with open(config_file, encoding="utf-8") as f:
        CONFIG = json.load(f)

    # Initialize logging
    log.setLevel(logging.DEBUG if CONFIG["server"]["logging"]["logLevel"].lower() == "debug" else logging.INFO)
    logging.basicConfig(format=CONFIG["server"]["logging"]["format"])

    # Prepare registers
    configured_discrete_inputs = prepare_register(CONFIG["registers"]["discreteInput"], "boolean", CONFIG["registers"]["initializeUndefinedRegisters"])
    configured_coils = prepare_register(CONFIG["registers"]["coils"], "boolean", CONFIG["registers"]["initializeUndefinedRegisters"])
    configured_holding_registers = prepare_register(CONFIG["registers"]["holdingRegister"], "word", CONFIG["registers"]["initializeUndefinedRegisters"])
    configured_input_registers = prepare_register(CONFIG["registers"]["inputRegister"], "word", CONFIG["registers"]["initializeUndefinedRegisters"])

    # Start Flask server in a separate thread
    flask_thread = threading.Thread(target=app.run, kwargs={"host": "0.0.0.0", "port": 5007})
    flask_thread.daemon = True
    flask_thread.start()

    # Start server
    log.info(f"Starting Modbus Server, v{VERSION}")
    run_server(
        listener_address=CONFIG["server"]["listenerAddress"],
        listener_port=CONFIG["server"]["listenerPort"],
        protocol=CONFIG["server"]["protocol"],
        tls_cert=CONFIG["server"]["tlsParams"]["privateKey"],
        tls_key=CONFIG["server"]["tlsParams"]["certificate"],
        zero_mode=CONFIG["registers"]["zeroMode"],
        discrete_inputs=configured_discrete_inputs,
        coils=configured_coils,
        holding_registers=configured_holding_registers,
        input_registers=configured_input_registers
    )
