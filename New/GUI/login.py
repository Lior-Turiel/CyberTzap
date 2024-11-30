import tkinter as tk
from tkinter import messagebox

class LoginPage:
    # Centralized styling variables
    FONT = ("Arial", 15)
    BG_COLOR = "light green"
    FG_COLOR = "black"
    ENTRY_BG_COLOR = "#e0e0e0"
    BUTTON_BG_COLOR = "#4CAF50"
    BUTTON_FG_COLOR = "white"

    def __init__(self, root):
        self.root = root
        self.root.title("Login Page")
        self.root.geometry("400x300")
        self.root.attributes('-fullscreen', True)
        
        # Frame covering the whole screen
        self.frame = tk.Frame(self.root, bg=self.BG_COLOR)
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        # Canvas for graphical elements
        self.canvas = tk.Canvas(self.frame, bg=self.BG_COLOR, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Title
        self.title = tk.Label(
            self.frame, 
            text="Login, if you don't have an account, one will be created with the details you provide", 
            font=self.FONT, bg=self.BG_COLOR, fg=self.FG_COLOR, wraplength=600
        )
        self.title.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        # Username and password backgrounds (rounded rectangles)
        self.create_rounded_rectangle(100, 200, 700, 250, 20, fill=self.ENTRY_BG_COLOR)
        self.create_rounded_rectangle(100, 300, 700, 350, 20, fill=self.ENTRY_BG_COLOR)

        # Username label
        self.username_label = self.create_label("Username:", 120, 170)

        # Username entry
        self.username_entry = self.create_entry(120, 210)

        # Password label
        self.password_label = self.create_label("Password:", 120, 270)

        # Password entry
        self.password_entry = self.create_entry(120, 310, show="*")
        
        # Submit button
        self.login_button = tk.Button(
            self.frame, 
            text="Submit", 
            font=self.FONT, 
            bg=self.BUTTON_BG_COLOR, 
            fg=self.BUTTON_FG_COLOR, 
            relief="flat", 
            borderwidth=0,
            command=self.submit_login
        )
        self.login_button.place(relx=0.5, rely=0.7, anchor=tk.CENTER, width=200, height=50)

        # Bind Enter key to submit the login form
        self.root.bind("<Return>", self.submit_login)

    def create_rounded_rectangle(self, x1, y1, x2, y2, radius=25, **kwargs):
        """Draw a rounded rectangle on the canvas."""
        points = [
            x1+radius, y1, x1+radius, y1,
            x2-radius, y1, x2-radius, y1,
            x2, y1, x2, y1+radius, x2, y1+radius,
            x2, y2-radius, x2, y2-radius, x2, y2,
            x2-radius, y2, x2-radius, y2, x1+radius, y2,
            x1+radius, y2, x1, y2, x1, y2-radius,
            x1, y2-radius, x1, y1+radius, x1, y1+radius, x1, y1
        ]
        return self.canvas.create_polygon(points, smooth=True, **kwargs)

    def create_label(self, text, x, y):
        """Create a label with consistent styling."""
        label = tk.Label(self.frame, text=text, font=self.FONT, bg=self.BG_COLOR, fg=self.FG_COLOR)
        label.place(x=x, y=y)
        return label

    def create_entry(self, x, y, **kwargs):
        """Create an entry with consistent styling."""
        entry = tk.Entry(self.frame, font=self.FONT, bd=0, highlightthickness=0, bg=self.ENTRY_BG_COLOR, insertbackground="black", **kwargs)
        entry.place(x=x, y=y, width=560, height=30)
        return entry

    def submit_login(self, event=None):
        """Method called when the submit button is clicked or Enter is pressed."""
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username and password:
            # You can add the login logic here (e.g., check against a database or list)
            print(f"Logged in with Username: {username}, Password: {password}")
            # Redirect to the next page (e.g., search page or dashboard)
            self.root.destroy()  # Close login page (or you can open a new page)
        else:
            messagebox.showwarning("Input Error", "Please fill in both username and password.")

if __name__ == "__main__":
    root = tk.Tk()
    login_page = LoginPage(root)
    root.mainloop()
