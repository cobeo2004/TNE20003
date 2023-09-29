import socket
import sys
import re
import os


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


def parse_http_header(response: str) -> dict:
    headers = {}
    content = ""
    splited_header_lines = response.split('\r\n')
    status = splited_header_lines[0]
    _, status_code, status_message = status.split(' ', 2)

    for header_line in splited_header_lines[1:]:
        if header_line.strip() == "":
            break
        key, value = header_line.split(': ', 1)
        headers[key] = value

    content = '\r\n'.join(
        splited_header_lines[splited_header_lines.index("") + 1:])

    return {
        "status": status_code,
        "message": status_message,
        "headers": headers,
        "content": content
    }


def display_header(parsed_header: dict) -> None:
    status_code = parsed_header["status"]
    message = parsed_header["message"]

    print(f"HTTP Response Code: {status_code}")
    print(f"HTTP Response Message: {message}")

    for value, content in parsed_header["headers"].items():
        print(f"{value}: {content}")
    if status_code != 200:
        print(f"Error: Cannot display content. Status code: {status_code}")
    else:
        print("\nHTML Content:")
        print(parsed_header["content"])


def write_to_file(response: str, file_name: str = "index.json") -> str:

    try:
        with open(file_name, "x") as file:
            file.write(response)
            return f"File name {file_name} is successfully created and successfully written!"
    except FileExistsError:
        return f"File name {file_name} is already exists, thus halted the writing process!"


def extract_image_tags(http_content: str) -> dict:
    return re.findall(r'<img [^>]*src ="([^"]*)"[^>]*>', http_content)


def download_images(socket_host: str, socket_port: int, url: str, base_url: str, save_folder: str = "downloaded_images") -> None:
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    if not url.startswith("http"):
        url = url.join(base_url, url)


def main() -> None:
    host: str = sys.argv[1]
    port: int = 80
    # file_name: str = sys.argv[2]
    buffer_size = 65535
    response: bytes = f"GET / HTTP/1.1\r\nHost: {host}\r\n\r\n".encode()
    http_response = get_response_from(host, port, buffer_size, response)
    parsed_response = parse_http_header(http_response)
    display_header(parsed_response)


if __name__ == "__main__":
    main()
