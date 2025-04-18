import socket
import threading
from user import User
from message import Message
import utilities
import json
from chat import Chat
import base64


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
                self.user.start_chat(str(other_user_id))

            chat = self.user.chats[str(other_user_id)]
            chat = Chat().from_dict(chat)
            encrypted_text = chat.cipher.encrypt(text.encode())

            message = Message(encrypted_text.decode(), self.user.id, other_user_id)

            chat.add_message(message, self, 'send')

            # Encode encrypted_text with Base64 for safe transmission
            encrypted_text_base64 = base64.b64encode(encrypted_text).decode('utf-8')

            self.server_socket.sendall(f"{self.user.id}:{other_user_id}:{encrypted_text_base64}".encode('utf-8'))
            print(f"Encrypted message sent from {self.user.username} to {addressee['username']}")

    def receive_message(self, other_id):
        """Receives an encrypted message from the server, decrypts, and adds it to chat."""
        self.user.load_chats()
        while self.is_active:
            try:
                data = self.server_socket.recv(1024).decode('utf-8')
                if data:
                    sender_id, encrypted_text_base64 = data.split(':', 1)  # Placeholder format
                    sender_id = int(sender_id)

                    # Decode the Base64-encoded encrypted text
                    encrypted_text = base64.b64decode(encrypted_text_base64)

                    message = Message(encrypted_text.decode(), other_id, self.user.id)

                    chat = Chat().from_dict(self.user.chats[str(sender_id)])
                    chat.add_message(message, self, 'receive')
                    if chat:
                        decrypted_text = chat.decrypt_message(encrypted_text)
                        print(f"Decrypted message from {sender_id}: {decrypted_text}")
                        return decrypted_text
                    else:
                        self.user.start_chat(other_id)
                        chat = Chat().from_dict(self.user.chats[str(sender_id)])
                        decrypted_text = chat.decrypt_message(encrypted_text)
                        print(f"Decrypted message from {sender_id}: {decrypted_text}")
                        return decrypted_text
            except Exception as e:
                print(e)

    def create_new_chat(self, other_id):
        db = utilities.load_data('db/users.json')
        user = db[self.user.username]
        chats = user['chats']
        chats[other_id] = []
        utilities.save_data('db/users.json', db)

    def start_receiving_thread(self, other_id):
        """Starts a separate thread to handle incoming messages."""
        receiving_thread = threading.Thread(target=self.receive_message, daemon=True, args=(other_id,))
        receiving_thread.start()

    def disconnect(self):
        """Cleans up and disconnects the client from the server."""
        self.is_active = False
        self.server_socket.close()
        print(f"{self.user.username} disconnected from the server.")


def send_messages(client: Client, user_id):
    while client.is_active:
        text = input("Send: ")
        client.send_message(text, user_id)
