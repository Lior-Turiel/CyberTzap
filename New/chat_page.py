from tkinter import *
from user import User
import socket
from client import Client
import json
import threading

def pixels2points(pixels):
    return int(0.75 * pixels)

class ChatPage(Frame):
    def __init__(self, user: User, root):
        super().__init__(root, bg="#031E49")
        self.pack(fill="both", expand=True)
        self.width = 960
        self.height = 540

        self.user = user
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client = Client(self.user, self.server_socket)
        self.client.connect_to_server()

        data = self.client.user.create_data_dict()

        json_object = json.dumps(data, indent=4)

        self.client.server_socket.send(json_object.encode('utf-8'))

        self.other_id_var = StringVar(self)
        self.choose_id()

    def send_messages(self, other_id):
        while self.client.is_active:
            text = input("Send: ")
            self.client.send_message(text, other_id)

    def choose_id(self):
        Label(self, text="Enter Id To Chat With", font=("ariel", pixels2points(self.width / 30)), bg="#031E49", fg="white").pack(pady=self.height // 20)

        id_entry = Entry(self, font=("ariel", pixels2points(self.width / 50)), width=self.width // 50, bg="lightgray", textvariable=self.other_id_var)
        id_entry.pack(pady=(0, self.height // 10))

        font_size = pixels2points(self.width / 40)
        enter_button = Button(
            self, text="ENTER", width=self.width // 100, bg="#1EB500", font=("ariel", font_size),
            fg="white", activebackground="#1EB500", activeforeground="white", bd=0, relief=SUNKEN, command=self.submit
        )
        enter_button.pack()

    def submit(self):
        other_id = int(self.other_id_var.get())
        threading.Thread(target=self.send_messages, args=(other_id,)).start()
        self.client.start_receiving_thread(other_id)
