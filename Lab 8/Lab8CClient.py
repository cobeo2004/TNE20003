import socket
import argparse


def tcp_client_listener(host: str, port: int, buffer_size: int = 1024) -> None:
    client_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_soc.connect((host, port))
    while True:
        msg = input("Enter message to send to server (or 'exit' to end): ")

        if msg.lower() == 'exit':
            break

        client_soc.sendall(msg.encode('ascii'))

        data = client_soc.recv(buffer_size)
        print(f"Received from server : {data.decode('ascii')}")
    client_soc.close()


def main() -> None:
    arg_parser = argparse.ArgumentParser("Client-side UDP for Lab 8P")
    arg_parser.add_argument(
        "-host", help="Host of the server, default is localhost", default="127.0.0.1", type=str)
    arg_parser.add_argument(
        "-port", help="Port of the server, default is 4231", default=4231, type=int)
    arg_parser.add_argument(
        "-buffer_size", help="Buffer size of the packet, default is 1024", default=1024, type=int)
    args = arg_parser.parse_args()
    tcp_client_listener(args.host, args.port, args.buffer_size)


if __name__ == "__main__":
    main()
