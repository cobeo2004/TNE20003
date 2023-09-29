import socket
import sys


def get_response_from(host: str, port: int, buffer_size: int, request: bytes) -> str:
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.connect((host, port))
    soc.send(request)
    response: bytes = b""
    while True:
        data = soc.recv(buffer_size)
        if not data:
            break
        response += data

    soc.close()
    return response.decode()


def write_to_file(response: str, file_name: str = "response.txt") -> str:
    try:
        with open(file_name, "x") as file:
            file.write(response)
            return f"File name {file_name} is successfully created and successfully written!"
    except FileExistsError:
        return f"File name {file_name} is already exists, thus halted the writing process!"


def main() -> None:
    host: str = sys.argv[1]
    port: int = 80
    file_name: str = sys.argv[2]
    buffer_size = 1024 * 512
    response: bytes = f"GET / HTTP/1.1\r\nHost: {host}\r\n\r\n".encode()
    html_content = get_response_from(host, port, buffer_size, response)
    print(write_to_file(html_content, file_name))


if __name__ == "__main__":
    main()
