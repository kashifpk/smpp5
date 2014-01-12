 
"""
2-Way chat server
Uses two threads sharing the same socket

thread 1 listens for incoming messages and displays them
thread 2 is used to send messages (by displaying prompts on the screen)
"""

import socket
import multiprocessing
import threading
import time
from shared_connection import SharedConnection


def handle_incoming_data(connection):

    while connection.is_open:
        msg = connection.recv_nonblocking()
        if msg:
            print("[Msg from client] " + msg)
            if 'quit' == msg.strip().lower():
                connection.close()

        time.sleep(1)


def handle_client_connection(conn, addr):
    """
    Handle a client connection
    """
    print("Accepted connection from: " + repr(addr))

    sc = SharedConnection(conn)
    sc.is_open = True

    # create a background thread here for receiving messages and show message sending ui in current thread
    background_thread = threading.Thread(target=handle_incoming_data, args=(sc, ))
    background_thread.start()

    # do gui related work here
    time.sleep(1)
    while sc.is_open:
        msg = input("send to client> ")
        sc.send(msg)

        if 'quit' == msg.strip().lower():
            sc.close()

    background_thread.join()

if '__main__' == __name__:

    HOST = ''      # Symbolic name meaning all available interfaces
    PORT = 50008   # Arbitrary non-privileged port
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))

    try:
        while True:
            s.listen(1)  # listening for connections
            print("listening......")
            conn, addr = s.accept()  # accept connections and return ip and port

            handle_client_connection(conn, addr)

    except (KeyboardInterrupt, SystemExit):
        print("Good bye!")

    s.close()
