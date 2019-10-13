import numpy as np
import math
import random


class Ai():
    def __init__(self, resolution, all_pos: list, all_ids, options: list):
        self.board_resolution = resolution
        self.all_pos = all_pos
        self.player_option, self.ai_option = options
        self.available_tiles = self.all_pos[:]
        self.ai_move = []
        self.id_array = np.array(all_ids)
        self.id_array = np.reshape(self.id_array, (3, 3))

        self.player_moves = []
        self.ai_moves = []

        # All the possible matches
        # Board:
        # np.array([1 2 3]
        #          [4 5 6]
        #          [7 8 9])

        # Sideway matches
        self.a_match_1 = self.id_array[0, 0], self.id_array[1, 1], self.id_array[2, 2]           # (1, 5, 9)           
        self.a_match_2 = self.id_array[0, 2], self.id_array[1, 1], self.id_array[2, 0]           # (3, 5, 7)  

        # Straight matches
        self.a_match_3 = self.id_array[0, 0], self.id_array[1, 0], self.id_array[2, 0]           # (1, 4, 7)           
        self.a_match_4 = self.id_array[0, 1], self.id_array[1, 1], self.id_array[2, 1]           # (2, 5, 8)         
        self.a_match_5 = self.id_array[0, 2], self.id_array[1, 2], self.id_array[2, 2]           # (3, 6, 9)         

        # Side matches
        self.a_match_6 = self.id_array[0, 0], self.id_array[0, 1], self.id_array[0, 2]           # (1, 2, 3)
        self.a_match_7 = self.id_array[1, 0], self.id_array[1, 1], self.id_array[1, 2]           # (4, 5, 6)            
        self.a_match_8 = self.id_array[2, 0], self.id_array[2, 1], self.id_array[2, 2]           # (7, 8, 9)          

        self.all_matches = [self.a_match_1, self.a_match_2, self.a_match_3,
                       self.a_match_4,
                       self.a_match_5,
                       self.a_match_6,
                       self.a_match_7,
                       self.a_match_8,
                       ]

    def calculate_move(self, user_pos: list):
        self.available_tiles.remove(user_pos)

        if len(self.available_tiles) > 1:
            self.ai_move = random.choice(self.available_tiles)
            self.available_tiles.remove(self.ai_move)

    def decide_winner(self, butt_dict, player_butt_id, ai_butt_id):
        self.player_moves.append(player_butt_id)
        self.ai_moves.append(ai_butt_id)

        # won_buttons keep of the buttons to illuminate (or change color)
        won_buttons = tuple()
        won = ""
        # Looping through all the matches and checking if any of those matches are in Player/Ai moves
        for matches in self.all_matches:
            if set(matches).issubset(self.player_moves) or set(matches).issubset(self.ai_moves):
                won_buttons = matches
                won = "Player" if set(matches).issubset(self.player_moves) else "Ai"

        # This changes the color of the buttons that won the match
        for button in butt_dict.values():
            if button[1] in won_buttons:
                button[0].background_normal = ""
                # Green when the player wins and red when the Ai wins
                button[0].background_color = (0, 1, 0, 1) if won == "Player" else (1, 0, 0, 1)

        return won