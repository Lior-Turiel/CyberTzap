import socket
import threading
from cryptography.fernet import Fernet

# Server details
HOST = '127.0.0.1'
PORT = 12345

# Create the socket for the client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# Receive the encryption key from the server
key = client_socket.recv(1024)
cipher = Fernet(key)


# Function to send encrypted messages to the server
def send_message():
    while True:
        message = input("You: ")
        encrypted_msg = cipher.encrypt(message.encode('utf-8'))
        client_socket.send(encrypted_msg)


# Function to receive encrypted messages from the server
def receive_message():
    while True:
        encrypted_msg = client_socket.recv(1024)
        if encrypted_msg:
            decrypted_msg = cipher.decrypt(encrypted_msg).decode('utf-8')
            print(f"Server: {decrypted_msg}")


# Start message sending and receiving in separate threads
def start_client():
    # Start a thread for sending messages
    send_thread = threading.Thread(target=send_message)
    send_thread.start()

    # Start a thread for receiving messages
    receive_thread = threading.Thread(target=receive_message)
    receive_thread.start()


if __name__ == "__main__":
    start_client()
