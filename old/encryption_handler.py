from cryptography.fernet import Fernet


class EncryptionHandler:
    def __init__(self):
        self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)

    def encrypt(self, text):
        return self.cipher.encrypt(text.encode('utf-8'))

    def decrypt(self, encrypted_text):
        return self.cipher.decrypt(encrypted_text).decode('utf-8')
