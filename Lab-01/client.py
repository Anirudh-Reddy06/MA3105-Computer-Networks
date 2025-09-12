import socket

CLIENT_NAME = "Client of Anirudh Reddy"
HOST = "127.0.0.1"  # Change to server's IP if running on another machine
PORT = 5050

# Get user input
client_number = int(input("Enter an integer (1-100): "))

# Create socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# Send data
message = f"{CLIENT_NAME},{client_number}"
client_socket.sendall(message.encode())

# Receive response
data = client_socket.recv(1024).decode()
server_name, server_number = data.split(",")
server_number = int(server_number)

# Display result
print("\n=== Communication Result ===")
print(f"Client Name: {CLIENT_NAME}")
print(f"Server Name: {server_name}")
print(f"Client Number: {client_number}")
print(f"Server Number: {server_number}")
print(f"Sum: {client_number + server_number}")

# Close socket
client_socket.close()
