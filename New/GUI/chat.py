import tkinter as tk

class ChatPage:
    def __init__(self, root, current_user, chat_with_user, on_back):
        self.root = root
        self.current_user = current_user
        self.chat_with_user = chat_with_user
        self.on_back = on_back

        self.frame = tk.Frame(self.root, bg="green")
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Chat title
        tk.Label(
            self.frame,
            text=f"Chat with {chat_with_user}",
            font=("Arial", 18),
            bg="green"
        ).pack(pady=10)

        # Chat history
        self.chat_history = tk.Text(
            self.frame,
            state="disabled",
            wrap="word",
            font=("Arial", 14),
            bg="#6bf98d",
            height=10,
            bd=0,
            highlightthickness=0
        )
        self.chat_history.pack(pady=10, padx=20, fill=tk.X)

        # Rounded message entry
        self.entry_canvas = tk.Canvas(self.frame, height=50, bg="green", highlightthickness=0)
        self.entry_canvas.pack(pady=(10, 0), padx=20, fill=tk.X)
        self._create_rounded_rectangle(self.entry_canvas, 10, 10, 590, 40, 25, fill="light blue")

        self.message_entry = tk.Entry(
            self.entry_canvas,
            font=("Arial", 16),
            bg="light blue",
            bd=0,
            highlightthickness=0
        )
        self.message_entry.place(x=15, y=10, width=560, height=30)

        # Rounded Send button
        self.send_button_canvas = tk.Canvas(self.frame, height=50, bg="green", highlightthickness=0)
        self.send_button_canvas.pack(pady=(10, 0), padx=20, fill=tk.X)
        self._create_rounded_rectangle(self.send_button_canvas, 10, 10, 200, 40, 25, fill="blue")

        self.send_button = tk.Button(
            self.send_button_canvas,
            text="Send",
            font=("Arial", 14),
            bg="blue",
            fg="white",
            bd=0,
            highlightthickness=0,
            command=self.send_message
        )
        self.send_button.place(x=10, y=10, width=180, height=30)

        # Rounded Back button
        self.back_button_canvas = tk.Canvas(self.frame, height=50, bg="green", highlightthickness=0)
        self.back_button_canvas.pack(pady=(10, 5), padx=20, fill=tk.X)
        self._create_rounded_rectangle(self.back_button_canvas, 10, 10, 300, 40, 25, fill="red")

        self.back_button = tk.Button(
            self.back_button_canvas,
            text="Chat with someone else",
            font=("Arial", 14),
            bg="red",
            fg="white",
            bd=0,
            highlightthickness=0,
            command=self.on_back
        )
        # Center the button inside the rounded rectangle
        self.back_button.place(x=10, y=10, width=280, height=30)

        # Bind the Enter key to send messages
        self.root.bind("<Return>", lambda event: self.send_message())

    def send_message(self):
        """Send the typed message."""
        message = self.message_entry.get().strip()
        if message:
            self.add_message(f"{self.current_user}: {message}")
            self.message_entry.delete(0, tk.END)

    def add_message(self, message):
        """Add a new message to the chat history."""
        self.chat_history.config(state="normal")
        self.chat_history.insert("end", f"{message}\n")
        self.chat_history.config(state="disabled")
        self.chat_history.see("end")

    def _create_rounded_rectangle(self, canvas, x1, y1, x2, y2, radius, **kwargs):
        """Draw a rounded rectangle on the canvas."""
        points = [
            x1 + radius, y1, x1 + radius, y1,
            x2 - radius, y1, x2 - radius, y1,
            x2, y1, x2, y1 + radius, x2, y1 + radius,
            x2, y2 - radius, x2, y2 - radius, x2, y2,
            x2 - radius, y2, x2 - radius, y2, x1 + radius, y2,
            x1 + radius, y2, x1, y2, x1, y2 - radius,
            x1, y2 - radius, x1, y1 + radius, x1, y1 + radius, x1, y1
        ]
        return canvas.create_polygon(points, smooth=True, **kwargs)
