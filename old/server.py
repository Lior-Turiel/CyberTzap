import socket
import threading
from cryptography.fernet import Fernet
import hashlib
import base64


def send_key(key, client_socket, username):
    temp = Fernet(username)
    hash_key = str(hashlib.sha256(key))
    encrypted_key = temp.encrypt(hash_key.encode())
    client_socket.send(encrypted_key)


def string_to_url_safe_base64(input_string):
    # Step 1: Hash the string (e.g., SHA-256 will produce 32 bytes)
    hash_bytes = hashlib.sha256(input_string.encode('utf-8')).digest()

    # Step 2: Encode the hash bytes to URL-safe base64
    base64_bytes = base64.urlsafe_b64encode(hash_bytes)

    # Step 3: Strip any trailing '=' padding and return the result
    return base64_bytes.rstrip(b'=').decode('utf-8')


class Server:
    def __init__(self):
        self.HOST = "127.0.0.1"
        self.PORT = 12345
        self.clients = {}

        self.listen()
        self.connect()

    def listen(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.HOST, self.PORT))
        self.server_socket.listen(5)

    def connect(self):
        while True:
            client_socket, client_address = self.server_socket.accept()
            username = client_socket.recv(1024).decode()
            print(username)
            self.clients[username] = client_socket
            thread = threading.Thread(target=self.handle_client, args=(client_socket, username,))
            thread.start()

    def handle_client(self, client_socket, username):
        key = Fernet.generate_key()
        send_key(key, client_socket, username)
        print(key)



Server()
