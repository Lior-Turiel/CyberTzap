import hashlib
import os
import json


# Function to load data from a JSON file
def load_data(filepath):
    try:
        with open(filepath, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


# Function to save data to a JSON file
def save_data(filepath, data):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as file:
        json.dump(data, file, indent=4)


# Function to hash a password with bcrypt
def hash_password(password):
    return hashlib.sha3_256(password.encode()).hexdigest()
