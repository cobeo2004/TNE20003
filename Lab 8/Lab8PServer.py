import socket
import argparse


def udp_server_listener(host: str, port: int, buffer_size: int = 1024) -> None:
    server_soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_soc.bind((host, port))

    while True:
        data, address = server_soc.recvfrom(buffer_size)
        msg = data.decode('ascii')

        if not msg.startswith("TNE20003:"):
            err_msg = "TNE20003:E:Invalid Protocol Header"
            server_soc.sendto(err_msg.encode('ascii'), address)
            continue

        payload = msg[9:]

        if not payload:
            err_msg = "TNE20003:E:Empty Messsage"
            server_soc.sendto(err_msg.encode('ascii'), address)
            continue

        ack_msg = f"TNE20003:A:{payload}"
        server_soc.sendto(ack_msg.encode('ascii'), address)


def main() -> None:
    arg_parser = argparse.ArgumentParser("Server-side UDP for Lab 8P")
    arg_parser.add_argument(
        "-host", help="Host of the client, default is localhost", default="127.0.0.1", type=str)
    arg_parser.add_argument(
        "-port", help="Port of the client, default is 4231", default=4231, type=int)
    arg_parser.add_argument(
        "-buffer_size", help="Buffer size of the packet, default is 1024", default=1024, type=int)
    args = arg_parser.parse_args()
    udp_server_listener(args.host, args.port, args.buffer_size)


if __name__ == "__main__":
    main()
