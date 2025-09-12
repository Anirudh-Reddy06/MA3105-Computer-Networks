import socket
import threading
import random

HOST = "0.0.0.0"          # Listen on all network interfaces
PORT = 5050               
SERVER_NAME = "Server of Anirudh Reddy"

def handle_client(conn, addr):
    print(f"[+] Connected by {addr}")

    try:
        # Receive data
        data = conn.recv(1024).decode()
        if not data:
            return
        
        client_name, client_number = data.split(",")
        client_number = int(client_number)

        # Validate number
        if not (1 <= client_number <= 100):
            print("[!] Invalid number received. Shutting down server.")
            conn.close()
            server_socket.close()
            exit()

        # Pick a server number
        server_number = random.randint(1, 100)

        # Display on server
        print("\n=== Received from Client ===")
        print(f"Client Name: {client_name}")
        print(f"Server Name: {SERVER_NAME}")
        print(f"Client Number: {client_number}")
        print(f"Server Number: {server_number}")
        print(f"Sum: {client_number + server_number}")

        # Send back server info
        response = f"{SERVER_NAME},{server_number}"
        conn.sendall(response.encode())

    finally:
        conn.close()
        print(f"[-] Connection with {addr} closed.")


# Main server setup
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Avoid "port already in use" errors
server_socket.bind((HOST, PORT))
server_socket.listen()

print(f"[*] Server listening on {HOST}:{PORT}...")

while True:
    conn, addr = server_socket.accept()
    # Start a new thread for each client
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()
