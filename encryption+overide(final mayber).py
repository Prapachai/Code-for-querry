import math
import random
import json

file_path = r'/Users/kullawatsatukulsan/Downloads/Code-for-querry-main/informationofclient.json'

# Function to check if a number is prime
def is_prime(x):
    if x <= 1:
        return False
    if x <= 3:
        return True
    if x % 2 == 0 or x % 3 == 0:
        return False
    i = 5
    while i * i <= x:
        if x % i == 0 or x % (i + 2) == 0:
            return False
        i += 6
    return True

# Function to generate a prime number greater than a given minimum value
def generate_prime(min_value):
    prime = min_value
    while not is_prime(prime):
        prime = random.randint(min_value, 2 * min_value)
    return prime

p = generate_prime(1000000)
q = generate_prime(1000000)
n = p * q
phi = (p - 1) * (q - 1)
lmbda = phi  # Using phi as a simplification for lcm(p-1, q-1)
g = n + 1  # Typically g is set to n + 1
mu = pow(lmbda, -1, n)  # Inverse of lambda modulo n

# Load JSON data from file
try:
    with open(file_path, 'r') as file:
        json_data = json.load(file)
    print("File loaded successfully!")
except FileNotFoundError:
    print("Error: File not found. Check the file path.")
    exit()
except json.JSONDecodeError:
    print("Error: File is not a valid JSON.")
    exit()
except Exception as e:
    print(f"An error occurred: {e}")
    exit()

# Function to encrypt a numerical value
def encrypt_value(value, n, g):
    r = random.randint(1, n - 1)
    c = (pow(g, value, n**2) * pow(r, n, n**2)) % n**2
    return c

# Function to encrypt a string by converting each character to its ASCII value and encrypting it
def encrypt_string(s, n, g):
    return [encrypt_value(ord(char), n, g) for char in s]

# Function to recursively encrypt values in a JSON object
def loop_encrypt_json(json_obj, n, g):
    if isinstance(json_obj, dict):
        for key, value in json_obj.items():
            if isinstance(value, str) and key in ("Name", "Surname"):
                json_obj[key] = encrypt_string(value, n, g)
            elif isinstance(value, (int, float)):
                json_obj[key] = encrypt_value(value, n, g)
    elif isinstance(json_obj, list):
        for index, item in enumerate(json_obj):
            loop_encrypt_json(item, n, g)
    return json_obj

encrypted_json = loop_encrypt_json(json_data, n, g)

# Function to save the encrypted data back to the file
def save_encrypted_data(encrypted_json, file_path):
    try:
        with open(file_path, 'w') as file:
            json.dump(encrypted_json, file, indent=4)
        print("Encrypted data has been saved successfully.")
    except Exception as e:
        print(f"An error occurred while saving the encrypted data: {e}")

save_encrypted_data(encrypted_json, file_path)

# Optional: Functions to decrypt the data (for demonstration purposes)
def decrypt_value(c, n, lmbda, mu):
    x = pow(c, lmbda, n**2)
    l_of_x = (x - 1) // n
    m = (l_of_x * mu) % n
    return m

def decrypt_string(encrypted_chars, n, lmbda, mu):
    return ''.join(chr(decrypt_value(char, n, lmbda, mu)) for char in encrypted_chars)

def loop_decrypt_json(encrypted_json, n, lmbda, mu):
    if isinstance(encrypted_json, dict):
        for key, value in encrypted_json.items():
            if isinstance(value, list) and all(isinstance(x, int) for x in value):
                encrypted_json[key] = decrypt_string(value, n, lmbda, mu)
            elif isinstance(value, int):
                encrypted_json[key] = decrypt_value(value, n, lmbda, mu)
    elif isinstance(encrypted_json, list):
        for item in encrypted_json:
            loop_decrypt_json(item, n, lmbda, mu)
    return encrypted_json

decrypted_json = loop_decrypt_json(encrypted_json, n, lmbda, mu)
print("Decrypted JSON:", decrypted_json)
