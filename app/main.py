import socket


def main():
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    print("Server listening on localhost:4221")

    client_socket, client_address = server_socket.accept()  # wait for client
    print(f"Connection from {client_address}")

    request_data = client_socket.recv(1024).decode()
    path = extract_path(request_data)

    if path == '/':
        http_response = "HTTP/1.1 200 OK\r\n\r\n"
    else:
        http_response = "HTTP/1.1 404 Not Found\r\n\r\n"

    client_socket.sendall(http_response.encode())
    client_socket.close()


def extract_path(request_data):
    lines = request_data.split('\r\n')
    start_line = lines[0]
    method, path, http_version = start_line.split()
    return path


if __name__ == "__main__":
    main()
