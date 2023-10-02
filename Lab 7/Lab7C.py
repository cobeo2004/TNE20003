import socket
import sys
import json


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


# def write_to_file(response: str | dict, file_name: str = "response.json") -> str:
#     try:
#         with open(file_name, "x") as file:
#             json.dump(response, file)
#             return f"File name {file_name} is successfully created and successfully written!"
#     except FileExistsError:
#         return f"File name {file_name} is already exists, thus halted the writing process!"


def main() -> None:
    host: str = sys.argv[1]
    port: int = int(sys.argv[2])
    # file_name: str = sys.argv[3]
    buffer_size = 65535
    response: bytes = f"GET / HTTP/1.1\r\nHost: {host}\r\n\r\n".encode()
    http_response = get_response_from(host, port, buffer_size, response)
    parsed_response = parse_http_header(http_response)
    display_header(parsed_response)
    # print(write_to_file(parsed_response, file_name))


if __name__ == "__main__":
    main()
