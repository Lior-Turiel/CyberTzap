from cryptography.fernet import Fernet
from encryption_handler import EncryptionHandler


class Message:
    def __init__(self, sender: client, receiver: client, original_text):
        self.sender = sender
        self.receiver = receiver
        self.original_text = original_text
        self.encrypted_text = None

    def encrypt_message(self):
        self.encrypted_text = sender.handler.encrypt(self.original_text)
        self.original_text = None

    def decrypt_message(self):
        self.original_text = self.receiver.handler.decrypt(self.encrypted_text)
