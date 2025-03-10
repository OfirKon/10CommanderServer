from typing import Dict, Optional
import logging

import client
from game import Game
from tank import Tank

logger = logging.getLogger(__name__)

MAX_LOBBY_SIZE = 2

class Lobby:
    def __init__(self):
        self.game = Game()
        self.password_to_tank: Dict[int, Tank] = {}
        self.password_to_client: Dict[int, client.Client] = {}

    def connect(self, client: "client.Client", password: int) -> Optional[Tank]:
        if client in self.password_to_client.values():
            raise RuntimeError("Same client tried to connect again.")
        if password in self.password_to_tank:
            logger.info(f"Switching client for tank {self.password_to_tank[password].tank_id}")
            self.password_to_client[password].close()
            self.password_to_client[password] = client
            return self.password_to_tank[password]
        if len(self.password_to_tank) >= MAX_LOBBY_SIZE:
            logger.info("Lobby is max size, refusing new connection.")
            client.close()
            return None
        logger.info("New client connected!")
        new_tank = Tank(self.game, len(self.password_to_tank))
        self.password_to_tank[password] = new_tank
        self.password_to_client[password] = client
        return new_tank
