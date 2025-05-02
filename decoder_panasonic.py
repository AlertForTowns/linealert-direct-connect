def decode_panasonic(raw_bytes):
    # Example decoder logic: assumes known offsets
    def to_float10(b):
        return int.from_bytes(b, 'little') / 10

    def to_float100(b):
        return int.from_bytes(b, 'little') / 100

    def from_bitmask(byte_val, bit):
        return bool(byte_val & (1 << bit))

    return {
        "sensor_temp": to_float10(raw_bytes[12:14]),
        "flow_rate": to_float100(raw_bytes[20:22]),
        "valve_open": from_bitmask(raw_bytes[30], 3)
    }

