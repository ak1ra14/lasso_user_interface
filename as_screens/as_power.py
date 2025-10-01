from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget  
from kivy.app import App
import os, sys
from as_utils.as_config_loader import load_config, save_config, update_current_page, update_text_language
from as_utils.as_layout import HeaderBar, SafeScreen
from as_utils.as_icons import IconTextButton, CircularImageButton


class PowerScreen(SafeScreen):
    """
    Power screen for the Soundeye application.
    This screen allows users to power off or restart the device.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.header = HeaderBar(title="power", icon_path="as_images/home.png", button_text="home", button_screen="menu")
        buttons = BoxLayout(orientation='horizontal', spacing=80, size_hint_y=0.3, pos_hint={'center_x': 0.5, 'center_y': 0.5}, padding=[80,0,80,0])  # Only left and right padding
        buttons.add_widget(Widget())
        self.reboot_button = RebootButton(icon_path="as_images/reboot.png", text=update_text_language("reboot"), height=50)
        buttons.add_widget(self.reboot_button)
        self.shutdown_button = ShutdownButton(icon_path="as_images/power.png", text=update_text_language("shutdown"), height=50)
        buttons.add_widget(self.shutdown_button)
        buttons.add_widget(Widget())
        self.add_widget(self.header)
        self.add_widget(buttons)

    def on_pre_enter(self):
        update_current_page('power')
        self.header.update_language()

    def update_language(self):
        """
        Update the language of the screen.
        :param language: The language to set. If None, it uses the current language from settings.
        """
        self.reboot_button.label.text = update_text_language("reboot")
        self.shutdown_button.label.text = update_text_language("shutdown")

class ShutdownButton(IconTextButton):
    """
    Shutdown button action.
    This method is called when the shutdown button is pressed.
    """
    def on_press(self):
        import subprocess
        try:
            # Attempt to shutdown the device (Linux, Raspberry Pi, etc.)
            subprocess.run(['sudo', 'shutdown', '-h', 'now'])
        except Exception as e:
            print(f"Shutdown failed: {e}")


class RebootButton(IconTextButton):
    """
    Reboot button action: restarts the current Python program.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(on_press=self.on_press)

    def on_press(self, instance):
        import subprocess
        try:
            # Attempt to reboot the device (Linux, Raspberry Pi, etc.)
            subprocess.run(['sudo', 'reboot'])
        except Exception as e:
            print(f"Reboot failed: {e}")

    