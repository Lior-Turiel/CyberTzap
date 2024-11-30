from tkinter import *
from user import User
from chat_page import ChatPage

def pixels2points(pixels):
    return int(0.75 * pixels)

class LoginPage(Frame):
    def __init__(self, root: Tk, client):
        super().__init__(root, bg="#031E49")
        self.client = client
        self.width = 960
        self.height = 540
        self.pack(fill="both", expand=True)
        self.current_frame = None

        self.client = client

        self.username = StringVar()
        self.password = StringVar()

        Label(self, text="Login", font=("ariel", pixels2points(self.width / 10)), bg="#031E49", fg="white").pack(
            pady=self.height // 20)

        Label(self, text="Username", font=("ariel", pixels2points(self.width / 25)), bg="#031E49", fg="white").pack()
        username_entry = Entry(self, font=("ariel", pixels2points(self.width / 50)), width=self.width // 50,
                               bg="lightgray", textvariable=self.username)
        username_entry.pack(pady=(0, self.height // 10))

        Label(self, text="Password", font=("ariel", pixels2points(self.width / 25)), bg="#031E49", fg="white").pack()
        password_entry = Entry(self, font=("ariel", pixels2points(self.width / 50)), width=self.width // 50,
                               bg="lightgray", show="*", textvariable=self.password)
        password_entry.pack(pady=(0, self.height // 10))

        buttons_frame = Frame(self, bg="#031E49")
        buttons_frame.pack()

        font_size = pixels2points(self.width / 40)
        enter_button = Button(
            buttons_frame, text="ENTER", width=self.width // 100, bg="#1EB500", font=("ariel", font_size),
            fg="white", activebackground="#1EB500", activeforeground="white", bd=0, relief=SUNKEN, command=self.submit
        )
        enter_button.grid(row=0, column=0, padx=self.width // 25)

        back_button = Button(
            buttons_frame, text="EXIT", width=self.width // 100, bg="#DC143C", font=("ariel", font_size),
            fg="white", activebackground="#DC143C", activeforeground="white", bd=0, relief=SUNKEN, command=self.quit
        )
        back_button.grid(row=0, column=1, padx=self.width // 25)

    def submit(self):
        try:
            user = User(self.username.get(), self.password.get())
            if user.auth:
                for widget in self.winfo_children():
                    widget.destroy()
                ChatPage(user, self)
        except:
            self.username.set("")
            self.password.set("")
            Label(self, text="Login Failed", font=("ariel", pixels2points(self.width / 50)), bg="#031E49",
                  fg="red").pack(
                pady=self.height // 20)
