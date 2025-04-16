import json
from jsonschema import validate, ValidationError

def parse_to_txt(response, output_file, phase_name):
    try:
        with open(output_file, "a") as file:
            file.write(str(phase_name))
            file.write(str(response))
            file.write(str("/n"))
        print(f"response has been written to {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

def convert_json_to_string(json_data):
    data = json.loads(json_data)
    output = ""
    for message in data["messages"]:
        output += f"{message['author']}|{message['timestamp']['date']}:{message['timestamp']['time']}|{message['text']}|{message['label']} \n"
    return output

def get_last_lines(filepath, num_lines=20):
    with open(filepath, 'rb') as f:
        f.seek(0, 2)  # Move to the end of the file
        filesize = f.tell()
        offset = -500  # Start reading from the last 100 bytes
        buffer = []
        
        while True:
            if filesize + offset > 0:
                f.seek(offset, 2)
                lines = f.readlines()
                buffer = lines + buffer
                if len(buffer) >= num_lines:
                    return "\n".join([line.decode().strip() for line in buffer[-num_lines:]])
            else:
                f.seek(0)
                buffer = f.readlines()
                return "\n".join([line.decode().strip() for line in buffer[-num_lines:]])
            
            offset *= 2  # Increase offset if needed

def parse_json(output):
    """Try to parse JSON. Return None if invalid."""
    try:
        json.loads(output)  # Convert string to dict
        return True
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")  # Log error
        return False

def validate_json(output, schema):    
    try:
        validate(instance=output, schema=schema)
        return True  # Valid JSON
    except ValidationError as e:
        print(f"Validation Error: {e.message}")
        return False  # Invalid JSON