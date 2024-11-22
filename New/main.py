import socket
import threading
from user import User
from message import Message
import utilities
from cryptography.fernet import Fernet
import json


class Client:
    def __init__(self, user: User, server_socket):
        self.user = user
        self.server_socket = server_socket
        self.is_active = True

    def connect_to_server(self):
        """Establishes connection to the server."""
        try:
            self.server_socket.connect(('localhost', 12345))
            print(f"{self.user.username} connected to the server.")
        except Exception as e:
            print(f"Connection error: {e}")

    def send_message(self, text, other_user_id):
        """Encrypts and sends a message to another user via the server."""
        users = utilities.load_data('db/users.json')
        addressee = self.user.get_user_by_id(users, other_user_id)

        if addressee:
            if other_user_id not in self.user.chats:
                self.user.start_chat(other_user_id)

            chat = self.user.chats[other_user_id]
            encrypted_text = chat.cipher.encrypt(text.encode())
            self.server_socket.sendall(f"{self.user.id}:{other_user_id}:{encrypted_text}".encode('utf-8'))
            print(f"Encrypted message sent from {self.user.username} to {addressee['username']}")

    def receive_message(self):
        """Receives an encrypted message from the server, decrypts, and adds it to chat."""
        while self.is_active:
            try:
                data = self.server_socket.recv(1024).decode('utf-8')
                if data:
                    sender_id, encrypted_text = data.split(':', 1)  # Placeholder format
                    sender_id = int(sender_id)
                    chat = self.user.chats.get(sender_id)

                    if True:
                        decrypted_text = chat.decrypt_message(encrypted_text.encode())
                        print(decrypted_text)
                        self.user.receive_message(decrypted_text, sender_id)
                    else:
                        print("Chat not found for the sender.")
            except Exception as e:
                print(f"Error receiving message: {e}")
                break

    def start_receiving_thread(self):
        """Starts a separate thread to handle incoming messages."""
        receiving_thread = threading.Thread(target=self.receive_message, daemon=True)
        receiving_thread.start()

    def disconnect(self):
        """Cleans up and disconnects the client from the server."""
        self.is_active = False
        self.server_socket.close()
        print(f"{self.user.username} disconnected from the server.")


def send_messages(client: Client):
    while client.is_active:
        text = input("Send: ")
        client.send_message("text", 1)


def client_main():
    user = User('yoav2', '123')
    if user.auth:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client = Client(user, server_socket)
        client.connect_to_server()

        data = client.user.create_data_dict()

        json_object = json.dumps(data, indent=4)

        client.server_socket.send(json_object.encode('utf-8'))

        threading.Thread(target=send_messages, args=(client,)).start()
        client.start_receiving_thread()


if __name__ == '__main__':
    client_main()
