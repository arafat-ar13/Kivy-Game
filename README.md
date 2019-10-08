# Tic-Tac-Toe game made with Python and Kivy

This is a simple Kivy GUI Tic-Tac-Toe game made entirely by me. This is a personal project and I encourage anyone to try the app out if they want. This game has a login system and supports multiple player accounts. It currently allows you to play against the computer and computer's moves are totally random with no complex or smart algorithms implemented. But I created the `game_ai.py` all by myself and I will really appreciate if anyone can take a look at its source code. Though, no implementations of a smart algorithm, the `game_ai.py` has some decent code that can figure out which tiles on the board are empty and pick a random tile and also place a "X" there. It also detects when someone has won the game.

## How to play

To play, at first make up to sign up with whatever info you like. The game still doesn't allow you to play if you don't sign up. The game also features a decently functioning Settings that can handle a lot of low level stuff around the game like resetting the game, managing and deleting players from the game, viewing highscores, with ton more settings options to come.

To get the game, please follow along the instructions from `requirements` above.

## Known bugs and how to avoid them

The game has some bugs that need to be avoided until I fix them (as soon as possible)

* When playing, when you click on an empty board, it places a "O" there and the computer randomly places a "X" on any of the other tiles. For now, don't click on any of your "O"s or any of the computer's "X"s as it breaks the program. In other words, don't click on a tile that you or the computer have already placed mark on.

* I don't know if this creates issue for every computer, but when following the instructions from the `requirements` above, if using `python` (where applicable) doesn't work, please use `python3`.
