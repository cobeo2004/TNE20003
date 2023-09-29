import socket
import sys
import re
import os
import json
import argparse


def get_response_from(host: str, port: int, buffer_size: int) -> str:
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    request = f"GET / HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n".encode()
    try:
        soc.connect((host, port))
        soc.send(request)
        response = b""
        while True:
            data = soc.recv(buffer_size)
            if not data:
                break
            response += data
    except Exception as exception:
        print(f"Failed to retreive {host}: {exception}")

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
    status_code = int(parsed_header["status"])
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


def write_to_file(response: str, file_name: str = "index.json") -> None:
    try:
        with open(file_name, "x") as file:
            json.dump(response, file)
            print(
                f"File name {file_name} is successfully created and successfully written!")
    except FileExistsError:
        print(
            f"File name {file_name} is already exists, thus halted the writing process!")


def extract_image_tag(http_content: str) -> dict:
    return re.findall(r'<img[^>]+src="([^">]+)"', http_content)


def download_image(img_url: str, host: str, buffer_size: int = 1024) -> None:
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if img_url.startswith("http"):
        match = re.match(r'http://([^/]+)(/.*)', img_url)
        if not match:
            print(f"Skipping invalid URL: {img_url}")
        host, path = match.groups()
    else:
        if img_url.startswith("/"):
            path = img_url
        else:
            path = f"/{img_url}"
    img_name = os.path.basename(path)
    request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n".encode()

    try:
        soc.connect((host, 80))
        soc.send(request)
        response = b""
        while True:
            data = soc.recv(buffer_size)
            if not data:
                break
            response += data
    except Exception as exception:
        print(f"Failed to retrieve data {img_url}: {exception}")

    header, img_data = response.split(b'\r\n\r\n', 1)
    if b"200 OK" in header:
        with open(img_name, 'wb') as img_file:
            img_file.write(img_data)
        print(f"Image {img_name} downloaded successfully!")
    else:
        print(
            f"Failed to download {img_url}: Server responded with {header.split(b' ', 2)[1]}")


def main() -> None:
    argument_parser = argparse.ArgumentParser(
        description="Get Image from HTTP client")
    argument_parser.add_argument("host", help="The host of the server")
    argument_parser.add_argument(
        "port", help="The port of the server, default is 80", default=80)
    argument_parser.add_argument(
        "file_name", help="The json file name for the response, default is index.json", default="index.json")
    arguments = argument_parser.parse_args()
    buffer_size = 65535
    http_response = get_response_from(
        arguments.host, int(arguments.port), buffer_size)
    parsed_response = parse_http_header(http_response)
    display_header(parsed_response)
    write_to_file(parsed_response, arguments.file_name)
    extracted_image = extract_image_tag(parsed_response["content"])
    for image in extracted_image:
        download_image(image, arguments.host, buffer_size)


if __name__ == "__main__":
    main()
