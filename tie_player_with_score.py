import os

if not os.path.isfile("highscores.txt"):
    with open("highscores.txt", "w+") as file:
        file.write("name,player_score\n")

player_info = {}

with open("highscores.txt", "r") as highscores_file:
    file_contents = highscores_file.readlines()[1:]

    for entry in file_contents:
        name, score = entry.strip("\n").split(",")

        player_info[name] = score


def tie_player(player_name, winner):

    with open("highscores.txt", "r+") as highscores_file:
        first_line = highscores_file.readline()
        file_contents = highscores_file.readlines()

        for entry in file_contents:
            name, score = entry.strip("\n").split(",")

            if player_name == name:
                player_info[player_name] = int(score) + 1 if winner == "Player" else int(score) - 1
    
    with open("highscores.txt", "r+") as file:
        file.write(first_line)
        for name, score in player_info.items():
            file.write(f"{name},{str(score)}\n")