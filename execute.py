import socket
import io
import sys

def captureOutput(code):
    buffer = io.StringIO()
    sys.stdout = buffer
    try:
        exec(code)
    except Exception as e:
        return str(e)
    finally:
        sys.stdout = sys.__stdout__
    return buffer.getvalue()

def main():
    receptionSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    receptionSocket.bind(("localhost", 12000))
    receptionSocket.listen(1)
    print("Server is listening on port 12000")

    while True:
        connectionSocket, addr = receptionSocket.accept()
        print(f"Connection from {addr}")
        code = connectionSocket.recv(1024).decode()
        print(f"Received code: {code}")

        result = captureOutput(code)
        connectionSocket.send(result.encode())

        connectionSocket.close()

if __name__ == "__main__":
    main()
