from cryptography.fernet import Fernet
from message import Message

class Chat:
    def __init__(self):
        self.messages = []
        self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)  # Create a Fernet cipher with the generated key

    @staticmethod
    def new_chat_with_key(key):
        chat = Chat()
        chat.key = key
        chat.cipher = Fernet(chat.key)
        return chat

    def add_message(self, message: Message):
        """Encrypts the message text and stores it in the chat."""
        self.messages.append(message)

    def decrypt_message(self, encrypted_text) -> str:
        """Decrypts a message using the stored Fernet key."""
        decrypted = self.cipher.decrypt(encrypted_text).decode('utf-8')
        print(decrypted)
        return decrypted

    def to_dict(self):
        """Serialize the chat, storing only necessary data (not including the key for security)."""
        return {
            "messages": [msg.to_dict() for msg in self.messages],
            "key": str(self.key)
            # You could consider a method to securely handle keys if needed in saved data
        }

    @staticmethod
    def from_dict(data):
        """Deserialize a chat from saved data, recreating messages (without the Fernet key)."""
        chat = Chat().new_chat_with_key(data['key'])
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
