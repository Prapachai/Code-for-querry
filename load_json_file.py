import json

def load_json_from_file(filename):
    with open(filename, 'r') as file:
        return json.load(file)

json_data = load_json_from_file('test.json')
