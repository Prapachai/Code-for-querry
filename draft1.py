import math
import random
import json

file_path = r'/Users/kullawatsatukulsan/Downloads/Code-for-querry-main/informationofclient.json'

# Open the file for reading
try:
    with open(file_path, 'r') as file:
        json_data = json.load(file)  # Load the content of the JSON file into a Python object
    print("File loaded successfully!")
    # Optionally print out the contents to verify the data
except FileNotFoundError:
    print("Error: File not found. Check the file path.")
except json.JSONDecodeError:
    print("Error: File is not a valid JSON.")
except Exception as e:
    print(f"An error occurred: {e}")

def is_prime(x):
    """ Check if a number is prime. """
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

def generate_prime(min_value):
    """ Generate a random prime number greater than a given minimum value. """
    prime = min_value
    while not is_prime(prime):
        prime = random.randint(min_value, 2 * min_value)
    return prime

p = generate_prime(1000000)
q = generate_prime(1000000)

n = p * q
phi = (p - 1) * (q - 1)
lmbda = phi  # λ should be lcm(p-1, q-1); use phi for simplicity here
g = n + 1  # g is typically set to n + 1
mu = pow(lmbda, -1, n)  # μ is calculated based on the L function, simplified here

def encrypt_value(value, n, g):
    """ Encrypt a value using the Paillier encryption scheme. """
    r = random.randint(1, n - 1)  # Choose a random r
    c = (pow(g, value, n**2) * pow(r, n, n**2)) % n**2
    return c

def loop_encrypt_json(json_obj, n, g):
    """ Recursively encrypt values in a JSON object. """
    if isinstance(json_obj, dict):
        for key, value in json_obj.items():
            if isinstance(value, (int, float)):  # Encrypt only numeric values
                json_obj[key] = encrypt_value(value, n, g)
    elif isinstance(json_obj, list):
        for index, item in enumerate(json_obj):
            loop_encrypt_json(item, n, g)
    return json_obj

# Encrypt the JSON data using the public key components n and g
encrypted_json = loop_encrypt_json(json_data, n, g)
print("Encrypted JSON:", encrypted_json)

def decrypt_value(c, n, lmbda, mu):
    x = pow(c, lmbda, n**2)
    l_of_x = (x - 1) // n
    m = (l_of_x * mu) % n
    return m

def loop_decrypt_json(encrypted_json, n, lmbda, mu):
    """ Recursively decrypt values in an encrypted JSON object. """
    if isinstance(encrypted_json, dict):
        for key, value in encrypted_json.items():
            if isinstance(value, int):  # Assuming all integers are encrypted
                encrypted_json[key] = decrypt_value(value, n, lmbda, mu)
    elif isinstance(encrypted_json, list):
        for item in encrypted_json:
            loop_decrypt_json(item, n, lmbda, mu)
    return encrypted_json

decrypted_json = loop_decrypt_json(encrypted_json, n, lmbda, mu)
print("Decrypted JSON:", decrypted_json)
