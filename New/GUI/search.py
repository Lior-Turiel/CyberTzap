import tkinter as tk
from tkinter import messagebox

class SearchPage:
    def __init__(self, root, current_user, on_select_user):
        """
        :param root: The parent Tk root.
        :param current_user: The logged-in username.
        :param on_select_user: Callback function after selecting a user to chat with.
        """
        self.root = root
        self.current_user = current_user
        self.on_select_user = on_select_user

        self.frame = tk.Frame(self.root, bg="light green")
        self.frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(
            self.frame, 
            text=f"Welcome, {current_user}! Search for a user to chat with:",
            font=("Arial", 18), 
            bg="light green"
        ).pack(pady=20)

        self.search_entry = tk.Entry(self.frame, font=("Arial", 14))
        self.search_entry.pack(pady=10)

        self.search_button = tk.Button(
            self.frame, 
            text="Search", 
            font=("Arial", 14), 
            bg="blue", 
            fg="white", 
            command=self.search_user
        )
        self.search_button.pack(pady=10)

        self.result_label = tk.Label(self.frame, font=("Arial", 14), bg="light green")
        self.result_label.pack(pady=10)

    def search_user(self):
        username = self.search_entry.get().strip()
        if username and username != self.current_user:
            self.result_label.config(text=f"Found user: {username}")
            tk.Button(
                self.frame, text=f"Chat with {username}", font=("Arial", 14), bg="green", fg="white",
                command=lambda: self.on_select_user(username)
            ).pack(pady=10)
        else:
            messagebox.showerror("Error", "Invalid user or cannot chat with yourself!")
