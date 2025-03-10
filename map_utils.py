from enum import Enum
from dataclasses import dataclass


# Starts at the bottom left corner (0, 0)
@dataclass
class Location:
    x: int
    y: int

    def add_direction(self, direction: "Direction"):
        match(direction):
            case Direction.LEFT:
                self.x -= 1
            case Direction.RIGHT:
                self.x += 1
            case Direction.DOWN:
                self.y -= 1
            case Direction.UP:
                self.y += 1

class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
