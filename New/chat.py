from cryptography.fernet import Fernet
from message import Message

class Chat:
    def __init__(self):
        self.messages = []
        self.key = Fernet.generate_key()  # Generate a unique Fernet key for this chat
        self.cipher = Fernet(self.key)  # Create a Fernet cipher with the generated key

    def add_message(self, message: Message):
        """Encrypts the message text and stores it in the chat."""
        encrypted_text = self.cipher.encrypt(message.text.encode())
        message.text = encrypted_text  # Store the encrypted text in the Message object
        self.messages.append(message)

    def decrypt_message(self, encrypted_text: bytes) -> str:
        """Decrypts a message using the stored Fernet key."""
        return self.cipher.decrypt(encrypted_text).decode()

    def to_dict(self):
        """Serialize the chat, storing only necessary data (not including the key for security)."""
        return {
            "messages": [msg.to_dict() for msg in self.messages],
            # You could consider a method to securely handle keys if needed in saved data
        }

    @staticmethod
    def from_dict(data):
        """Deserialize a chat from saved data, recreating messages (without the Fernet key)."""
        chat = Chat()
        # TODO: Load key securely or regenerate if needed
        for msg_data in data['messages']:
            chat.messages.append(Message.from_dict(msg_data))
        return chat

    def get_decrypted_messages(self):
        """Return all messages decrypted for viewing."""
        decrypted_messages = []
        for message in self.messages:
            decrypted_text = self.cipher.decrypt(message.text).decode()
            # Create a copy or custom representation of the decrypted message
            decrypted_messages.append((message.sender_id, decrypted_text))
        return decrypted_messages