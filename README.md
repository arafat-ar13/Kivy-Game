# Tic-Tac-Toe game made with Python and Kivy

This is a simple Kivy GUI Tic-Tac-Toe game made entirely by me. This is a personal project and I encourage anyone to try the app out if they want. This game has a login system and supports multiple player accounts. It currently allows you to play against the computer and computer's moves are totally random with no complex or smart algorithms implemented. But I created the `game_ai.py` all by myself and I will really appreciate if anyone can take a look at its source code. Though, no implementations of a smart algorithm, the `game_ai.py` has some decent code that can figure out which tiles on the board are empty and pick a random tile and also place a "X" there. It also detects when someone has won the game.

## Features

* Multi Player support.
* Manage individual players from a dedicated screen in the app itself.
* Reset game info.
* Currently, the computer can only make completely random moves with no idea how to play the game. But still my program does keep track of empty spaces and only place marks on those screen. The game is also good at detecting if anyone has won, lost or if all the places are filled (therefore the match tied). 
* Shows red or green color on buttons that won the match (red if the Ai wins and green if the player wins)
* Live updating screens: The Highscores Page and the Manage Players page. The highscores page will now read data from the certain game files and will show the latest highscores of each player, all without closing the app. This is achieved by reading data whenever the button to go to the Highscores Page is clicked. The Manage Players page work in the same way.
* Tighter integration of email with its particular password, this fixing certain app signing in functionality.

## Things not recommended

When running the app for the first time, two new .txt files will be created. It's really suggested to not mess with those files as deleting any of them or both will result in lost data in the game or maybe even the game breaking.
The `Game Sounds` folder is not to be touched as well. As removing this will remove the sounds from the game.

## To get the game

  * The first version of this game has been released. To get the exe file please get it from the Releases page. 
  * For those who want to build the game right from the source code just follow the instructions from the requirements folder.

## How to play

To play, at first sign up with whatever info you like. The game still doesn't allow you to play if you don't sign up. The game also features a decently functioning Settings that can handle a lot of low level stuff around the game like resetting the game, managing and deleting players from the game, viewing highscores.
