import socket
import sys
import re
import os
import json
import argparse


def get_response_from(host: str, port: int, buffer_size: int, request: bytes) -> str:
    """
    - Function to get HTTP response from the server

    Args:
        + host (str): Host (Could be IP Address or a WWW Website) of the server
        + port (int): Port of the server, reconmend using 80
        + buffer_size (int): buffer size, recommend using 8192 bytes
        + request (bytes): Request to send to server by bytes

    Return:
        * str: Response from the server
    """
    soc = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM)  # Using TCP IPV4 Connection
    soc.connect((host, port))  # Connect to the server
    soc.send(request)  # Sending request to server in bytes
    response: bytes = b""
    while True:
        data = soc.recv(buffer_size)  # Receive response from server in bytes
        if not data:
            break  # Break if there are no datas left
        response += data  # Appending to the response string

    soc.close()  # Close the socket
    return response.decode()  # Return the decoded response in string


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


def extract_image_tag(http_content: str) -> list:
    """- Function to take the image from the HTTP response's <img> tag
    Args:
        + http_content (str): the content of the HTTP
    Return:
        * list: a list that contains the image path or the image from a website
    """
    return re.findall(r'<img[^>]+src="([^">]+)"', http_content)


def download_image(img_url: str, host: str, buffer_size: int = 1024) -> None:
    """- Function to download images
    Args:
        + img_url (str): the extracted image url
        + host (str): the host of the server that contains the img tag
        + buffer_size (int): buffer size, recommended using 1024 to 8192 bytes
    Return:
        * None: Nothing to return
    """
    soc = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM)  # Connect to socket
    # Check if the url is a http website
    if img_url.startswith("http"):
        match = re.match(r'http://([^/]+)(/.*)', img_url)
        if match:
            host, path = match.groups()  # extract protocol (http | https) and the url
        else:
            # Skipping if there are any invalid urls
            print(f"Skipping invalid URL: {img_url}")

    # Check if the url is a https website
    if img_url.startswith("https"):
        match = re.match(r'https://([^/]+)(/.*)', img_url)
        if match:
            host, path = match.groups()  # extract protocol (http | https) and the url
        else:
            # Skipping if there are any invalid urls
            print(f"Skipping invalid URL: {img_url}")

    else:
        # Check if url is a local-stored image and starts with a /
        if img_url.startswith("/"):
            path = img_url  # set path to the given image url
        # If it starts with ./
        else:
            strip_img_url = img_url.strip(".")  # Strip away the (.)
            path = f"{strip_img_url}"  # Use the stripped url
    # Set the name of the downloaded image into the same name as one in the server / website
    img_name = os.path.basename(path)
    # Request getting image from the web in bytes
    request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n".encode()

    try:
        soc.connect((host, 80))
        soc.send(request)  # Connect to the host and send the GET request
        response = b""
        while True:
            data = soc.recv(buffer_size)
            if not data:
                break
            response += data  # Take the reponse from the server
    except Exception as exception:
        # Except any exceptions / errors
        print(f"Failed to retrieve data {img_url}: {exception}")

    # Split the header and image content (in bytes)
    header, img_data = response.split(b'\r\n\r\n', 1)
    # If the response is 200 OK
    if b"200 OK" in header:
        with open(img_name, 'wb') as img_file:
            img_file.write(img_data)  # Write the image in bytes
        print(f"Image {img_name} downloaded successfully!")
    else:
        # Print error if cannot download or there are no 200 OK in response header
        print(
            f"Failed to download {img_url}: Server responded with {header.split(b' ', 2)[1]}")


def main() -> None:
    argument_parser = argparse.ArgumentParser(
        description="Get Image from HTTP client")  # Argument Parser
    argument_parser.add_argument(
        "--host", help="The host of the server")  # Host argument
    argument_parser.add_argument(
        "--port", help="The port of the server, default is 80", default=80)  # Port argument, default is 80
    arguments = argument_parser.parse_args()  # parse the args
    buffer_size = 65535
    http_response = get_response_from(
        arguments.host, int(arguments.port), buffer_size)  # Get the response header from website
    parsed_response = parse_http_header(http_response)
    display_header(parsed_response)  # Parse and display the response header
    # extract the image from the content of the HTTP header
    extracted_image = extract_image_tag(parsed_response["content"])
    # Loop and download images on from the extracted image
    for image in extracted_image:
        download_image(image, arguments.host, buffer_size)


if __name__ == "__main__":
    main()
