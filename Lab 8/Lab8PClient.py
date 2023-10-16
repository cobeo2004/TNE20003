import socket
import argparse


def udp_client_listener(host: str, port: int, buffer_size: int = 1024) -> None:
    """ Client listener for the UDP connection that send the message to the server via UDP protocol

    Args:
        host (str): Host of the server
        port (int): Port of the server
        buffer_size (int, optional): Buffer size of the server. Defaults to 1024.
    """
    client_soc = socket.socket(
        socket.AF_INET, socket.SOCK_DGRAM)  # Using the IPV4 and UDP diagram
    while True:
        # Enter the message to send to the server
        msg = input("Enter message to send to server (or 'exit' to end): ")

        if msg.lower() == 'exit':
            break  # If it is exit then break

        # Send the message to the server in (host, port) with ascii encoded
        client_soc.sendto(msg.encode('ascii'), (host, port))

        # Receive the server's data and server address
        data, address = client_soc.recvfrom(buffer_size)
        # Print the response
        print(f"Received from server {address}: {data.decode('ascii')}")
    # Close the socket if not in use
    client_soc.close()


def main() -> None:
    # Argument parser
    arg_parser = argparse.ArgumentParser("Client-side UDP for Lab 8P")
    arg_parser.add_argument(
        "-host", help="Host of the server, default is localhost", default="127.0.0.1", type=str)  # Host of the server, default is localhost
    arg_parser.add_argument(
        "-port", help="Port of the server, default is 4231", default=4231, type=int)  # Port of the server, default is 4231
    arg_parser.add_argument(
        "-buffer_size", help="Buffer size of the packet, default is 1024", default=1024, type=int)  # Buffer size, default is 1024
    args = arg_parser.parse_args()  # Parsing argument
    # Execute the udp_client_listener function
    udp_client_listener(args.host, args.port, args.buffer_size)


if __name__ == "__main__":
    main()
