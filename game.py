import logging
from typing import Set

import client

logger = logging.getLogger(__name__)

class Game:
    def __init__(self) -> None:
        self.clients: Set[client.Client] = set()

    def notify_enemy(self, message: str) -> None:
        logger.info(f"Notifying enemy: {message}")
