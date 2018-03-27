import socket

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.25.74", 4242))
s.send(b"hello")