# clean_json.py
def remove_hidden_characters(input_file, output_file):
    """
    Removes hidden characters (non-printable characters) from the input file,
    except for newline, tab, and space characters.
    
    Args:
    - input_file (str): The path to the JSON file to clean.
    - output_file (str): The path where the cleaned JSON file will be saved.
    """
    try:
        # Open the input file in read mode
        with open(input_file, 'r') as file:
            content = file.read()

        # Remove non-printable characters except space, tab, and newline
        cleaned_content = ''.join(c for c in content if c.isprintable() or c in ['\n', '\t', ' '])

        # Save the cleaned content into the output file
        with open(output_file, 'w') as file:
            file.write(cleaned_content)

        print(f"Cleaned file saved to {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Define the file paths
if __name__ == "__main__":
    input_file = "modbus_server.json"  # Modify with your actual input file name if needed
    output_file = "modbus_server_cleaned.json"  # Output file name after cleaning
    remove_hidden_characters(input_file, output_file)
