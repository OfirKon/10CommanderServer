from typing import Tuple
from enum import Enum
from dataclasses import dataclass

MAP_HEIGHT = 10
MAP_WIDTH = 11

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
    UP = 0
    LEFT = 1
    DOWN = 2
    RIGHT = 3

    def reverse(self):
        return Direction((self.value + 2) % 4)


def reverse_direction(direction_str: str):
    return Direction[direction_str].reverse().name

def reverse_location(x_str: str, y_str: str) -> Tuple[int, int]:
    x, y = int(x_str), int(y_str)
    return MAP_WIDTH - x - 1, MAP_HEIGHT - y - 1
