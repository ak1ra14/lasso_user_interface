from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from utils.icons import IconTextButton, CircularImageButton
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from utils.config_loader import load_config, update_current_page
from utils.layout import HeaderBar, SafeScreen

class LanguageScreen(SafeScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        header = HeaderBar(title="Language", icon_path="images/home.png", button_text="Home", button_screen="menu")
        buttons = BoxLayout(orientation='horizontal', spacing=80, size_hint_y=0.3, pos_hint={'center_x': 0.5, 'center_y': 0.5}, padding=[80,0,80,0])  # Only left and right padding
        buttons.add_widget(Widget())
        buttons.add_widget(IconTextButton(icon_path="images/english.png", text="English", height=50))
        buttons.add_widget(IconTextButton(icon_path="images/japanese.png", text="Japanese", height=50))
        buttons.add_widget(Widget())
        self.add_widget(header)
        self.add_widget(buttons)
    
    def go_to_main(self, instance):
        """
        Navigate to a specified screen.
        :param instance: The instance of the button that was pressed.
        :param screen_name: The name of the screen to navigate to.
        """
        self.manager.current = 'menu'

    def on_pre_enter(self):
        """
        This method is called when the screen is about to be displayed.
        It can be used to perform any setup or updates needed before the screen is shown.
        """
        # You can add any setup code here if needed
        update_current_page('language')