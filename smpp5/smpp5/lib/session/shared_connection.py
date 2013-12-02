import threading
import socket
import sys
import datetime
from smpp5.lib.parameter_types import Integer, CString, String, TLV
from smpp5.lib.util.hex_print import hex_convert, hex_print
from smpp5.lib.constants import *
from smpp5.lib.constants import NPI, TON, esm_class, command_ids, command_status, tlv_tag, message_state
from smpp5.lib.constants.command_status import *
from smpp5.lib.pdu import command_mappings
from smpp5.lib.pdu.pdu import PDU


class SharedConnection(object):
    """
    Shared connection class for sharing a socket and its state between multiple threads
    """

    _socket_lock = None
    is_open = False
    state = 0

    def __init__(self, sock):
        self._socket_lock = threading.Lock()
        self.socket = sock

    def close(self):
        self.is_open = False
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()

    def send(self, data):
        self._socket_lock.acquire()
        self.socket.sendall(data)
        print("data sended g from client....")
        self._socket_lock.release()

    def recv(self, bufsize=4098):
        "blocking recv"

        self._socket_lock.acquire()
        data = self.socket.recv(bufsize)
        self._socket_lock.release()

        return data.decode('utf-8')

    def get_pdu_from_socket(self):
        "non-blocking recv"
        """
        Given a socket, returns a completed PDU and blocks until a PDU is received

        For non-blocking sockets see:

        * http://docs.python.org/2/howto/sockets.html#non-blocking-sockets
        * http://stackoverflow.com/questions/2719017/how-to-set-timeout-on-pythons-socket-recv-method
        * http://docs.python.org/2/library/select.html#select.select
        """
        P = None
        try:
            self._socket_lock.acquire()
        #First wait till 4 bytes a read from the socket (command_length)
            d = self.socket.recv(4, socket.MSG_DONTWAIT)
            command_length = Integer.decode(d)  # decode first four bytes to get the command length via it

        # get bytes specified by command_length - 4
            sock_data = self.socket.recv(command_length.value - 4, socket.MSG_DONTWAIT)
            sock_data = d + sock_data

            command_id = Integer.decode(sock_data[4:8])    # decode from 5th byte till 8th to get command_id
            PDUClass = command_mappings[command_id.value]  # get the class name via command_id
            P = PDUClass.decode(sock_data)
            self._socket_lock.release()
        except Exception:
            self._socket_lock.release()

        # decode PDU
        return P

