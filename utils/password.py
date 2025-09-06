from utils.keyboard import KeyboardScreen
from utils.config_loader import read_txt_file, update_text_language
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.uix.label import Label
from utils.keyboard import show_saved_popup
from kivy.app import App

class PasswordScreen(KeyboardScreen):
    def __init__(self,title = 'enter_password', **kwargs):
        super().__init__(title,**kwargs)
        self.password = read_txt_file("temp/password.txt").strip()
        self.screen_name = None

    def press_enter(self, instance):
        """
        Override the on_enter method to set the keyboard title.
        """    
        if self.keyboard.text_input.text == self.password:
            show_saved_popup(text = 'correct_password')
            App.get_running_app().sm.current = self.screen_name
        else:
            show_saved_popup(text = 'incorrect_password')
            self.keyboard.text_input.text = ''
            self.keyboard.actual_text_input = ''
    
    
    

