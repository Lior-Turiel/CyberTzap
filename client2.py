import hashlib
import json
from encryption_handler import EncryptionHandler

# This will be your global counter for generating unique client IDs
id_counter = 1


class Client:
    def __init__(self, username, password):
        global id_counter
        self.id = id_counter
        id_counter += 1
        self.username = username
        # Hash the password (ensure it's in bytes)
        self.password = hashlib.sha256(password.encode()).hexdigest()
        self.handler = EncryptionHandler()
        self.key = self.handler.key

    def to_dict(self):
        """ Convert the Client object to a dictionary suitable for JSON """
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "key": self.key
        }

    @classmethod
    def from_dict(cls, data):
        """ Create a Client object from a dictionary """
        client = cls(data['username'], data['password'])
        client.id = data['id']
        client.key = data['key']
        return client


def load_clients(filename="database.json"):
    """ Load the list of clients from the JSON file """
    try:
        with open(filename, "r") as f:
            data = json.load(f)
            return [Client.from_dict(client_data) for client_data in data]
    except (FileNotFoundError, json.JSONDecodeError):
        return []  # Return an empty list if no file or invalid JSON


def save_clients(clients, filename="clients_db.json"):
    """ Save the list of clients to the JSON file """
    with open(filename, "w") as f:
        json.dump([client.to_dict() for client in clients], f, indent=4)


def add_or_update_client(new_client, filename="clients_db.json"):
    """ Add or update a client in the JSON database """
    clients = load_clients(filename)

    # Check if client already exists based on username
    existing_client = next((client for client in clients if client.username == new_client.username), None)

    if existing_client:

        existing_client.key = new_client.key
    else:
        # Add new client
        clients.append(new_client)

    save_clients(clients, filename)
