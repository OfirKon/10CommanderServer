from typing import List, Optional
from select import select
import socket
import logging

from map_utils import Direction
from reactor import Handler
from lobby_manager import LobbyManager
from tank import Tank

logger = logging.getLogger(__name__)

class Client(Handler):
    id_counter = 0

    def __init__(self, sock: socket.socket) -> None:
        self.__class__.id_counter += 1
        self.id = self.__class__.id_counter
        logger.info(f"New client #{self.id}")

        self.sock = sock
        self.socket_buffer = b""
        self.tank: Optional[Tank] = None

    def fileno(self) -> int:
        return self.sock.fileno()

    def close(self):
        self.sock.close()

    def read_all_from_socket(self):
        logging.debug("Start reading client's socket")
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
                self.socket_buffer += cur_read
            else:
                logging.debug("Done reading")
                return

    def handle_game_message(self, partial_message: List[str]):
        if self.tank is None:
            raise RuntimeError("Cannot handle Game message since Tank is none")
        match(partial_message):
            case ["Tank", "Move"]:
                self.tank.move()
            case ["Tank", "Rotate", direction]:
                self.tank.rotate(Direction[direction])
            case ["Tunnel", "Start"]:
                self.tank.is_tunneling = True
            case _:
                logger.info("Unknown message ignored.")

    def handle_message(self, split_message: List[str]):
        print(split_message)
        match(split_message):
            case ["Lobby", "Connect", gameid, password]:
                lobby = LobbyManager.instance.get_or_create_lobby(int(gameid))
                self.tank = lobby.connect(self, int(password))
                if self.tank:
                    logger.info("Assigned tank!")
                else:
                    logger.info("No tank assigned!")
            case ["Game", *other]:
                self.handle_game_message(other)
            case _:
                logger.info("Unknown message ignored.")

    def handle(self) -> None:
        logging.info("Handling")
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

