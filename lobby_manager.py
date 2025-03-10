from lobby import Lobby
from collections import defaultdict
from typing import Dict

class LobbyManager:
    instance: "LobbyManager"

    def __init__(self) -> None:
        self.__class__.instance = self
        self.lobbies: Dict[int, Lobby] = defaultdict(Lobby)

    def get_or_create_lobby(self, lobby_id: int) -> Lobby:
        return self.lobbies[lobby_id]

