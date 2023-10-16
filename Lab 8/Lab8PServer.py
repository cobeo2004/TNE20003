import socket
import argparse


def udp_server_listener(host: str, port: int, buffer_size: int = 1024) -> None:
    """ Server listener for the UDP connection that send the response to the client via UDP protocol

    Args:
        host (str): Host of the server
        port (int): Port of the server
        buffer_size (int, optional): Buffer size of the server. Defaults to 1024.
    """

    # Using IPV4 and UDP protocol
    server_soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Bind any upcoming connect from the host and port
    server_soc.bind((host, port))

    while True:
        # Receive response from the client
        data, address = server_soc.recvfrom(buffer_size)
        msg = data.decode('ascii')  # Decode the response

        # If message not starts with TNE20003: then send back with error
        if not msg.startswith("TNE20003:"):
            err_msg = "TNE20003:E:Invalid Protocol Header"
            server_soc.sendto(err_msg.encode('ascii'), address)
            continue

        # Extract the payload message from the client
        payload = msg[9:]

        # If the payload is empty then send back with error message that says Empty Message
        if not payload:
            err_msg = "TNE20003:E:Empty Messsage"
            server_soc.sendto(err_msg.encode('ascii'), address)
            continue

        # Send back the acknowledge message to client
        ack_msg = f"TNE20003:A:{payload}"
        server_soc.sendto(ack_msg.encode('ascii'), address)


def main() -> None:
    arg_parser = argparse.ArgumentParser("Server-side UDP for Lab 8P")
    arg_parser.add_argument(
        "-host", help="Host, default is localhost", default="127.0.0.1", type=str)  # Host, default is localhost
    arg_parser.add_argument(
        "-port", help="Port, default is 4231", default=4231, type=int)  # Port, default is 4231
    arg_parser.add_argument(
        "-buffer_size", help="Buffer size of the packet, default is 1024", default=1024, type=int)  # Buffer size, default is 1024
    args = arg_parser.parse_args()  # Parse the args
    # Execute the udp_server_listener() function
    udp_server_listener(args.host, args.port, args.buffer_size)


if __name__ == "__main__":
    main()
