"""
2-Way chat client
Uses two threads sharing the same socket

thread 1 listens for incoming messages and displays them
thread 2 is used to send messages (by displaying prompts on the screen)
"""

import socket
import threading

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
            print("[Msg from server] " + msg)
            if 'quit' == msg.strip().lower():
                connection.close()

        time.sleep(1)


def handle_server_connection(conn):
    """
    Handle a client connection to the server
    """
    print("connected to server")

    sc = SharedConnection(conn)
    sc.is_open = True

    # create a background thread here for receiving messages and show message sending ui in current thread
    background_thread = threading.Thread(target=handle_incoming_data, args=(sc, ))
    background_thread.start()

    # do gui related work here
    while sc.is_open:
        msg = input("send to server> ")
        sc.send(msg)

        if 'quit' == msg.strip().lower():
            sc.close()

    background_thread.join()

if '__main__' == __name__:

    HOST = '127.0.0.1'
    PORT = 50008

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))     # notice the double brackets

    try:
        handle_server_connection(s)

    except (KeyboardInterrupt, SystemExit):
        print("Good bye!")

    s.close()
