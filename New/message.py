class Message:
    def __init__(self, text: str, sender, addressee):
        self.text = text
        self.sender = sender
        self.addressee = addressee

    def to_dict(self):
        return {
            "text": self.text,
            "sender": self.sender,
            "addressee": self.addressee
        }

    @staticmethod
    def from_dict(data):
        return Message(data.text, data.sender, data.addressee)
