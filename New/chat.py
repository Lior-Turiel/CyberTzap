from cryptography.fernet import Fernet
from message import Message
import utilities

class Chat:
    def __init__(self):
        self.messages = []
        self.key = b'-YqZx5qUt95Z8SJ0isavH_-lE9b6lwTmu_rKEJagiiY='
        self.cipher = Fernet(self.key)  # Create a Fernet cipher with the key

    def add_message(self, message: Message, client, types):
        """store the message in the database"""
        self.messages.append(message)

        db = utilities.load_data('db/users.json')
        if types == 'send':
            db[client.user.username]['chats'][str(message.addressee)].append(message.to_dict())
        elif types == 'receive':
            db[client.user.username]['chats'][str(message.sender)].append(message.to_dict())
        utilities.save_data('db/users.json', db)

    def decrypt_message(self, encrypted_text) -> str:
        """Decrypts a message using the Fernet key."""
        decrypted = self.cipher.decrypt(encrypted_text).decode('utf-8')
        return decrypted

    def to_dict(self):
        """Serialize the chat"""
        return {
            "messages": list([msg.to_dict() for msg in self.messages]),
        }

    @staticmethod
    def from_dict(data):
        """Deserialize a chat from saved data"""
        chat = Chat()
        if type(data) is not dict:
            for msg_data in data.messages:
                chat.messages.append(Message.from_dict(msg_data))
        else:
            for msg_data in data['messages']:
                chat.messages.append(Message.from_dict(msg_data))
        return chat
