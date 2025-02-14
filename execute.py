import socket
import io
import sys
import threading
import multiprocessing

BUFSIZE = 1024
EXECUTION_PORT = 12000
STOP_PORT = 13000
stop_flag = threading.Event()

def runCode(code, output_queue):
    buffer = io.StringIO()
    sys.stdout = buffer
    try:
        exec(code)
    except Exception as e:
        print(e)

    output_queue.put(buffer.getvalue())
    sys.stdout = sys.__stdout__

def captureOutput(code):
    global stop_flag
    output_queue = multiprocessing.Queue()
    stop_flag.clear()

    process = multiprocessing.Process(target=runCode, args=(code, output_queue))
    process.start()

    while process.is_alive():
        if stop_flag.is_set():
            print("Stopping execution...")
            process.terminate()
            break

    sys.stdout = sys.__stdout__
    if not output_queue.empty():
        return output_queue.get()
    else:
        return ""

def execution_server():
    executionSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    executionSocket.bind(("0.0.0.0", EXECUTION_PORT))
    executionSocket.listen(5)
    print(f"Execution server listening on port {EXECUTION_PORT}")

    while True:
        connectionSocket, addr = executionSocket.accept()
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
        if stop_flag.is_set():
            print("Code execution cancelled by user")
        else:
            print("Code run succesfully")
            connectionSocket.send(result.encode())
        connectionSocket.close()

def stop_server():
    stopSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    stopSocket.bind(("0.0.0.0", STOP_PORT))
    stopSocket.listen(1)
    print(f"Stop server listening on port {STOP_PORT}")

    while True:
        connectionSocket, addr = stopSocket.accept()
        stop_flag.set()
        connectionSocket.close()

if __name__ == "__main__":
    threading.Thread(target=execution_server, daemon=True).start()
    stop_server()
