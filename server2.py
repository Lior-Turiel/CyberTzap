import socket
import threading
from encryption_handler import EncryptionHandler


class Server:
    def __init__(self):
        self.HOST = socket.gethostname()
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
            client = Client() # make new client
            self.clients[client.id] = client
            thread = threading.Thread(target=self.handle_client, args=(client_socket, client))
            thread.start()

    def handle_client(self, client_socket, client):
        client_socket.send(client.handler.key)

        while True:
            try:
                message = client_socket.recv(1024)
                if not message:
                    break

                message.decrypt_message()

                self.rout_message(message)

            except:
                # Remove client on disconnect or error
                self.remove_client(client)
                break

    def rout_message(self, message):
        message.decrypt_message()
        message.receivr.send(message)

    def remove_client(self, client):
        if client in self.clients:
            self.clients.pop(client.id)
