from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget  
from utils.icons import IconTextButton, CircularImageButton
from kivy.app import App
import os, sys
from utils.config_loader import load_config, save_config, update_current_page
from utils.layout import HeaderBar, SafeScreen

class PowerScreen(SafeScreen):
    """
    Power screen for the Soundeye application.
    This screen allows users to power off or restart the device.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        header = HeaderBar(title="Power", icon_path="images/home.png", button_text="Home", button_screen="menu")
        buttons = BoxLayout(orientation='horizontal', spacing=80, size_hint_y=0.3, pos_hint={'center_x': 0.5, 'center_y': 0.5}, padding=[80,0,80,0])  # Only left and right padding
        buttons.add_widget(Widget())
        buttons.add_widget(RebootButton(icon_path="images/reboot.png", text="Reboot", height=50))
        buttons.add_widget(ShutdownButton(icon_path="images/power.png", text="Shutdown", height=50))
        buttons.add_widget(Widget())
        self.add_widget(header)
        self.add_widget(buttons)

    def on_pre_enter(self):
        update_current_page('power')

class ShutdownButton(IconTextButton):
    """
    Shutdown button action.
    This method is called when the shutdown button is pressed.
    """
    def on_press(self):
        App.get_running_app().stop()  # Stop the application, simulating a shutdown action


class RebootButton(IconTextButton):
    """
    Reboot button action: restarts the current Python program.
    """
    def on_press(self):
        python = sys.executable
        os.execl(python, python, *sys.argv)