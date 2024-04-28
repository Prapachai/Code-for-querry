import math
import random

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

def generate_prime(min_value):
    # Generate a random prime number greater than min_value
    prime = min_value
    while not is_prime(prime):
        prime = random.randint(min_value, min_value * 10)  # Adjust range as needed
    return prime

# Generate p and q greater than 1 million
p = generate_prime(1000000)
q = generate_prime(1000000)

assert p != q
assert is_prime(p)
assert is_prime(q)

n = p * q
phi = (p - 1) * (q - 1)

def lx(x):
    y = (x - 1) // n
    assert y - int(y) == 0
    return int(y)

g = 1 + n
lmbda = phi * 1
mu = pow(phi, -1, n)

print(p,q)
print(f"private key lambda = {lmbda}. Use this for decryption.")
print(f"public key: g = {g}, n = {n}, mu = {mu}. Use this for encryption.")

def encrypt(m, r):
    assert math.gcd(r, n) == 1
    c = (pow(g, m, n * n) * pow(r, n, n * n)) % (n * n)
    return c

def decrypt(c):
    L_x = (pow(c, lmbda, n**2) - 1) // n
    m = (L_x * mu) % n
    return m

# Encrypt and decrypt a message
m = 72
r = random.randint(1, n)  # Random r such that 1 <= r < n
c = encrypt(m, r)
decrypted_message = decrypt(c)

print("Plaintext message:", m)
print("Ciphertext:", c)
print("Decrypted message:", decrypted_message)

# Function to encrypt a string message
def encrypt_string(message):
    numerical_values = [ord(char) for char in message]  # Convert characters to ASCII values
    encrypted_values = [encrypt(value, random.randint(1, n)) for value in numerical_values]
    print ("Value ASCII:",numerical_values)
    return encrypted_values

# Function to decrypt a list of encrypted numerical values back to string
def decrypt_string(encrypted_values):
    decrypted_numerical_values = [decrypt(value) for value in encrypted_values]
    decrypted_message = ''.join(chr(value) for value in decrypted_numerical_values)
    return decrypted_message

# Encrypt a string
message = "Hello"

print("Message:", message)
encrypted_message = encrypt_string(message)
print("Encrypted Message:", encrypted_message)

# Decrypt the encrypted string
decrypted_message = decrypt_string(encrypted_message)
print("Decrypted Message:", decrypted_message)
