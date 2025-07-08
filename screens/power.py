from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget  
from utils.icons import IconTextButton, CircularImageButton
from kivy.app import App
import os, sys

class PowerScreen(Screen):
    """
    Power screen for the Soundeye application.
    This screen allows users to power off or restart the device.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        header= BoxLayout(orientation='horizontal', pos_hint={'top': 1}, size_hint_y=0.25, padding=[50, 40, 50, 0], spacing=10)
        header.add_widget(Label(
            text="Power",
            font_size=60,
            font_name='fonts/Roboto-Bold.ttf',
            pos_hint={'left': 1, 'top': 1},
        ))
        header.add_widget(Widget())  # Spacer
        header.add_widget(IconTextButton(
            icon_path="images/home.png",
            text="Home",
            size_hint_y=None,
            height=50,
            screen_name='menu',  # Navigate to menu screen
        ))
        buttons = BoxLayout(orientation='horizontal', spacing=80, size_hint_y=0.3, pos_hint={'center_x': 0.5, 'center_y': 0.5}, padding=[80,0,80,0])  # Only left and right padding
        buttons.add_widget(Widget())
        buttons.add_widget(RebootButton(icon_path="images/reboot.png", text="Reboot", height=50))
        buttons.add_widget(ShutdownButton(icon_path="images/power.png", text="Shutdown", height=50))
        buttons.add_widget(Widget())
        self.add_widget(header)
        self.add_widget(buttons)

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