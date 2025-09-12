import socket

HOST, PORT = '', 8080

def create_response(body, cookie=None):
    """Helper function to create an HTTP response string."""
    response = "HTTP/1.1 200 OK\r\n"
    response += "Content-Type: text/html\r\n"
    response += f"Content-Length: {len(body)}\r\n"
    if cookie:
        # Set a cookie in the client's browser [cite: 28]
        response += f"Set-Cookie: session_id={cookie}\r\n"
    response += "\r\n"
    response += body
    return response

def parse_cookies(request_headers):
    """Parses the Cookie header from raw request headers."""
    cookies = {}
    for header in request_headers:
        if header.lower().startswith("cookie:"):
            cookie_data = header.split(':', 1)[1].strip()
            pairs = cookie_data.split(';')
            for pair in pairs:
                if '=' in pair:
                    key, value = pair.split('=', 1)
                    cookies[key.strip()] = value.strip()
    return cookies

def handle_request(client_socket):
    """Handles an incoming client connection."""
    request_data = client_socket.recv(1024).decode('utf-8')
    if not request_data:
        return
    
    headers = request_data.split('\r\n')
    print("--- Received Request ---")
    print(request_data)
    print("------------------------")

    # Check for existing cookies in the request [cite: 32]
    cookies = parse_cookies(headers)
    
    if 'session_id' in cookies:
        # Returning visitor with a cookie [cite: 31]
        user_id = cookies['session_id']
        # Respond with a personalized welcome back message [cite: 34]
        body = f"<h1>Welcome back, {user_id}!</h1><p>Your session is maintained.</p>"
        response = create_response(body)
    else:
        # First-time visitor, no cookie found [cite: 26]
        user_id = "User123"
        # Display a welcome message for the new user [cite: 30]
        body = "<h1>Welcome, new visitor!</h1><p>A cookie has been set for your session.</p>"
        # Assign a simple value to the cookie [cite: 29]
        response = create_response(body, cookie=user_id)
    
    client_socket.sendall(response.encode('utf-8'))
    client_socket.close()

def run_server():
    """Main function to run the socket server."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)
        print(f"Listening on port {PORT}...")
        print(f"Open your browser to http://localhost:{PORT}")
        
        while True:
            client_socket, addr = server_socket.accept()
            print(f"Accepted connection from {addr}")
            handle_request(client_socket)

if __name__ == '__main__':
    run_server()