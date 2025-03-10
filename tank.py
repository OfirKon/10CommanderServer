from game import Game
from vehicle import Vehicle
from map_utils import *
import tunnel


class Tank(Vehicle):
    def __init__(self, game: Game, tank_id:int):
        super().__init__(game, Location(5, 1), Direction.UP)
        self.tank_id = tank_id
        self.tunnel = tunnel.Tunnel(self)
        self.is_tunneling = False

    def move(self):
        if self.is_tunneling:
            self.tunnel.move()
            return
        super().move()
        self.game.notify_enemy("Enemy.Move")

    def rotate(self, direction: Direction):
        if self.is_tunneling:
            self.tunnel.rotate(direction)
            return
        super().rotate(direction)
        self.game.notify_enemy(f"Enemy.Rotate.{direction.name}")
