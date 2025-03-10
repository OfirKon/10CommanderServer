from game import Game
from map_utils import Direction, Location

class Vehicle:
    def __init__(self, game: Game, initial_location: Location, initial_facing_direction: Direction):
        self.game = game
        self.location = initial_location
        self.facing_direction = initial_facing_direction

    def move(self):
        self.location.add_direction(self.facing_direction)

    def rotate(self, direction: Direction):
        self.facing_direction = direction
