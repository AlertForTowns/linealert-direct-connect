import reprlib

# Specify the file path
file_path = '/home/vboxuser/linealert-direct-connect/modbus_server.json'

# Read the file and print hidden characters
with open(file_path, 'r', encoding='utf-8') as file:
    content = file.read()

# Use repr to show all characters including hidden ones
print("Hidden characters and non-printable characters in the file:")
print(reprlib.repr(content))  # This will show characters like '\n', '\t', etc.

# Optionally, you can also check for problematic characters by filtering out printable characters
for char in content:
    if not char.isprintable():
        print(f"Non-printable character found: {repr(char)}")
