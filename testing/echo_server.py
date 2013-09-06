import socket

HOST = ''      # Symbolic name meaning all available interfaces
PORT = 50007   # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)    # keep only one connection in waiting queue
conn, addr = s.accept()
print('Connected by' + str(addr))
data = conn.recv(1024)
while data:
    print("[Got message] %s" % data)
    data = conn.recv(1024)

conn.close()
