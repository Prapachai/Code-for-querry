from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import json
import base64

def generate_key_pair():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

def encrypt_value(value, public_key):
    key = RSA.import_key(public_key)
    cipher = PKCS1_OAEP.new(key)
    if isinstance(value, str):
        encrypted_value = cipher.encrypt(value.encode())
    elif isinstance(value, int):
        encrypted_value = cipher.encrypt(value.to_bytes((value.bit_length() + 7) // 8, byteorder='big'))
    else:
        raise ValueError("Unsupported data type for encryption")
    return encrypted_value

def loop_encrypt_json(json_obj, public_key):
    if isinstance(json_obj, dict):
        for key, value in json_obj.items():
            if isinstance(value, dict):
                json_obj[key] = loop_encrypt_json(value, public_key)
            elif isinstance(value, (str, int)):
                json_obj[key] = encrypt_value(str(value), public_key) if isinstance(value, int) else encrypt_value(value, public_key)
            # Add conditions for encrypting other data types if needed
    elif isinstance(json_obj, list):
        for index, item in enumerate(json_obj):
            if isinstance(item, dict):
                json_obj[index] = loop_encrypt_json(item, public_key)
            elif isinstance(item, (str, int)):
                json_obj[index] = encrypt_value(str(item), public_key) if isinstance(item, int) else encrypt_value(item, public_key)
            # Add conditions for encrypting other data types if needed
    return json_obj

def encrypt_json(json_data, public_key):
    encrypted_data = loop_encrypt_json(json_data, public_key)
    return encrypted_data

# Example usage:
json_data = {
    "name": "John",
    "age": 30,
    "address": {
    "city": "New York",
    "zip": "10001"
    }
}

private_key, public_key = generate_key_pair()

def binary_to_string(binary_data):
    return base64.b64encode(binary_data).decode()

# Encrypt the JSON data
encrypted_json = encrypt_json(json_data, public_key)

# Convert encrypted binary data to string representation
encrypted_json_str = json.dumps(encrypted_json, default=binary_to_string)
print("Encrypted JSON:", encrypted_json_str)

