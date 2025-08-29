from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from utils.icons import ColoredLabel
from kivy.core.audio import SoundLoader
from kivy.app import App
from kivy.clock import Clock
from utils.config_loader import load_config, update_current_page, update_text_language
from utils.layout import HeaderBar, SafeScreen
import socket

class MonitorScreen(SafeScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print("MonitorScreen initialized")
        header = BoxLayout(orientation='horizontal', pos_hint={'top': 1}, size_hint_y=0.2, padding=10, spacing=10)
        self.ip_label = ColoredLabel(
            text=f"{update_text_language('ip_address')}: {App.get_running_app().ip_address}",
            font_size=20,
            color=(0, 0, 0, 1),  # Black text
            size_hint=(None, None),
            size=(300, 40),
            font_name='fonts/MPLUS1p-Regular.ttf',
            pos_hint={'left': 1, 'top': 1},
            bg_color=(1,1,1,1)  # RGBA
        )

        self.ip_label.bind(size=self.ip_label.setter('text_size'))  # For text wrapping
        header.add_widget(self.ip_label)
        header.bind(minimum_height=header.setter('height'))
        header.add_widget(Widget())  # Spacer

        setting_button = Button(
            background_normal='images/settings.png',
            background_down='images/settings.png',
            size_hint=(None, None),
            size=(50, 50),
            pos_hint={'right': 1, 'top': 1},
            on_press=self.go_to_menu)
        
        setting_button.bind(size=setting_button.setter('size'))
        setting_button.bind(pos=setting_button.setter('pos'))
        header.add_widget(setting_button)
        self.add_widget(header)

        self.add_widget(Image(
            source='images/soundeye.png',
            size_hint=(0.5, 0.5),
            pos_hint={'center_x': 0.5, 'center_y': 0.5})
        )
        
    def go_to_menu(self, instance):
        print("Going to menu")
        App.get_running_app().play_sound()
        App.get_running_app().sm.current = 'menu'  # Change 'main' to the actual screen name for the menu
        print("Menu screen activated")

    def on_pre_enter(self):
        update_current_page('monitor')

    def update_language(self):
        """
        Update the language of the screen.
        :param language: The language to set. If None, it uses the current language from settings.
        """
        self.ip_label.text = f"{update_text_language('ip_address')}: {self.get_ip_address()}"
        

def get_ip_address():
    try:
        # Connect to an external server to force socket to use active network
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Google DNS
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception as e:
        return f"Not connected" 
