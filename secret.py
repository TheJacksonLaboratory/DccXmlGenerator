from cryptography.fernet import Fernet
import json
from getpass import getpass
import os


# Generate a key for encryption and decryption
# You must keep this key safe. Anyone with this key can decrypt your data.
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Function to encrypt data
def encrypt_data(data):
    return cipher_suite.encrypt(data.encode())

# Function to decrypt data
def decrypt_data(encrypted_data):
    return cipher_suite.decrypt(encrypted_data).decode()

# Store usernames and passwords
credentials = {
    "user2": encrypt_data("password2")
}

# Save credentials to a file
with open('credentials.json', 'w') as file:
    json.dump({user: cred.decode() for user, cred in credentials.items()}, file)

# Load credentials from a file
with open('credentials.json', 'r') as file:
    loaded_credentials = json.load(file)
    loaded_credentials = {user: decrypt_data(cred.encode()) for user, cred in loaded_credentials.items()}

OMERO_USER="michaelm" 
OMERO_PASSWORD=
OMERO_HOST="ctomero01lp.jax.org"
OMERO_PORT=4064

if __name__ == "__main__":
    print("Enter your username")
    username = input()
    print(username)
    print("Enter your password")    
    password = getpass()
    print(encrypt_data(password))
    print(loaded_credentials)
    print(loaded_credentials[OMERO_USER])
    print(OMERO_PASSWORD)
    print(OMERO_USER)
    print(OMERO_HOST)
    print(OMERO_PORT)
    print(key)