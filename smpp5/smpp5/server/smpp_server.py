"""
SMPP Server
"""

import time
import socket
import hashlib
import transaction
import multiprocessing

import db
from db import DBSession
from models import User

from smpp5.lib.session import SMPPSession


def handle_client_connection(conn, addr):
    """
    Handle a client connection
    """

    print("Accepted connection from: " + repr(addr))
    server_session = SMPPSession('server', conn)

    server_session.handle_bind()

    time.sleep(5)
    conn.close()


class SMPPServer(object):
    '''
    Server class is responsible for recieving PDUs from client and decode them and also for sending encoded PDUs response
    '''

    def __init__(self):
        self.socket = None
        self.session = None

    def start_serving(self, host, port):
        print("*** Seving on {host}:{port}".format(host=host, port=port))

        if '0.0.0.0' == host:  # translating all available ips to socket convention
            host = ''

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((host, port))

        try:
            while True:
                self.socket.listen(1)
                conn, addr = self.socket.accept()

                P = multiprocessing.Process(target=handle_client_connection, args=(conn, addr))
                P.start()

                active_conns = multiprocessing.active_children()
                print("Active connections: %i" % len(active_conns))

        except (KeyboardInterrupt, SystemExit):
            print("Good bye!")


if __name__ == '__main__':
    #testing server
    S = SMPPServer()
    S.start_serving('127.0.0.1', 1337)
