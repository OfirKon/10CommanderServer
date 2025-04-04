from typing import Dict
import logging

import client

logger = logging.getLogger(__name__)

MAX_LOBBY_SIZE = 2

class Lobby:
    def __init__(self):
        self.password_to_client: Dict[int, client.Client] = {}

    def connect(self, client: "client.Client", password: int):
        self.remove_closed_clients()
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

        if len(self.password_to_client) >= MAX_LOBBY_SIZE:
            logger.info("Starting game!")
            for client in self.password_to_client.values():
                client.send_message("Game.Start")

    def remove_closed_clients(self):
        keys_to_remove = []
        for key, client in self.password_to_client.items():
            if client.is_closed:
                keys_to_remove.append(key)

        for key in keys_to_remove:
            del self.password_to_client[key]

    def send_to_other_clients(self, client: "client.Client", message: str):
        other_clients = set(self.password_to_client.values()) - {client}
        for client in other_clients:
            client.send_message(message)

