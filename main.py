import math
import os

import kivy
from kivy.animation import Animation
from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager, SwapTransition
from kivy.uix.textinput import TextInput

from game_ai import Ai
from tie_player_with_score import tie_player

Config.set('graphics', 'width', '500')
Config.set('graphics', 'height', '400')

if not os.path.isfile("login_info.txt"):
    with open("login_info.txt", "w+") as file:
        file.write("first_name,last_name,email,password\n")


class WelcomeScreen(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1

        self.welcome = Label(
            text="Welcome to my game! Sign up or login below", color=[55, 0, 1, 1])
        self.add_widget(self.welcome)

        self.login = Button(text="Login", font_size=30, size_hint=(1.2, 0.5))
        self.login.bind(on_release=self.login_func)
        self.add_widget(self.login)

        # Creating animation for the three main buttons of our welcome screen
        animation = Animation(
            background_color=[23, 0, 1, 1], duration=1.3, y=162)
        animation.start(self.login)

        self.signup = Button(text="Signup", font_size=30,
                             size_hint=(1.2, 0.5), pos=(0, -117))
        self.signup.bind(on_release=self.signup_func)
        self.add_widget(self.signup)

        animation = Animation(
            background_color=[0, 14, 4, 1], duration=1.28, y=81.5)
        animation.start(self.signup)

        self.settings = Button(
            text="Game settings", font_size=30, size_hint=(1.2, 0.5), pos=(0, -160))
        self.settings.bind(on_press=self.settings_page_func)
        self.add_widget(self.settings)

        animation = Animation(
            background_color=[0, 1, 0, 1], duration=1.3, y=0)
        animation.start(self.settings)

    # Creating functions to access our three main screen
    def signup_func(self, instance):
        tic_tac_toe.screen_manager.current = "Signup Page"

    def login_func(self, instance):
        tic_tac_toe.screen_manager.current = "Login Page"

    def settings_page_func(self, instance):
        tic_tac_toe.screen_manager.current = "Settings Page"


class SignupScreen(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1

        # Creating another Layout object inside of SignupScreen as Kivy doesn't allow "columnspan" like Tkinter
        # We are placing our Label texts inside of the inner Layout while the "Sign up" button is placed on the main "self" Layout
        self.inside = GridLayout()
        self.inside.cols = 2

        self.inside.add_widget(Label(text="First Name: "))
        self.first_name = TextInput(multiline=False)
        self.inside.add_widget(self.first_name)

        self.inside.add_widget(Label(text="Last Name: "))
        self.last_name = TextInput(multiline=False)
        self.inside.add_widget(self.last_name)

        self.inside.add_widget(Label(text="Email: "))
        self.email = TextInput(multiline=False)
        self.inside.add_widget(self.email)

        self.inside.add_widget(Label(text="Password"))
        self.password = TextInput(password=True, multiline=False)
        self.inside.add_widget(self.password)

        self.inside.add_widget(Label(text="Enter password again"))
        self.again_password = TextInput(password=True, multiline=False)
        self.inside.add_widget(self.again_password)

        self.add_widget(self.inside)

        self.signup = Button(text="Sign up", font_size=30,
                             size_hint=(1.0, 0.6))
        self.add_widget(self.signup)
        # <<<<< It's important to check if the password fields are empty before checking if they are correct or not
        self.signup.bind(on_press=self.check_if_empty)
        self.signup.bind(on_press=self.check_password)

        # Creating a button to go back to the main screen
        self.welcome_page = Button(
            text="Back to main screen", font_size=30, size_hint=(0.8, 0.4))
        self.add_widget(self.welcome_page)
        self.welcome_page.bind(on_press=self.back_to_home)

    def back_to_home(self, instance):
        tic_tac_toe.screen_manager.current = "Welcome Page"

    def check_password(self, instance):
        if self.password.text != "":
            if self.password.text == self.again_password.text:
                self.write_to_file()

                popup = Popup(title="Signup confirmation", content=Label(
                    text="Welcome!!", color=[0, 1, 0, 1]), size_hint=(0.6, 0.2))
                popup.open()

                tic_tac_toe.home_page.update_info(
                    "Welcome to your home page")
                tic_tac_toe.screen_manager.current = "Home Page"

            else:
                self.password.text = self.again_password.text = ""

                popup = Popup(title="Password check error", content=Label(
                    text="You passwords didn't match", color=[1, 0, 0, 1]), size_hint=(0.6, 0.2))
                popup.open()

    def check_if_empty(self, instance):
        if not self.first_name.text or not self.last_name.text or not self.email.text:
            empty_warning = Popup(title="Input fields empty", content=Label(
                text="You cannot leave any of the fields empty", color=[1, 0, 0, 1]), size_hint=(0.6, 0.2))
            empty_warning.open()

    def write_to_file(self):
        first_name = self.first_name.text
        last_name = self.last_name.text
        email = self.email.text

        # Hashing the password for security
        password = self.password.text[::-1]

        with open("login_info.txt", "a") as file:
            file.write(f"{first_name},{last_name},{email},{password}\n")
        with open("highscores.txt", "a") as file:
            file.write(f"{first_name} {last_name},{0}\n")

        tic_tac_toe.login_page.account_query_for[2] = f"{first_name} {last_name}"


class LoginScreen(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Creating a list as a "placeholder" for email, password and full name
        self.account_query_for = ["email", "password", "name"]
        self.cols = 1

        self.inside = GridLayout()
        self.inside.cols = 2

        self.inside.add_widget(Label(text="Email:"))
        self.email = TextInput(multiline=False)
        self.inside.add_widget(self.email)

        self.inside.add_widget(Label(text="Password"))
        self.password = TextInput(password=True, multiline=False)
        self.inside.add_widget(self.password)

        self.add_widget(self.inside)

        self.submit = Button(text="Submit!", font_size=30,
                             size_hint=(1.0, 0.6))
        self.add_widget(self.submit)
        self.submit.bind(on_press=self.check_input_info)

        self.welcome_page = Button(
            text="Back to main screen", font_size=30, size_hint=(0.8, 0.4))
        self.add_widget(self.welcome_page)
        self.welcome_page.bind(on_press=self.back_to_home)

    def back_to_home(self, instance):
        tic_tac_toe.screen_manager.current = "Welcome Page"

    def check_input_info(self, instance):
        with open("login_info.txt", "r") as file:

            file_contents = file.readlines()
            for line in file_contents:
                first_name, last_name, email, hashed_password = line.split(",")
                # Unhashing the password and removing any newline characters
                real_password = hashed_password[::-1]
                real_password = real_password.strip("\n")

                if email == self.email.text:
                    # We are first checking if any email in our data file matches the email given by the user
                    # If an email match is found then the password is set for that email in the text file
                    # This strictly ties the password with that email only
                    self.account_query_for[0] = email
                    self.account_query_for[1] = real_password
                    self.account_query_for[2] = f"{first_name} {last_name}"

            # If the first item in account_query_for is "email" that means that the system didn't find any match,
            # if it had found then it would have updated the items in account_query_for with the correct credentials
            if self.account_query_for[0] == "email":
                no_account_found_warning = Popup(title="No matching accounts", content=Label(
                    text="We couldn't find your account", color=[1, 0, 0, 1]), size_hint=(0.6, 0.2))
                no_account_found_warning.open()

            allowance = False
            if self.account_query_for[0] != "email":

                if self.password.text == self.account_query_for[1]:
                    allowance = True
                else:
                    self.password.text = ""

                    popup = Popup(title="Wrong password", content=Label(
                        text="Your password is incorrect", color=[1, 0, 0, 1]), size_hint=(0.6, 0.2))
                    popup.open()

                if allowance:
                    self.password.text = ""

                    tic_tac_toe.home_page.update_info(
                        f"Welcome to your Home Page, {self.account_query_for[2]}")
                    tic_tac_toe.screen_manager.current = "Home Page"


class HomeScreen(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.message = Label(halign="center", valign="middle", font_size=35)
        self.message.bind(width=self.update_text_width)
        self.add_widget(self.message)
        message_animation = Animation(color=[1, 0, 0, 1], duration=.8)
        message_animation.start(self.message)

        # Adding a button to go back to the login screen
        self.back = Button(text="Start your game",
                           font_size=30, size_hint=(0.6, 0.2))
        self.add_widget(self.back)
        self.back.bind(on_release=self.enter_game_screen)

        # Adding a button to go the highscores screen
        self.highscores = Button(
            text="View you scores", font_size=28, size_hint=(0.55, 0.19))
        self.add_widget(self.highscores)
        self.highscores.bind(on_press=self.enter_scores_screen)

        # Adding a button to start the game
        self.game_start = Button(
            text="Logout", font_size=23, size_hint=(0.6, 0.2))
        self.add_widget(self.game_start)
        self.game_start.bind(on_press=self.logout)

    def update_info(self, message):
        self.message.text = message

    def update_text_width(self, *_):
        self.message.text_size = (self.message.width*0.9, None)

    def enter_game_screen(self, *_):
        tic_tac_toe.screen_manager.current = "Game Page"

    def enter_scores_screen(self, *_):
        tic_tac_toe.highscores_page.here_from = "Home Page"
        tic_tac_toe.screen_manager.current = "HighScores Page"

    def logout(self, *_):
        tic_tac_toe.screen_manager.current = "Login Page"


class GameScreen(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Our main screen for gaming
        self.cols = 3
        self.rows = 3
        self.buttons_dict = {}
        self.moves_counter = 0

        # Setting up a list to store the game input options
        self.fill_options = ["O", "X"]

        # Creating a board made of buttons
        for button_count in range(self.cols * self.rows):
            self.buttons_dict["Button_" + str(button_count)] = [Button(
                halign="center", valign="middle", font_size=40, on_press=self.fill_button)]

        for count, button in enumerate(self.buttons_dict.values(), start=1):
            self.add_widget(button[0])
            # Making IDs of each button for tracking buttons
            button.append(count)

        # Creating the AI instantiation
        self.ai = Ai(self.cols * self.rows, [position[0].pos for position in self.buttons_dict.values()], [
                     button[1] for button in self.buttons_dict.values()], self.fill_options)

    def fill_button(self, instance):
        if not hasattr(instance, "pressed") or not instance.pressed:
            self.ai.calculate_move(instance.pos)

            instance.text = self.fill_options[0]
            setattr(instance, "pressed", True)

            self.moves_counter += 1

        computer_move = self.ai.ai_move
        computer_button_instance = ""
        computer_button_id = 0
        for button in self.buttons_dict.values():

            if computer_move == button[0].pos:
                if not hasattr(button[0], "pressed") or not button[0].pressed:
                    button[0].text = self.ai.ai_option
                    computer_button_instance = button[0]
                    computer_button_id = button[1]
                    setattr(button[0], "pressed", True)
                    setattr(button[0], "checked_winner_on", True)

                    if self.moves_counter < 9:
                        self.moves_counter += 1

        instance_id = 0
        for button in self.buttons_dict.values():
            if button[0] == instance:
                instance_id = button[1]

        if not hasattr(instance, "checked_winner_on"):
            winner = self.ai.decide_winner(
                self.buttons_dict, instance, computer_button_instance, instance_id, computer_button_id)
            setattr(instance, "checked_winner_on", True)

        if winner != "" and winner == "Player":
            tie_player(tic_tac_toe.login_page.account_query_for[2])

        Clock.schedule_once(lambda instance: self.game_over(
            self.moves_counter, winner), 0.6)

    def game_over(self, moves_counter, winner):
        if self.moves_counter == (self.cols * self.rows) or winner != "":
            pop_up_layout = BoxLayout(orientation='vertical', padding=(10))

            # Setting up the popup_title depending on who the winner is or if no one won
            popup_title = f"{tic_tac_toe.login_page.account_query_for[2]} is the winner!" if winner == "Player" else "AI beat your ass!"
            popup = Popup(title=popup_title if winner != "" else "It's a tie!!",
                          content=pop_up_layout, size_hint=(0.8, 0.7))

            # Setting up the popup message depending on who won. ALso setting up the color
            popup_msg = "You have won the game!!" if winner == "Player" else "You have lost the game!!"
            popup_msg_color = [
                0, 1, 0, 1] if winner == "Player" else [1, 0, 0, 1]
            game_over_msg = Label(text=popup_msg if winner != "" else "The game is over. It is a tie!!",
                                  color=popup_msg_color if winner != "" else [1, 1, 1, 1])

            pop_up_layout.add_widget(game_over_msg)

            back_to_user_page = Button(
                text="Go back", on_press=lambda instance: self.reset_board(popup, True))
            another_game = Button(text="Or...player another game!!",
                                  on_press=lambda instance: self.reset_board(popup, False))

            pop_up_layout.add_widget(back_to_user_page)
            pop_up_layout.add_widget(another_game)

            popup.open()

    def reset_board(self, popup, back_to_user_home):

        for button in self.buttons_dict.values():
            button[0].text = ""
            setattr(button[0], "pressed", False)
            if hasattr(button[0], "checked_winner_on"):
                delattr(button[0], "checked_winner_on")

            button[0].background_normal = "atlas://data/images/defaulttheme/button"
            button[0].background_color = (1, 1, 1, 1)

        popup.dismiss()

        self.moves_counter = 0
        self.ai.available_tiles = self.ai.all_pos[:]

        self.ai.player_moves.clear()
        self.ai.ai_moves.clear()

        if back_to_user_home:
            tic_tac_toe.screen_manager.current = "Home Page"


class HighScoresScreen(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.here_from = ""

        self.cols = 1
        self.file = open("highscores.txt", "r")
        self.inside = GridLayout()
        self.inside.cols = 2
        self.inside.rows = len(self.file.readlines())
        self.rows = self.inside.rows
        self.file.close()

        self.name_label = Label(text="Name")
        self.inside.add_widget(self.name_label)
        self.score_label = Label(text="Score")
        self.inside.add_widget(self.score_label)

        with open("highscores.txt", "r") as file:
            contents = file.readlines()[1:]

            scores = []
            names = []
            for entry in contents:
                name, score = entry.strip("\n").split(",")

                scores.append(int(score))
                names.append(name)

            # This sorts the names according to who has the highest points
            names = [x for _, x in sorted(zip(scores, names), reverse=True)]
            scores = sorted(scores, reverse=True)

            for name, score in zip(names, scores):

                self.inside.add_widget(Label(text=f"{name}"))
                self.inside.add_widget(Label(text=str(score)))

        self.add_widget(self.inside)

        self.back_button = Button(text="Go back", size_hint=(0.2, 0.18))
        self.add_widget(self.back_button)
        self.back_button.bind(on_press=self.go_back)
    
    def go_back(self, instance):
        tic_tac_toe.screen_manager.current = self.here_from


class SettingsScreen(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.rows = 4

        # A settings to manage and view the high scores
        self.high_scores_button = Button(text="View high scores", size_hint=(
            0.5, 0.2), background_color=[1, 1, 0, 1], on_press=self.view_high_scores)
        self.add_widget(self.high_scores_button)

        # This resets all the player info from the app. Use with caution
        self.reset_info_button = Button(text="Reset game info", size_hint=(
            0.5, 0.2), background_color=[1, 0, 0, 0.75], on_press=self.manage_game_reset)
        self.add_widget(self.reset_info_button)

        # A settings to manage the players
        self.manage_players_button = Button(
            text="Manage players", size_hint=(0.5, 0.2), on_press=self.manage_players)
        self.add_widget(self.manage_players_button)

        # A settings to go back to the welcome screen
        self.welcome_page = Button(text="Back to main screen", size_hint=(
            0.3, 0.2), on_press=self.back_to_home)
        self.add_widget(self.welcome_page)

    def back_to_home(self, instance):
        tic_tac_toe.screen_manager.current = "Welcome Page"

    def view_high_scores(self, instance):
        tic_tac_toe.highscores_page.here_from = "Settings Page"
        tic_tac_toe.screen_manager.current = "HighScores Page"

    def manage_game_reset(self, instance):
        pop_up_layout = BoxLayout(orientation='vertical', padding=(10))

        deletion_message = Label(
            text="Are you sure? This cannot be undone.", color=[1, 0, 0, 1])
        pop_up_layout.add_widget(deletion_message)

        yes_button = Button(text="Yes reset the game")
        no_button = Button(
            text="Don't reset my game!!")

        pop_up_layout.add_widget(yes_button)
        pop_up_layout.add_widget(no_button)

        # This is named "fake_instance" so that it doesn't get mixed with the main "instance" in the outer function manage_game_reset
        def reset_game(fake_instance):
            if instance != None:
                with open("login_info.txt", "r+") as file:
                    first_line = file.readline()

                    file.seek(0)
                    file.truncate()
                    file.write(first_line)

                with open("highscores.txt", "r+") as file:
                    first_line = file.readline()

                    file.seek(0)
                    file.truncate()
                    file.write(first_line)

            # Clearing the players screen and adding only the back button
            tic_tac_toe.players_page.canvas.clear()

            tic_tac_toe.players_page.cols = 1
            tic_tac_toe.players_page.go_back = Button(text="Go back to settings", size_hint=(
                0.8, 0.19), on_press=tic_tac_toe.players_page.back_to_settings)
            tic_tac_toe.players_page.add_widget(
                tic_tac_toe.players_page.go_back)

            deletion_message.text = "Success! This popup will dismiss any time now."
            deletion_message.color = [0, 1, 0, 1]

            Clock.schedule_once(popup.dismiss, 0.5)

        popup = Popup(title='Game reset confirmation', title_size=(30),
                      title_align='center', content=pop_up_layout,
                      size_hint=(None, None), size=(400, 400),
                      auto_dismiss=False)

        yes_button.bind(on_press=reset_game)
        no_button.bind(on_press=popup.dismiss)

        popup.open()

    def manage_players(self, instance):
        tic_tac_toe.screen_manager.current = "Manage Players Page"


class ManagePlayers(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.inside = GridLayout()

        self.file = open("login_info.txt", "r")
        self.inside.cols = 2
        self.inside.rows = len(self.file.readlines())
        self.file.close()

        with open("login_info.txt", "r") as file:
            file_contents = file.readlines()[1:]
            file_contents = [content.strip("\n") for content in file_contents]

            buttons_dict = {}
            labels_dict = {}

            def manage_player_deletion(instance):
                pop_up_layout = BoxLayout(orientation='vertical', padding=(10))

                deletion_message = Label(
                    text="Are you sure? You cannot undo this.", color=[1, 0, 0, 1])
                pop_up_layout.add_widget(deletion_message)

                yes_button = Button(text="Yes delete the player")
                no_button = Button(
                    text="I changed my mind. The player can stay!")

                pop_up_layout.add_widget(yes_button)
                pop_up_layout.add_widget(no_button)

                def delete_player(fake_instance):
                    # The parameter is named "fake_instance" so that it doesn't get mixed with the main
                    # "instance" in the outer function manage_player_deletion

                    for label in labels_dict.values():
                        if label.text in instance.text:
                            for data in file_contents:

                                # Stripping the whitespace between first and last name
                                if label.text.replace(" ", "") == "".join(data.split(",")[0] + data.split(",")[1]):

                                    with open("login_info.txt", "r") as f:
                                        lines = f.readlines()

                                    with open("login_info.txt", "w") as f:
                                        for line in lines:
                                            if line.strip("\n") != data:
                                                f.write(line)

                    deletion_message.text = "Success! This popup will dismiss any time now."
                    deletion_message.color = [0, 1, 0, 1]

                    Clock.schedule_once(popup.dismiss, 0.5)

                popup = Popup(title='Player deletion confirmation', title_size=(30),
                              title_align='center', content=pop_up_layout,
                              size_hint=(None, None), size=(400, 400),
                              auto_dismiss=False)

                yes_button.bind(on_press=delete_player)
                no_button.bind(on_press=popup.dismiss)

                popup.open()

            for count, content in enumerate(file_contents, start=1):
                first, last, *_ = content.split(",")
                name = first + " " + last

                labels_dict["player_label_" + str(count)] = Label(text=name)
                buttons_dict["remove_butt_" + str(count)] = Button(
                    text=f"Remove {name}", on_press=manage_player_deletion)

            for label, button in zip(labels_dict.values(), buttons_dict.values()):
                self.inside.add_widget(label)
                self.inside.add_widget(button)

        self.add_widget(self.inside)

        self.cols = 1
        self.go_back = Button(text="Go back to settings", size_hint=(
            0.8, 0.19), on_press=self.back_to_settings)
        self.add_widget(self.go_back)

    def back_to_settings(self, instance):
        tic_tac_toe.screen_manager.current = "Settings Page"


class MyApp(App):
    def build(self):
        self.screen_manager = ScreenManager(transition=SwapTransition())

        # Creating all of our screens to show up
        # Welcome Screen
        self.welcome_page = WelcomeScreen()
        screen = Screen(name="Welcome Page")
        screen.add_widget(self.welcome_page)
        self.screen_manager.add_widget(screen)

        # Signup Screen
        self.signup_page = SignupScreen()
        screen = Screen(name="Signup Page")
        screen.add_widget(self.signup_page)
        self.screen_manager.add_widget(screen)

        # Login Screen
        self.login_page = LoginScreen()
        screen = Screen(name="Login Page")
        screen.add_widget(self.login_page)
        self.screen_manager.add_widget(screen)

        # Home Screen
        self.home_page = HomeScreen()
        screen = Screen(name="Home Page")
        screen.add_widget(self.home_page)
        self.screen_manager.add_widget(screen)

        # Game Screen
        self.game_page = GameScreen()
        screen = Screen(name="Game Page")
        screen.add_widget(self.game_page)
        self.screen_manager.add_widget(screen)

        # High Scores Screen
        self.highscores_page = HighScoresScreen()
        screen = Screen(name="HighScores Page")
        screen.add_widget(self.highscores_page)
        self.screen_manager.add_widget(screen)

        # Making a settings screen for managing certain things in the game
        self.settings_page = SettingsScreen()
        screen = Screen(name="Settings Page")
        screen.add_widget(self.settings_page)
        self.screen_manager.add_widget(screen)

        # Adding the screen for managing players
        self.players_page = ManagePlayers()
        screen = Screen(name="Manage Players Page")
        screen.add_widget(self.players_page)
        self.screen_manager.add_widget(screen)

        return self.screen_manager


if __name__ == "__main__":
    tic_tac_toe = MyApp()
    tic_tac_toe.run()
