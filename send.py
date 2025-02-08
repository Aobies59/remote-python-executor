from sys import argv
import socket

BUFSIZE = 1024

def main(argc, argv):
    if argc != 2:
        print("Usage ./execute.py <path>")
        return

    try:
        with open(argv[1], "r") as file:
            code = file.read()
    except FileNotFoundError:
        print("File not found")
        return

    try:
        connectionSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connectionSocket.connect(("localhost", 12000))
        connectionSocket.send(code.encode())
        response = connectionSocket.recv(BUFSIZE).decode()
        print(response)
    except Exception as e:
        print(e)
        return

if __name__ == "__main__":
    main(len(argv), argv)
