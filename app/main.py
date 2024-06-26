import os
import re
import socket
import sys
import threading


def main():
    print("Logs from your program will appear here!")
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    print("Server listening on localhost:4221")
    while True:
        client_socket, client_address = server_socket.accept()  # wait for client
        print(f"Connection from {client_address}")
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()


def handle_client(client_socket):
    try:
        request_data = client_socket.recv(1024).decode()
        request_header, request_body = request_data.split('\r\n\r\n', 1)
        lines = request_header.split('\r\n')
        method, path, http_version = lines[0].split()
        if path == '/':
            http_response = "HTTP/1.1 200 OK\r\n\r\n"
        elif path.startswith("/echo"):
            random_string = extract_random_string(request_data)
            http_response = prepare_response(random_string)
        elif path.startswith("/user-agent"):
            _, user_agent = lines[2].split()
            res_string = user_agent
            http_response = prepare_response(res_string)
        elif path.startswith("/files"):
            file_path = path.lstrip('/files/')
            os.chdir(sys.argv[2])
            if method == "GET":
                contents = ""
                files = os.listdir()
                if file_path in files:
                    with open(file_path, 'r') as f:
                        contents = f.read()
                if contents:
                    http_response = f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length:{len(contents)}\r\n\n{contents}\r\n\r\n"
                else:
                    http_response = "HTTP/1.1 404 NOT FOUND\r\n\r\n"
            else:
                with open(file_path, 'w') as f:
                    f.write(request_body)
                    http_response = "HTTP/1.1 201 Created\r\n\r\n"
        else:
            http_response = "HTTP/1.1 404 Not Found\r\n\r\n"
        client_socket.sendall(http_response.encode())
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        client_socket.close()


def extract_random_string(request_data):
    random_string = re.match(r"GET /echo/(\w+) HTTP/1\.1", request_data)
    if random_string is not None:
        return random_string.group(1)
    else:
        return None


def prepare_response(res_string):
    response_body = res_string
    content_type = "Content-Type: text/plain\r\n"
    content_length = f"Content-Length: {len(response_body)}\r\n"
    http_response = f"HTTP/1.1 200 OK\r\n{content_type}{content_length}\r\n{response_body}"
    return http_response


if __name__ == "__main__":
    main()
