from client import Client
from reactor import Handler, Reactor
# from typing import final
import socket
import logging

logger = logging.getLogger(__name__)

# @final
class Server(Handler):
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(("0.0.0.0", 41337))
        self.server_socket.listen()

    def fileno(self) -> int:
        return self.server_socket.fileno()

    def handle(self) ->  None:
        # logger.info("Accepting new connection")
        client_socket, _ = self.server_socket.accept()
        Reactor.instance().add(Client(client_socket))
        self.server_socket.listen()

    def close(self):
        self.server_socket.close()
        print("\n\nCLOSED SOCKET\n\n")
