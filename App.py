from tkinter import *
import socket
import hashlib
from cryptography.fernet import Fernet
import base64


def string_to_url_safe_base64(input_string):
    # Step 1: Hash the string (e.g., SHA-256 will produce 32 bytes)
    hash_bytes = hashlib.sha256(input_string.encode('utf-8')).digest()

    # Step 2: Encode the hash bytes to URL-safe base64
    base64_bytes = base64.urlsafe_b64encode(hash_bytes)

    # Step 3: Strip any trailing '=' padding and return the result
    return base64_bytes.rstrip(b'=').decode('utf-8')


class App:
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 12345
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))

        self.username = input("enter username: ")
        self.client_socket.send(self.username.encode())

        self.key = self.client_socket.recv(1024)

        temp = Fernet(str(hashlib.sha256(self.username)))
        self.key = temp.decrypt(self.key)
        print(self.key)


App()
