import socket
import signal
import sys
import threading
import os

def handle_client(client_socket, directory):
    try:
        # Read the HTTP request from the client.
        data = client_socket.recv(1024).decode()
        req = data.split('\r\n')
        path = req[0].split(" ")[1]

        if path == "/":
            response = "HTTP/1.1 200 OK\r\n\r\n".encode()
        elif path.startswith('/echo'):
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(path[6:])}\r\n\r\n{path[6:]}".encode()
        elif path.startswith("/user-agent"):
            user_agent = req[2].split(": ")[1]
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(user_agent)}\r\n\r\n{user_agent}".encode()
        elif path.startswith("/files"):
            filename = path[7:]
            file_path = os.path.join(directory, filename)
            try:
                with open(file_path, "rb") as f:
                    body = f.read()
                response = (
                    f"HTTP/1.1 200 OK\r\n"
                    "Content-Type: application/octet-stream\r\n"
                    f"Content-Length: {len(body)}\r\n\r\n"
                ).encode() + body
            except Exception as e:
                response = "HTTP/1.1 404 Not Found\r\n\r\n".encode()
        else:
            response = "HTTP/1.1 404 Not Found\r\n\r\n".encode()

        client_socket.send(response)
    finally:
        client_socket.close()

def main():
    # Parse command-line arguments to get the directory path
    if len(sys.argv) < 3 or sys.argv[1] != '--directory':
        print("Usage: ./your_server.sh --directory <directory>")
        sys.exit(1)
    directory = sys.argv[2]

    # Print statements for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")
    print(f"Serving files from directory: {directory}")

    # Create a server socket that listens on localhost at port 4221.
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    
    # Define a signal handler to gracefully shut down the server
    def signal_handler(sig, frame):
        print("Shutting down the server...")
        server_socket.close()
        sys.exit(0)

    # Register the signal handler for SIGINT (Ctrl+C)
    signal.signal(signal.SIGINT, signal_handler)

    while True:
        client_socket, client_address = server_socket.accept()
        threading.Thread(target=handle_client, args=(client_socket, directory)).start()

if __name__ == "__main__":
    main()