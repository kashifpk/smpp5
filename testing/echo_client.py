#shares the same socket between multiple threads

import socket
import threading

def say_hello(thread_name, sock):
    sock.sendall("hello from " + thread_name)

HOST = '127.0.0.1'          # The remote host
PORT = 50007                # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))     # notice the double brackets

s.sendall('Hello from the main program')

t1 = threading.Thread(target=say_hello, args=('thread 1', s))
t2 = threading.Thread(target=say_hello, args=('thread 2', s))
t3 = threading.Thread(target=say_hello, args=('thread 3', s))  

t1.start()
t2.start()
t3.start()

t1.join()
t2.join()
t3.join()

s.close()
