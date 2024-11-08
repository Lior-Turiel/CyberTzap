import socket
from encryption_handler import EncryptionHandler

class Client:
    def __init__(self, username, password):
        id_counter = 0
        self.id = id_counter
        id_counter += 1
        self.username = username
        self.password = password
        self.handler = EncryptionHandler()
        self.key = self.handler.key



