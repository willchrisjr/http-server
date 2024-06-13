# HTTP Server Implementation

This project is a simple HTTP server implemented in Python using the asyncio library. The server can handle basic HTTP requests, including serving files, echoing messages, and responding with user-agent information. It also supports gzip compression for echo responses.

## Table of Contents

1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Step 1: Basic TCP Server](#step-1-basic-tcp-server)
4. [Step 2: Basic HTTP Response](#step-2-basic-http-response)
5. [Step 3: URL Path Handling](#step-3-url-path-handling)
6. [Step 4: Echo Endpoint](#step-4-echo-endpoint)
7. [Step 5: User-Agent Endpoint](#step-5-user-agent-endpoint)
8. [Step 6: Concurrent Connections](#step-6-concurrent-connections)
9. [Step 7: Serving Files](#step-7-serving-files)
10. [Step 8: POST Method for Files](#step-8-post-method-for-files)
11. [Step 9: HTTP Compression](#step-9-http-compression)
12. [Step 10: Multiple Compression Schemes](#step-10-multiple-compression-schemes)
13. [Step 11: Gzip Compression](#step-11-gzip-compression)
14. [Code Explanation](#code-explanation)

## Introduction

HTTP is the protocol that powers the web. In this challenge, you'll build an HTTP server that's capable of handling simple GET/POST requests, serving files, and handling multiple concurrent connections.

## Getting Started

To run the server, execute the following command:

```sh
$ ./your_server.sh --directory /path/to/your/directory
```

This will start the server and set the directory for file operations.

## Step 1: Basic TCP Server

In this step, you'll create a TCP server that listens on port 4221.

### Requirements

- Your server must listen on port 4221.
- The server must accept TCP connections.

### Testing

The tester will execute your program like this:

```sh
$ ./your_server.sh
```

Then, the tester will try to connect to your server on port 4221. The connection must succeed for you to pass this step.

## Step 2: Basic HTTP Response

In this step, your server will respond to an HTTP request with a 200 response.

### HTTP Response

An HTTP response is made up of three parts, each separated by a CRLF (`\r\n`):

1. Status line.
2. Zero or more headers, each ending with a CRLF.
3. Optional response body.

### Example Response

```http
HTTP/1.1 200 OK\r\n\r\n
```

### Testing

The tester will execute your program like this:

```sh
$ ./your_server.sh
```

The tester will then send an HTTP GET request to your server:

```sh
$ curl -v http://localhost:4221
```

Your server must respond with:

```http
HTTP/1.1 200 OK\r\n\r\n
```

## Step 3: URL Path Handling

In this step, your server will extract the URL path from an HTTP request and respond with either a 200 or 404, depending on the path.

### Example Requests and Responses

1. For a random path:

    ```sh
    $ curl -v http://localhost:4221/abcdefg
    ```

    Response:

    ```http
    HTTP/1.1 404 Not Found\r\n\r\n
    ```

2. For the root path:

    ```sh
    $ curl -v http://localhost:4221
    ```

    Response:

    ```http
    HTTP/1.1 200 OK\r\n\r\n
    ```

## Step 4: Echo Endpoint

In this step, you'll implement the `/echo/{str}` endpoint, which accepts a string and returns it in the response body.

### Example Request and Response

Request:

```http
GET /echo/abc HTTP/1.1\r\nHost: localhost:4221\r\nUser-Agent: curl/7.64.1\r\nAccept: /\r\n\r\n
```

Response:

```http
HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 3\r\n\r\nabc
```

## Step 5: User-Agent Endpoint

In this step, you'll implement the `/user-agent` endpoint, which reads the `User-Agent` request header and returns it in the response body.

### Example Request and Response

Request:

```http
GET /user-agent HTTP/1.1\r\nHost: localhost:4221\r\nUser-Agent: foobar/1.2.3\r\nAccept: /\r\n\r\n
```

Response:

```http
HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 12\r\n\r\nfoobar/1.2.3
```

## Step 6: Concurrent Connections

In this step, you'll add support for concurrent connections.

### Testing

The tester will execute your program like this:

```sh
$ ./your_server.sh
```

Then, the tester will create multiple concurrent TCP connections to your server and send a single GET request through each connection.

```sh
$ (sleep 3 && printf "GET / HTTP/1.1\r\n\r\n") | nc localhost 4221 &
$ (sleep 3 && printf "GET / HTTP/1.1\r\n\r\n") | nc localhost 4221 &
$ (sleep 3 && printf "GET / HTTP/1.1\r\n\r\n") | nc localhost 4221 &
```

Your server must respond to each request with:

```http
HTTP/1.1 200 OK\r\n\r\n
```

## Step 7: Serving Files

In this step, you'll implement the `/files/{filename}` endpoint, which returns a requested file to the client.

### Testing

The tester will execute your program with a `--directory` flag:

```sh
$ ./your_server.sh --directory /tmp/
```

1. For an existing file:

    ```sh
    $ echo -n 'Hello, World!' > /tmp/foo
    $ curl -i http://localhost:4221/files/foo
    ```

    Response:

    ```http
    HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: 14\r\n\r\nHello, World!
    ```

2. For a non-existent file:

    ```sh
    $ curl -i http://localhost:4221/files/non_existant_file
    ```

    Response:

    ```http
    HTTP/1.1 404 Not Found\r\n\r\n
    ```

## Step 8: POST Method for Files

In this step, you'll add support for the POST method of the `/files/{filename}` endpoint, which accepts text from the client and creates a new file with that text.

### Example Request and Response

Request:

```http
POST /files/number HTTP/1.1\r\nHost: localhost:4221\r\nUser-Agent: curl/7.64.1\r\nAccept: /\r\nContent-Type: application/octet-stream\r\nContent-Length: 5\r\n\r\n12345
```

Response:

```http
HTTP/1.1 201 Created\r\n\r\n
```

### Testing

The tester will execute your program with a `--directory` flag:

```sh
$ ./your_server.sh --directory /tmp/
```

Then, the tester will send a POST request to the `/files/{filename}` endpoint:

```sh
$ curl -v --data "12345" -H "Content-Type: application/octet-stream" http://localhost:4221/files/file_123
```

Your server must create a new file in the specified directory with the contents of the request body.

## Step 9: HTTP Compression

In this step, you'll add support for the `Content-Encoding` header based on what the client sends.

### Example Requests and Responses

1. For a valid encoding:

    Request:

    ```http
    GET /echo/foo HTTP/1.1\r\nHost: localhost:4221\r\nUser-Agent: curl/7.64.1\r\nAccept-Encoding: gzip\r\n\r\n
    ```

    Response:

    ```http
    HTTP/1.1 200 OK\r\nContent-Encoding: gzip\r\nContent-Type: text/plain\r\nContent-Length: 3\r\n\r\nfoo
    ```

2. For an invalid encoding:

    Request:

    ```http
    GET /echo/bar HTTP/1.1\r\nHost: localhost:4221\r\nUser-Agent: curl/7.64.1\r\nAccept-Encoding: invalid-encoding\r\n\r\n
    ```

    Response:

    ```http
    HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 3\r\n\r\nbar
    ```

## Step 10: Multiple Compression Schemes

In this step, you'll add support for choosing a compression scheme when multiple values are passed in via the `Accept-Encoding` header.

### Example Requests and Responses

1. For multiple encodings including gzip:

    Request:

    ```http
    GET /echo/foo HTTP/1.1\r\nHost: localhost:4221\r\nUser-Agent: curl/7.64.1\r\nAccept-Encoding: encoding-1, gzip, encoding-2\r\n\r\n
    ```

    Response:

    ```http
    HTTP/1.1 200 OK\r\nContent-Encoding: gzip\r\nContent-Type: text/plain\r\nContent-Length: 3\r\n\r\nfoo
    ```

2. For multiple invalid encodings:

    Request:

    ```http
    GET /echo/bar HTTP/1.1\r\nHost: localhost:4221\r\nUser-Agent: curl/7.64.1\r\nAccept-Encoding: encoding-1, encoding-2\r\n\r\n
    ```

    Response:

    ```http
    HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 3\r\n\r\nbar
    ```

## Step 11: Gzip Compression

In this step, you'll add support for returning responses compressed using gzip.

### Example Request and Response

Request:

```http
GET /echo/foo HTTP/1.1\r\nHost: localhost:4221\r\nUser-Agent: curl/7.64.1\r\nAccept-Encoding: gzip\r\n\r\n
```

Response:

```http
HTTP/1.1 200 OK\r\nContent-Encoding: gzip\r\nContent-Type: text/plain\r\nContent-Length: 23\r\n\r\ngzip-encoded-data
```

The response body should be the random string sent in the request, gzip encoded. The `Content-Length` header should be the length of the gzip encoded data.

## Code Explanation

parse_request(content: bytes) -> tuple
Parses the HTTP request content and returns the method, path, headers, and body.

make_response(status: int, headers: dict, body: bytes) -> bytes
Creates an HTTP response with the given status, headers, and body.

gzip_compress(data: str) -> bytes
Compresses the given string data using gzip and returns the compressed bytes.

handle_connection(reader: StreamReader, writer: StreamWriter) -> None
Handles incoming connections, parses the request, and sends the appropriate response based on the request path and method.

main()
The main entry point of the server. It parses command-line arguments, sets up the server, and starts serving requests.

### Explanation

- **`parse_request`**: Parses the HTTP request and extracts the method, path, headers, and body.
- **`make_response`**: Constructs an HTTP response with the given status, headers, and body.
- **`gzip_compress`**: Compresses the given data using gzip.
- **`handle_connection`**: Handles incoming connections, processes the request, and sends the appropriate response.
- **`main`**: Sets up the server and starts listening for connections.

