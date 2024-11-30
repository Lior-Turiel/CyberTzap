from tkinter import *
from user import User
import socket
from client import Client
import json
import threading

class ChatPage:
    def __init__(self, user: User):
        self.user = user
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client = Client(self.user, self.server_socket)
        self.client.connect_to_server()

        data = self.client.user.create_data_dict()

        json_object = json.dumps(data, indent=4)

        self.client.server_socket.send(json_object.encode('utf-8'))

        other_id = 2

        threading.Thread(target=self.send_messages, args=(other_id,)).start()
        self.client.start_receiving_thread(other_id)

    def send_messages(self, id):
        while self.client.is_active:
            text = input("Send: ")
            self.client.send_message(text, id)
