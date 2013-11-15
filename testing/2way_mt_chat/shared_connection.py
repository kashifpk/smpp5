import threading
import socket


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
        data = bytes(data.encode('utf-8'))
        self._socket_lock.acquire()
        self.socket.sendall(data)
        self._socket_lock.release()

    def recv(self, bufsize=4098):
        "blocking recv"

        self._socket_lock.acquire()
        data = self.socket.recv(bufsize)
        self._socket_lock.release()

        return data.decode('utf-8')

    def recv_nonblocking(self, bufsize=4098):
        "non-blocking recv"
        data = b''
        try:
            self._socket_lock.acquire()
            data = self.socket.recv(bufsize, socket.MSG_DONTWAIT)
            self._socket_lock.release()
        except Exception:
            self._socket_lock.release()

        return data.decode('utf-8')
