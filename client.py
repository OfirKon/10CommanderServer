from typing import List
from select import select
import socket
import logging

from map_utils import *
from reactor import Handler
from lobby_manager import LobbyManager

logger = logging.getLogger(__name__)

class Client(Handler):
    id_counter = 0

    def __init__(self, sock: socket.socket) -> None:
        self.__class__.id_counter += 1
        self.id = self.__class__.id_counter
        logger.info(f"New client #{self.id}")

        self.sock = sock
        self.socket_buffer = b""
        self.lobby = None

    def fileno(self) -> int:
        return self.sock.fileno()

    def close(self):
        self.sock.close()

    def send_message(self, message: str):
        print(f"Sending: {message}")
        message += ";\n"
        self.sock.sendall(message.encode())

    def read_all_from_socket(self):
        # logging.debug("Start reading client's socket")
        while True:
            if (fileno := self.sock.fileno()) <= 0:
                self.close()
                return
            result, _, _ = select([fileno], [], [], 0)
            if result:
                cur_read = self.sock.recv(2048)
                if len(cur_read) == 0:
                    logging.debug("Closing socket")
                    self.close()
                    return
                logger.debug(f"cur_read: {cur_read}")
                self.socket_buffer += cur_read
            else:
                # logging.debug("Done reading")
                return

    def handle_game_message(self, partial_message: List[str]):
        match(partial_message):
            case ["Tank", "Move", x, y]:
                x, y = reverse_location(x, y)
                self.notify_others(f"Enemy.Move.{x}.{y}")
            case ["Tank", "Rotate", direction]:
                self.notify_others(f"Enemy.Rotate.{reverse_direction(direction)}")
            case ["Tunnel", "Start"]:
                self.notify_others(f"Enemy.Tunnel.Start")
            case ["Trails", "Remove"]:
                self.notify_others(f"Enemy.Trails.Remove")
            case ["Trails", "Add", x, y, direction]:
                x, y = reverse_location(x, y)
                self.notify_others(f"Enemy.Trails.Add.{x}.{y}.{reverse_direction(direction)}")
            case _:
                logger.error(f"Unknown game message ignored: {partial_message}")

    def handle_message(self, split_message: List[str]):
        match(split_message):
            case ["Lobby", "Connect", gameid, password]:
                self.lobby = LobbyManager.instance.get_or_create_lobby(int(gameid))
                self.lobby.connect(self, int(password))
            case ["Game", *other]:
                self.handle_game_message(other)
            case _:
                logger.error(f"Unknown general message ignored: {split_message}")

    def notify_others(self, message: str):
        logger.info(f"Sending to other clients: {message}")
        if self.lobby:
            self.lobby.send_to_other_clients(self, message)

    def handle(self) -> None:
        # logging.info("Handling")
        self.read_all_from_socket()
        split_result = self.socket_buffer.split(b";")
        self.socket_buffer = split_result[-1]
        for message in split_result[:-1]:
            message = message.decode().strip()
            logger.info(f"Client {self.id}: Handling message: {message}")
            try:
                self.handle_message(message.split("."))
            except Exception:
                logger.exception(f"Failed to handle message: {message}")

