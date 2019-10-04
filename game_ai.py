import math
import random

class Ai():
    def __init__(self, resolution, all_pos: list, option):
        self.board_resolution = resolution
        self.all_pos = all_pos
        self.option = option
        self.available_tiles = self.all_pos[:]
        self.ai_move = []

    def calculate_move(self, user_pos: list):
        self.available_tiles.remove(user_pos)

        if len(self.available_tiles) > 1:
            self.ai_move = random.choice(self.available_tiles)
            self.available_tiles.remove(self.ai_move)

    def decide_winner(self):
        pass