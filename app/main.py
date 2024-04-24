import socket

def main():
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    print("Server listening on localhost:4221")

    client_socket, client_address = server_socket.accept() # wait for client
    print(f"Connection from {client_address}")

    # HTTP response with status line and empty headers
    http_response = "HTTP/1.1 200 OK\r\n\r\n"

    # Send the HTTP response
    client_socket.sendall(http_response.encode())

    # Close the connection
    client_socket.close()

if __name__ == "__main__":
    main()
