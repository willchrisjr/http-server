import socket
import signal
import sys
import re
import os
import argparse

def main():
    # Parse command-line arguments to get the directory path
    parser = argparse.ArgumentParser(description='Simple HTTP Server')
    parser.add_argument('--directory', required=True, help='Directory to serve files from')
    args = parser.parse_args()
    directory = args.directory

    # Print statements for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")
    print(f"Serving files from directory: {directory}")

    # Create a server socket that listens on localhost at port 4221.
    # The reuse_port=True option allows the socket to be reused immediately after the program exits.
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    
    # Define a signal handler to gracefully shut down the server
    def signal_handler(sig, frame):
        print("Shutting down the server...")
        server_socket.close()
        sys.exit(0)

    # Register the signal handler for SIGINT (Ctrl+C)
    signal.signal(signal.SIGINT, signal_handler)

    while True:
        # Wait for a client to connect.
        # The accept() method blocks and waits for an incoming connection.
        client_socket, client_address = server_socket.accept()
        
        # Print the client address for debugging purposes.
        print(f"Connection from {client_address}")

        # Read the HTTP request from the client.
        request = client_socket.recv(1024).decode('utf-8')
        print(f"Received request:\n{request}")

        # Extract the request line (the first line of the request).
        request_line = request.split('\r\n')[0]
        print(f"Request line: {request_line}")

        # Extract the URL path from the request line.
        method, path, http_version = request_line.split()
        print(f"Method: {method}, Path: {path}, HTTP Version: {http_version}")

        # Initialize the User-Agent header value
        user_agent = None

        # Extract headers from the request
        headers = request.split('\r\n\r\n')[0].split('\r\n')[1:]
        for header in headers:
            header_name, header_value = header.split(': ', 1)
            if header_name.lower() == 'user-agent':
                user_agent = header_value
                break

        # Check if the path matches the /files/<filename> pattern.
        match = re.match(r'^/files/(.*)$', path)
        if match:
            # Extract the filename from the path.
            filename = match.group(1)
            file_path = os.path.join(directory, filename)
            if os.path.exists(file_path) and os.path.isfile(file_path):
                # Read the file contents
                with open(file_path, 'rb') as file:
                    file_contents = file.read()
                # Generate the HTTP response with the file contents.
                http_response = (
                    "HTTP/1.1 200 OK\r\n"
                    "Content-Type: application/octet-stream\r\n"
                    f"Content-Length: {len(file_contents)}\r\n"
                    "\r\n"
                ).encode('utf-8') + file_contents
            else:
                # File not found, respond with 404 Not Found.
                http_response = "HTTP/1.1 404 Not Found\r\n\r\n".encode('utf-8')
        elif path == "/user-agent" and user_agent is not None:
            # Handle the /user-agent endpoint.
            http_response = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/plain\r\n"
                f"Content-Length: {len(user_agent)}\r\n"
                "\r\n"
                f"{user_agent}"
            ).encode('utf-8')
        elif path == "/":
            # Handle the root path with a 200 OK response.
            http_response = "HTTP/1.1 200 OK\r\n\r\n".encode('utf-8')
        elif re.match(r'^/echo/(.*)$', path):
            # Handle the /echo/{str} endpoint.
            echo_str = re.match(r'^/echo/(.*)$', path).group(1)
            http_response = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/plain\r\n"
                f"Content-Length: {len(echo_str)}\r\n"
                "\r\n"
                f"{echo_str}"
            ).encode('utf-8')
        else:
            # Handle any other path with a 404 Not Found response.
            http_response = "HTTP/1.1 404 Not Found\r\n\r\n".encode('utf-8')

        # Send the HTTP response to the client.
        client_socket.sendall(http_response)

        # Close the client socket to indicate that the response has been sent.
        client_socket.close()

if __name__ == "__main__":
    main()