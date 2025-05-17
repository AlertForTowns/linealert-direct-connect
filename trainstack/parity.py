def calculate_parity(data_list):
    if not data_list:
        return 0
    parity = 0
    for item in data_list:
        parity ^= item
    return parity
