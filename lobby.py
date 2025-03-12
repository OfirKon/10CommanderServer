from typing import Dict
import logging

import client

logger = logging.getLogger(__name__)

MAX_LOBBY_SIZE = 2

class Lobby:
    def __init__(self):
        self.password_to_client: Dict[int, client.Client] = {}

    def connect(self, client: "client.Client", password: int):
        if client in self.password_to_client.values():
            raise RuntimeError("Same client tried to connect again.")
        if password in self.password_to_client:
            logger.info(f"Switching client")
            self.password_to_client[password].close()
            self.password_to_client[password] = client
        if len(self.password_to_client) >= MAX_LOBBY_SIZE:
            logger.info("Lobby is max size, refusing new connection.")
            client.close()
            return None
        logger.info("New client connected!")
        self.password_to_client[password] = client

    def send_to_other_clients(self, client: "client.Client", message: str):
        other_clients = set(self.password_to_client.values()) - {client}
        for client in other_clients:
            client.send_message(message)

