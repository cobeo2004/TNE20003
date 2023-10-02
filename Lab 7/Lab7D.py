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
    """- Function to Parse the HTTP Header to a dictionary
    Args:
        + Response (str): Response from the server
    Return:
        * dict: Response on the server but on a dictionary
    """
    headers = {}  # Header values
    content = ""  # Content value
    # Split the \r\n on the response and append each header line to the array
    splited_header_lines = response.split('\r\n')
    status = splited_header_lines[0]
    status_type, status_code, status_message = status.split(
        ' ', 2)  # Split the type, code, message of the header

    for header_line in splited_header_lines[1:]:
        # Run a loop to append the header to the dictionary until there is a empty string '' on the array then break
        if header_line.strip() == "":
            break
        key, value = header_line.split(': ', 1)
        headers[key] = value

    content = '\r\n'.join(
        splited_header_lines[splited_header_lines.index("") + 1:])  # Join the HTTP Content with \r\n

    return {
        "type": status_type,
        "status": status_code,
        "message": status_message,
        "headers": headers,
        "content": content
    }  # Return as a dictionary


def display_header(parsed_header: dict) -> None:
    """- Function to display the parsed HTTP Header
    Args:
        + parsed_header (dict): Parsed header from the parse_http_header
    Return:
        * None: Nothing to return
    """
    # Take the type, status, message of the parsed header
    status_type = parsed_header["type"]
    status_code = int(parsed_header["status"])
    message = parsed_header["message"]
    # Display the taken datas
    print(f"HTTP Response Type: {status_type}")
    print(f"HTTP Response Code: {status_code}")
    print(f"HTTP Response Message: {message}")
    # Display the header's data
    print(f"HTTP Headers:")
    for value, content in parsed_header["headers"].items():
        print(f"{value}: {content}")

    # If status code is 200 then display the code
    if status_code == 200:
        print("\nHTTP Content:")
        print(parsed_header["content"])
    # Else display the error!
    else:
        print(f"Can not display content: {status_code}")


# def write_to_file(response: str, file_name: str = "index.json") -> None:
#     try:
#         with open(file_name, "x") as file:
#             json.dump(response, file)
#             print(
#                 f"File name {file_name} is successfully created and successfully written!")
#     except FileExistsError:
#         print(
#             f"File name {file_name} is already exists, thus halted the writing process!")


def extract_image_tag(http_content: str) -> dict:
    return re.findall(r'<img[^>]+src="([^">]+)"', http_content)


def download_image(img_url: str, host: str, buffer_size: int = 1024) -> None:
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if img_url.startswith("http"):
        match = re.match(r'http://([^/]+)(/.*)', img_url)
        if not match:
            print(f"Skipping invalid URL: {img_url}")
        host, path = match.groups()

    if img_url.startswith("https"):
        match = re.match(r'https://([^/]+)(/.*)', img_url)
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
    argument_parser.add_argument("--host", help="The host of the server")
    argument_parser.add_argument(
        "--port", help="The port of the server, default is 80", default=80)
    # argument_parser.add_argument(
    #     "--file_name", help="The json file name for the response, default is index.json", default="index.json")
    arguments = argument_parser.parse_args()
    buffer_size = 65535
    http_response = get_response_from(
        arguments.host, int(arguments.port), buffer_size)
    parsed_response = parse_http_header(http_response)
    display_header(parsed_response)
    # write_to_file(parsed_response, arguments.file_name)
    extracted_image = extract_image_tag(parsed_response["content"])
    for image in extracted_image:
        download_image(image, arguments.host, buffer_size)


if __name__ == "__main__":
    main()
