import socket
from threading import Thread

from rpc.serializer import deserialize


class NodeListenerThread(Thread):
    def __init__(self, n):
        self.node_reference = n
        super().__init__(target=self.task)

    def task(self):
        sock = socket.socket()
        sock.bind(("", self.node_reference.port))
        sock.listen(20)
        while True:
            conn, addr = sock.accept()

            length = int.from_bytes(conn.recv(4), 'big')
            data = conn.recv(length)
            msg = deserialize(data)

            self.node_reference.service(msg)
