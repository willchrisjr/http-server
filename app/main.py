import socket

def main():
    # Print statements for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Create a server socket that listens on localhost at port 4221.
    # The reuse_port=True option allows the socket to be reused immediately after the program exits.
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    
    # Wait for a client to connect.
    # The accept() method blocks and waits for an incoming connection.
    client_socket, client_address = server_socket.accept()
    
    # Print the client address for debugging purposes.
    print(f"Connection from {client_address}")

    # Define the HTTP response to be sent to the client.
    # The response consists of a status line followed by two CRLF sequences.
    http_response = "HTTP/1.1 200 OK\r\n\r\n"

    # Send the HTTP response to the client.
    # The sendall() method ensures that all data is sent.
    client_socket.sendall(http_response.encode('utf-8'))

    # Close the client socket to indicate that the response has been sent.
    client_socket.close()

    # Close the server socket.
    server_socket.close()

if __name__ == "__main__":
    main()