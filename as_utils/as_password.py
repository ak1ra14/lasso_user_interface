from kivy.app import App

from as_utils.as_keyboard import KeyboardScreen
from as_utils.as_config_loader import read_txt_file, update_text_language
from as_utils.as_keyboard import show_saved_popup

class PasswordScreen(KeyboardScreen):
    def __init__(self,title = 'enter_password', **kwargs):
        super().__init__(title,**kwargs)
        self.password = read_txt_file("as_temp/password.txt").strip()
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
    
    def on_pre_enter(self):
        super().on_pre_enter()
        self.keyboard.text_input.text = ''
        self.keyboard.actual_text_input = ''

    
    

