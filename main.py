from kivy.app import App
from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Color, Rectangle
from hoverable import HoverBehavior
from kivy.uix.behaviors import ButtonBehavior
import json, glob
from pathlib import Path
import random


Builder.load_file("design.kv")
#To load up our kivy file to our python we need to use code above.

#code below is a class to that inherites from the designkv file. In our case weare inherting sign_up_screen
class LoginScreen(Screen):
    def sign_up(self):
        self.manager.current = "sign_up_screen"

    def login(self, uname, pword):
        with open("users.json") as file:
            users = json.load(file)
        if uname in users and users[uname]['password'] == pword:
            self.manager.current = "login_screen_success"
        else:
            self.ids.login_wrong.text = "Wrong username or Password"

    def resetpassword(self):
        self.manager.current = "reset_password"
    


class RootWidget(ScreenManager):
    pass


#Code below is a sign up screen that stores usernames and password when a usr sign up on app. It is stored in a JSON file
class SignUpScreen(Screen):
    def add_user(self, uname, pword):
        with open ("users.json") as file:
            users = json.load(file)
        
        users[uname] = {'username': uname, 'password': pword}

        with open("users.json", 'w') as file:
            json.dump(users, file)
        self.manager.current = "sign_up_screen_success"

class SignUpScreenSuccess(Screen):
    def go_to_login(self):

        self.manager.transition.direction = 'right'
        self.manager.current = "login_screen"

class LoginScreenSuccess(Screen):
    def log_out(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"

    def get_quote(self, feel):
        feel = feel.lower()
        available_feelings = glob.glob("quotes/*txt")

        available_feelings = [Path(filename).stem for filename in available_feelings]

        if feel in available_feelings:
            with open(f"quotes/{feel}.txt", encoding='utf8') as file:
                quotes = file.readlines()
            self.ids.quote.text = random.choice(quotes)
        else:
            self.ids.quote.text = " We have not added that one! Try another feeling"


class ImageButton(ButtonBehavior, HoverBehavior, Image):
    pass


#need to code password reset function
class ResetPassword(Screen):
    pass








#This code create the actual app to load
class MainApp(App):
    def build(self):
        return RootWidget()

#This is requires to run the application since python when ran hard codes a variable called __main__, 
if __name__ == "__main__":
    MainApp().run()