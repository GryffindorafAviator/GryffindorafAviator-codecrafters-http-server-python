import re
import socket


def main():
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    print("Server listening on localhost:4221")

    client_socket, client_address = server_socket.accept()  # wait for client
    print(f"Connection from {client_address}")

    request_data = client_socket.recv(1024).decode()
    lines = request_data.split('\r\n')
    method, path, http_version = lines[0].split()

    if path == '/':
        http_response = "HTTP/1.1 200 OK\r\n\r\n"
    elif path is not None and path.find("/echo") == 0:
        random_string = extract_random_string(request_data)
        http_response = prepare_response(random_string)
    elif path is not None and path.find("/user-agent") == 0:
        _, user_agent = lines[2].split()
        res_string = user_agent
        http_response = prepare_response(res_string)
    else:
        http_response = "HTTP/1.1 404 Not Found\r\n\r\n"

    client_socket.sendall(http_response.encode())
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
