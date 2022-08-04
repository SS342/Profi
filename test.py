import socket
import time

def TOFILE(content)

def netcat(hostname, port, content):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((hostname, port))
    s.sendall(content)
    s.shutdown(socket.SHUT_WR)
    while 1:
        data = s.recv(1024)
        if len(data) == 0:
            content = "ddd"
            print("TIME SLEEP")
            time.sleep(0.25)
            s.sendall(bytes(content, 'utf-8'))
        print("Received:", eval(repr(data)))



netcat('10.1.0.141', 1686, b'\n')
