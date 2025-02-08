import socket
import io
import sys

BUFSIZE = 1024

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
    receptionSocket.bind(("0.0.0.0", 12000))
    receptionSocket.listen(5)
    print("Server is listening on port 12000")

    while True:
        connectionSocket, addr = receptionSocket.accept()
        print(f"Connection from {addr}")
        code = b""
        while True:
            codePart = connectionSocket.recv(BUFSIZE)
            if not codePart:
               break
            code += codePart
            if len(code) < BUFSIZE:
                break
        print("Received code")

        result = captureOutput(code.decode())
        connectionSocket.send(result.encode())
        connectionSocket.close()

if __name__ == "__main__":
    main()
