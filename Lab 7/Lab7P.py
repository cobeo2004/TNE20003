# Import neccessary libraries
import socket
import sys


def get_response_from(host: str, port: int, buffer_size: int, request: bytes) -> str:
    """- Function to get HTTP response from the server

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


def main() -> None:
    host: str = sys.argv[1]  # Get host's addr from the first argument
    port: int = int(sys.argv[2])  # Get host's port from the second argument
    buffer_size = 1024 * 8  # Buffer size
    # Bytes-encoded HTTP GET request
    response: bytes = f"GET / HTTP/1.0\r\nHost: {host}\r\n\r\n".encode()
    # Print the result
    print(get_response_from(host, port, buffer_size, response))


if __name__ == "__main__":
    main()
