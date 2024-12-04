from tkinter import *
from user import User
import socket
from client import Client
import json
import threading
import utilities
from message import Message
from chat import Chat

def pixels2points(pixels):
    return int(0.75 * pixels)

class ChatPage(Frame):
    def __init__(self, user: User, root):
        super().__init__(root, bg="#031E49")

        self.other_id = None
        self.chat_history = None
        self.entry_canvas = None
        self.message_entry = None
        self.send_button = None
        self.send_button_canvas = None

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
        self.other_id = int(self.other_id_var.get())

        db = utilities.load_data('db/users.json')

        this_user = db[self.user.username]
        chats = this_user['chats']

        keys = chats.keys()
        if str(self.other_id) not in keys:
            chats[str(self.other_id)] = []
            utilities.save_data('db/users.json', db)

        for widget in self.winfo_children():
            widget.destroy()
        threading.Thread(target=self.send_messages, args=(self.other_id,)).start()
        threading.Thread(target=self.recive_msg).start()

    def send_messages(self, other_id):
        users = utilities.load_data('db/users.json')
        other_user = self.user.get_user_by_id(users, other_id)

        Label(self, text=f'chat with {other_user["username"]}', bg="#031E49", fg="white",
              font=("Arial", pixels2points(self.width / 50))).pack()

        self.chat_history = Text(
            self,
            state="disabled",
            wrap="word",
            font=("Arial", 14),
            bg="#6bf98d",
            height=18,
            bd=0,
            highlightthickness=0
        )
        self.chat_history.pack(pady=10, padx=20, fill=X)

        self.entry_canvas = Canvas(self, height=50, bg="green", highlightthickness=0)
        self.entry_canvas.pack(pady=(10, 0), padx=20, fill=X)

        self.message_entry = Entry(
            self.entry_canvas,
            font=("Arial", 16),
            bg="light blue",
            bd=0,
            highlightthickness=0
        )
        self.message_entry.place(x=15, y=10, width=560, height=30)

        self.send_button = Button(
            self.entry_canvas,
            text="Send",
            font=("Arial", 14),
            bg="blue",
            fg="white",
            bd=0,
            highlightthickness=0,
            command=self.send_message
        )
        self.send_button.place(x=600, y=10, width=180, height=30)

        self.load_chat(str(other_id))

    def load_chat(self, other_id: str):
        db = utilities.load_data('db/users.json')
        chat = db[self.client.user.username]['chats'][other_id]
        for message in chat:
            encrypted_text, sender, adressee = list(message.values())
            decrypted_text = Chat().decrypt_message(encrypted_text)
            user = self.user.get_user_by_id(utilities.load_data('db/users.json'), sender)
            text = user['username'] + ': ' + decrypted_text
            self.add_message(text)

    def send_message(self):
        """Send the typed message."""
        text = self.message_entry.get().strip()
        if text:
            self.add_message(f"{self.user.username}: {text}")
            self.message_entry.delete(0, END)
            self.client.send_message(text, self.other_id)

    def add_message(self, message):
        """Add a new message to the chat history."""
        self.chat_history.config(state="normal")
        self.chat_history.insert("end", f"{message}\n")
        self.chat_history.config(state="disabled")
        self.chat_history.see("end")

    def recive_msg(self):
        while self.client.is_active:
            user = self.user.get_user_by_id(utilities.load_data('db/users.json'), self.other_id)
            text = user['username'] + ': ' + self.client.receive_message(self.other_id)
            self.add_message(text)
