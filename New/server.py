import socket
import threading
import json
from utilities import save_data, load_data
from user import User
from message import Message


class Server:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = {}  # {client_socket: User instance}
        self.lock = threading.Lock()

    def start(self):
        """Starts the server to listen for incoming connections."""
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        print(f"Server started on {self.host}:{self.port}")

        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"Connection from {client_address} has been established.")
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self, client_socket):
        """Manages a single client's connection, authentication, and message handling."""
        try:
            data = client_socket.recv(1024).decode('utf-8')
            user = json.loads(data)
            if user:
                with self.lock:
                    self.clients[client_socket] = user
                print(f"{user['username']} has logged in.")

                # Listen for messages from this client
                while True:
                    data = client_socket.recv(1024).decode('utf-8')
                    if not data:
                        break
                    sender_id, recipient_id, encrypted_text = self.parse_message(data)
                    self.route_message(sender_id, recipient_id, encrypted_text)
        except Exception as e:
            print(f"Error with client: {e}")
        finally:
            self.remove_client(client_socket)

    def route_message(self, sender_id, recipient_id, encrypted_text):
        """Routes an encrypted message from sender to recipient."""
        with self.lock:
            recipient_socket = next(
                (sock for sock, user in self.clients.items() if user['id'] == recipient_id), None
            )

        if recipient_socket:
            # Sending in format: "sender_id:encrypted_text"
            recipient_socket.sendall(f"{sender_id}:{encrypted_text}".encode('utf-8'))
            print(f"Message routed from {sender_id} to {recipient_id}")
        else:
            print(f"User {recipient_id} not connected. Message could not be delivered.")

    def parse_message(self, data):
        """Parses incoming data and extracts sender, recipient, and encrypted text."""
        # Expected data format: "sender_id:recipient_id:encrypted_text"
        parts = data.split(":", 2)
        sender_id = int(parts[0])
        recipient_id = int(parts[1])
        encrypted_text = parts[2]
        return sender_id, recipient_id, encrypted_text

    def remove_client(self, client_socket):
        """Removes a disconnected client and closes their socket."""
        with self.lock:
            user = self.clients.pop(client_socket, None)
            if user:
                print(f"{user['username']} has disconnected.")
        client_socket.close()

    def stop(self):
        """Stops the server and closes all client connections."""
        for client_socket in list(self.clients.keys()):
            client_socket.close()
        self.server_socket.close()
        print("Server stopped.")


# To run the server
if __name__ == "__main__":
    server = Server()
    server.start()
