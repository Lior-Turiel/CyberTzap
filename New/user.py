import hashlib
from message import Message
from chat import Chat
import utilities

user_counter = 0


class User:
    def __init__(self, username, password):
        global user_counter
        user_counter += 1
        self.username = username
        self.password_hash = hashlib.sha3_256(password.encode()).hexdigest()
        self.id = user_counter
        self.chats = {}  # {other_user_id: Chat instance}

    def create_data_dict(self):
        """Generate a dictionary representation of the user for saving/loading."""
        return {
            "username": self.username,
            "id": self.id,
            "password_hash": self.password_hash,
            "chats": {user_id: chat.to_dict() for user_id, chat in self.chats.items()}
        }

    @staticmethod
    def get_user_by_id(users, user_id):
        """Retrieve a user by ID from a list of users."""
        return next((user for user in users if user.id == user_id), None)

    def start_chat(self, other_user_id):
        """Initiates a new chat with another user, if one doesn’t already exist."""
        if other_user_id not in self.chats:
            self.chats[other_user_id] = Chat()
            self.send_message(f"Chat started by {self.username}.", other_user_id)
            print(f"Chat started with User {other_user_id}")
        else:
            print("Chat already exists with this user.")

    def send_message(self, text, other_user_id):
        """Encrypt and send a message to another user."""
        users = utilities.load_data('db/users.json')
        addressee = self.get_user_by_id(users, other_user_id)

        if addressee:
            if other_user_id not in self.chats:
                self.start_chat(other_user_id)

            chat = self.chats[other_user_id]
            encrypted_text = chat.cipher.encrypt(text.encode())
            message = Message(encrypted_text, self, addressee)
            chat.add_message(message)
            print(f"Encrypted message sent to {addressee.username}")
            # TODO: Send the message via server

    def receive_message(self, encrypted_text, sender_id):
        """Decrypt a received message and store it in the appropriate chat."""
        if sender_id not in self.chats:
            self.chats[sender_id] = Chat()

        chat = self.chats[sender_id]
        decrypted_text = chat.decrypt_message(encrypted_text)
        message = Message(decrypted_text, self.get_user_by_id(sender_id), self)
        chat.add_message(message)
        print(f"Message received from User {sender_id}: {decrypted_text}")

    def load_chats(self):
        """Loads the user's chats from a file, initializing Chat instances."""
        saved_data = utilities.load_data('db/chats.json')
        user_chats = saved_data.get(str(self.id), {})

        for other_user_id, chat_data in user_chats.items():
            chat = Chat.from_dict(chat_data)
            self.chats[int(other_user_id)] = chat
