from vehicle import Vehicle
import tank
from map_utils import *


class Tunnel(Vehicle):
    def __init__(self, tank: "tank.Tank"):
        self.tank = tank
        super().__init__(tank.game, tank.location, tank.facing_direction)
