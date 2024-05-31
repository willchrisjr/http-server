import socket
import threading
import sys
import os

def handle_req(client, addr, directory):
    try:
        data = client.recv(1024).decode()
        req = data.split('\r\n')
        request_line = req[0].split(" ")
        method = request_line[0]
        path = request_line[1]

        if method == "GET":
            if path == "/":
                response = "HTTP/1.1 200 OK\r\n\r\n".encode()
            elif path.startswith('/echo'):
                response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(path[6:])}\r\n\r\n{path[6:]}".encode()
            elif path.startswith("/user-agent"):
                user_agent = None
                for header in req:
                    if header.lower().startswith("user-agent:"):
                        user_agent = header.split(": ")[1]
                        break
                if user_agent:
                    response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(user_agent)}\r\n\r\n{user_agent}".encode()
                else:
                    response = "HTTP/1.1 400 Bad Request\r\n\r\n".encode()
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
        elif method == "POST":
            if path.startswith("/files"):
                filename = path[7:]
                file_path = os.path.join(directory, filename)
                # Extract the body of the POST request
                body = data.split('\r\n\r\n')[1]
                try:
                    with open(file_path, "wb") as f:
                        f.write(body.encode())
                    response = "HTTP/1.1 201 Created\r\n\r\n".encode()
                except Exception as e:
                    response = "HTTP/1.1 500 Internal Server Error\r\n\r\n".encode()
            else:
                response = "HTTP/1.1 404 Not Found\r\n\r\n".encode()
        else:
            response = "HTTP/1.1 405 Method Not Allowed\r\n\r\n".encode()

        client.send(response)
    finally:
        client.close()

def main():
    if len(sys.argv) < 3 or sys.argv[1] != '--directory':
        print("Usage: ./your_server.sh --directory <directory>")
        sys.exit(1)
    directory = sys.argv[2]

    print("Logs from your program will appear here!")
    print(f"Serving files from directory: {directory}")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    while True:
        client, addr = server_socket.accept()
        threading.Thread(target=handle_req, args=(client, addr, directory)).start()

if __name__ == "__main__":
    main()