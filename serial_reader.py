import serial
from decoder_panasonic import decode_panasonic
from trainstack import Train, Cart

# Config
PORT = '/dev/ttyUSB0'
BAUD_RATE = 115200
TIMEOUT = 0.1

# Initialize
ser = serial.Serial(PORT, baudrate=BAUD_RATE, timeout=TIMEOUT)
train = Train(id="train_panasonic_001", role_id="heater_loop")

print(f"Listening on {PORT} at {BAUD_RATE} baud...")

while True:
    raw = ser.read(128)
    if raw:
        snapshot = decode_panasonic(raw)
        cart = Cart.from_snapshot(snapshot)
        train.push(cart)
