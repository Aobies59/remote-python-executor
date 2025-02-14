import socket
import signal
import sys

BUFSIZE = 1024
EXECUTION_PORT = 12000
STOP_PORT = 13000

def send_code(ip, file_path):
    try:
        with open(file_path, "r") as file:
            code = file.read()
    except FileNotFoundError:
        print("File not found")
        return

    try:
        connectionSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connectionSocket.connect((ip, EXECUTION_PORT))
        connectionSocket.send(code.encode())
        executionResult = b""
        while True:
            response = connectionSocket.recv(BUFSIZE)
            if not response:
                break
            executionResult += response
            if len(response) < BUFSIZE:
                break
        print(executionResult.decode())
        connectionSocket.close()
    except Exception as e:
        print(e)
        return

def send_stop_signal(ip):
    try:
        stopSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        stopSocket.connect((ip, STOP_PORT))
        stopSocket.send(b"STOP")
        stopSocket.close()
        print("Sent stop signal")
    except Exception as e:
        print("Error sending stop signal:", e)

def signal_handler(sig, frame):
    print("\nCtrl-C detected, sending stop signal...")
    send_stop_signal(sys.argv[1])
    sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: ./execute.py <IP> <path>")
        sys.exit(1)

    signal.signal(signal.SIGINT, signal_handler)
    send_code(sys.argv[1], sys.argv[2])
