import socket
import threading
from cryptography.fernet import Fernet

# Generate a key for encryption (this key should be securely stored/shared between server and clients)
key = Fernet.generate_key()
cipher = Fernet(key)

# Server configurations
HOST = '127.0.0.1'
PORT = 12345

# List of all connected clients
clients = []

# Handle client communication
def handle_client(client_socket, client_address):
    print(f"New connection from {client_address}")
    # Send the encryption key to the client (shared secret for this session)
    client_socket.send(key)

    while True:
        try:
            # Receive the encrypted message from the client
            encrypted_msg = client_socket.recv(1024)
            if not encrypted_msg:
                break

            # Decrypt the message
            message = cipher.decrypt(encrypted_msg).decode('utf-8')
            print(f"Received (Decrypted): {message}")

            # Broadcast the message to all clients
            broadcast(message, client_socket)
        except:
            # Remove client on disconnect or error
            remove_client(client_socket)
            break

# Broadcast messages to all clients
def broadcast(message, sending_client):
    for client in clients:
        if client != sending_client:
            encrypted_msg = cipher.encrypt(message.encode('utf-8'))
            try:
                client.send(encrypted_msg)
            except:
                remove_client(client)

# Remove a client from the list
def remove_client(client_socket):
    if client_socket in clients:
        clients.remove(client_socket)

# Main function to run the server
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Server started on {HOST}:{PORT}")

    while True:
        client_socket, client_address = server_socket.accept()
        clients.append(client_socket)
        thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        thread.start()

if __name__ == "__main__":
    start_server()
