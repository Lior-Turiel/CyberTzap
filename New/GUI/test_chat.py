import tkinter as tk
from chat import ChatPage

if __name__ == "__main__":
    def go_back():
        print("Back button pressed (exit chat)")  # Placeholder for "back" action
        root.destroy()

    root = tk.Tk()
    root.geometry("800x600")
    root.title("Chat Test")

    # Initialize the ChatPage with test data
    current_user = "TestUser"
    chat_with_user = "ChatWithMe"
    ChatPage(root, current_user, chat_with_user, go_back)

    root.mainloop()
