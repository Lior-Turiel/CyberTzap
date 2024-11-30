import tkinter as tk
from login import LoginPage
from search import SearchPage
from chat import ChatPage

class MainApp:
    def __init__(self, root):
        self.root = root
        self.current_user = None
        self.selected_chat_user = None

        # Start with the login pag
        self.show_login_page()

    def show_login_page(self):
        """Show the login page."""
        self.clear_frame()
        LoginPage(self.root, self.on_login)

    def on_login(self, username):
        """Callback after successful login."""
        self.current_user = username
        self.show_search_page()

    def show_search_page(self):
        """Show the search page."""
        self.clear_frame()
        SearchPage(self.root, self.current_user, self.on_select_user)

    def on_select_user(self, chat_user):
        """Callback after selecting a user to chat with."""
        self.selected_chat_user = chat_user
        self.show_chat_page()

    def show_chat_page(self):
        """Show the chat page."""
        self.clear_frame()
        ChatPage(self.root, self.current_user, self.selected_chat_user, self.show_search_page)

    def clear_frame(self):
        """Clear all widgets from the root frame."""
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    app = MainApp(root)
    root.mainloop()
