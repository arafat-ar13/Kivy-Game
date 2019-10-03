import kivy
from kivy.animation import Animation
from kivy.app import App
from kivy.config import Config
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager, SwapTransition
from kivy.uix.textinput import TextInput
from kivy.clock import Clock

Config.set('graphics', 'width', '500')
Config.set('graphics', 'height', '400')


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

        animation = Animation(
            background_color=[23, 0, 1, 1], duration=1.3, y=90)
        animation.start(self.login)

        self.signup = Button(text="Signup", font_size=30,
                             size_hint=(1.2, 0.5), pos=(0, -105))
        self.signup.bind(on_release=self.signup_func)
        self.add_widget(self.signup)

        animation = Animation(
            background_color=[0, 14, 4, 1], duration=1.3, y=0)
        animation.start(self.signup)

        self.settings = Button(
            text="Game settings", font_size=35, size_hint=(1.2, 0.5), pos=(0, -160))
        self.settings.bind(on_press=self.login_to_admin)
        self.add_widget(self.settings)

        animation = Animation(
            background_color=[0, 1, 0, 1], duration=1.3, y=180)
        animation.start(self.settings)

    def signup_func(self, instance):
        tick_tack_toe.screen_manager.current = "Signup Page"

    def login_func(self, instance):
        tick_tack_toe.screen_manager.current = "Login Page"

    def login_to_admin(self, instance):
        tick_tack_toe.screen_manager.current = "Settings Page"


class SignupScreen(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1

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

        self.signup = Button(text="Sign up", font_size=30)
        self.add_widget(self.signup)
        self.signup.bind(on_press=self.check_if_empty)
        self.signup.bind(on_press=self.check_password)

    def check_password(self, instance):
        if self.password.text != "":
            if self.password.text == self.again_password.text:
                self.write_to_file()

                popup = Popup(title="Signup confirmation", content=Label(
                    text="Welcome!!", color=[0, 1, 0, 1]), size_hint=(0.6, 0.2))
                popup.open()

                tick_tack_toe.home_page.update_info(
                    "Welcome to your home page")
                tick_tack_toe.screen_manager.current = "Home Page"

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
            file.write(f"\n{first_name},{last_name},{email},{password}")


class LoginScreen(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1

        self.inside = GridLayout()
        self.inside.cols = 2

        self.inside.add_widget(Label(text="Email: ", color=[0, 0, 1, 1]))
        self.email = TextInput(multiline=False)
        self.inside.add_widget(self.email)

        self.inside.add_widget(Label(text="Password"))
        self.password = TextInput(password=True, multiline=False)
        self.inside.add_widget(self.password)

        self.add_widget(self.inside)

        self.submit = Button(text="Submit!", font_size=35)
        self.add_widget(self.submit)
        self.submit.bind(on_press=self.check_input_info)

    def check_input_info(self, instance):
        with open("login_info.txt", "r") as file:
            account_query_for = ["email", "password", "name"]

            file_contents = file.readlines()
            for line in file_contents:
                first_name, last_name, email, hashed_password = line.split(",")
                real_password = hashed_password[::-1]
                real_password = real_password.strip("\n")

                if email == self.email.text:
                    account_query_for[0] = email
                    account_query_for[1] = real_password
                    account_query_for[2] = f"{first_name} {last_name}"

            if account_query_for[0] == "email":
                no_account_found_warning = Popup(title="No matching accounts", content=Label(
                    text="We couldn't find your account", color=[1, 0, 0, 1]), size_hint=(0.6, 0.2))
                no_account_found_warning.open()

            allowance = False
            if account_query_for[0] != "email":

                if self.password.text == account_query_for[1]:
                    allowance = True
                else:
                    self.password.text = ""

                    popup = Popup(title="Wrong password", content=Label(
                        text="Your password is incorrect", color=[1, 0, 0, 1]), size_hint=(0.6, 0.2))
                    popup.open()

                if allowance:
                    self.password.text = ""

                    tick_tack_toe.home_page.update_info(
                        f"Welcome to your Home Page, {account_query_for[2]}")
                    tick_tack_toe.screen_manager.current = "Home Page"


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
        self.back = Button(text="Logout", font_size=30, size_hint=(0.6, 0.2))
        self.add_widget(self.back)
        self.back.bind(on_release=self.logout)

        # Adding a button to start the game
        self.game_start = Button(
            text="Start your game", font_size=23, size_hint=(0.6, 0.2))
        self.add_widget(self.game_start)
        self.game_start.bind(on_press=self.enter_game_screen)

    def update_info(self, message):
        self.message.text = message

    def update_text_width(self, *_):
        self.message.text_size = (self.message.width*0.9, None)

    def enter_game_screen(self, *_):
        tick_tack_toe.screen_manager.current = "Game Page"

    def logout(self, *_):
        tick_tack_toe.screen_manager.current = "Login Page"


class GameScreen(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.cols = 1

        self.welcome_label = Label(text="Welcome bee ach")
        self.add_widget(self.welcome_label)


class SettingsScreen(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.rows = 3

        self.high_scores_button = Button(text="View high scores", size_hint=(
            0.5, 0.2), background_color=[1, 1, 0, 1], on_press=self.view_high_scores)
        self.add_widget(self.high_scores_button)

        self.reset_info_button = Button(text="Reset game info", size_hint=(
            0.5, 0.2), background_color=[1, 0, 0, 0.75], on_press=self.reset_game)
        self.add_widget(self.reset_info_button)

        self.manage_players_button = Button(
            text="Manage players", size_hint=(0.5, 0.2), on_press=self.manage_players)
        self.add_widget(self.manage_players_button)

    def view_high_scores(self, instance):
        pass

    def reset_game(self, instance):
        if instance != None:
            with open("login_info.txt", "r+") as file:
                first_line = file.readline()

                file.seek(0)
                file.truncate()
                file.write(first_line)

        # Clearing the players screen and adding only the back button
        tick_tack_toe.players_page.canvas.clear()

        tick_tack_toe.players_page.cols = 1
        tick_tack_toe.players_page.go_back = Button(text="Go back to settings", size_hint=(
            0.8, 0.19), on_press=tick_tack_toe.players_page.back_to_settings)
        tick_tack_toe.players_page.add_widget(
            tick_tack_toe.players_page.go_back)

    def manage_players(self, instance):
        tick_tack_toe.screen_manager.current = "Manage Players Page"


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

                deletion_message =Label(text="Are you sure? You cannot undo this.", color=[1, 0, 0, 1])
                pop_up_layout.add_widget(deletion_message)

                yes_button = Button(text="Yes delete the player")
                no_button = Button(
                    text="I changed my mind. The player can stay!")

                pop_up_layout.add_widget(yes_button)
                pop_up_layout.add_widget(no_button)

                def delete_player(fake_instance):

                    for label in labels_dict.values():
                        if label.text in instance.text:
                            for data in file_contents:
                                line_index = file_contents.index(data) + 1

                                if label.text.replace(" ", "") == "".join(data.split(",")[0] + data.split(",")[1]):

                                    with open("login_info.txt", "r") as f:
                                        lines = f.readlines()
                                        if line_index == len(lines) - 1:
                                            last_line_stripped = lines[-2].strip(
                                                "\n")
                                            lines[-2] = last_line_stripped

                                    with open("login_info.txt", "w") as f:
                                        for line in lines:
                                            if line.strip("\n") != data:
                                                f.write(line)

                    deletion_message.text = "Success! This popup will dismiss in 2 seconds."
                    deletion_message.color = [0, 1, 0, 1]

                    Clock.schedule_once(popup.dismiss, 2)
                    

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
        tick_tack_toe.screen_manager.current = "Settings Page"


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
    tick_tack_toe = MyApp()
    tick_tack_toe.run()
