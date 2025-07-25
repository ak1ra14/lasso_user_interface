from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget  
from utils.icons import IconTextButton
from kivy.uix.image import Image
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.app import App
import json
import os

from utils.config_loader import load_config
from utils.layout import HeaderBar


class VolumeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.volume = load_config('config/V3.json').get('volume', 50)
        header = HeaderBar(title="Volume", icon_path="images/home.png", button_text="Home", button_screen="menu")
        buttons = BoxLayout(orientation='horizontal', spacing=15, size_hint_y=0.3, pos_hint={'center_x': 0.5, 'center_y': 0.5}, padding=[50,0,50,0])  # Only left and right padding

        self.volume_label = (Label(
            text=f"{self.volume}%",
            font_size=110,
            font_name='fonts/Roboto-Bold.ttf',
            size_hint_y=0.9,
        ))

        buttons.add_widget(ChangeVolume(icon_path="images/decrease_10.png",
                                        volume_label=self.volume_label,
                                        change="decrease",
                                        volume_screen=self,
                                        pos_hint={'center_x': 0.5, 'center_y': 0.5},
                                        by=10, height=50))
        buttons.add_widget(ChangeVolume(icon_path="images/decrease.png",
                                        volume_label=self.volume_label,
                                        change="decrease",
                                        volume_screen=self,  # Pass the screen instance
                                        pos_hint={'center_x': 0.5, 'center_y': 0.5},
                                        by=1, height=50))
        volume = BoxLayout(orientation='vertical', spacing=30, size_hint_y=0.3, pos_hint={'center_x': 0.5, 'center_y': 0.5}, padding=[20,0,20,0])

        volume.add_widget(self.volume_label)

        buttons.add_widget(volume)
        buttons.add_widget(ChangeVolume(icon_path="images/increase.png", 
                                        volume_label=self.volume_label, 
                                         change = "increase", # Pass the label to update
                                          pos_hint={'center_x': 0.5, 'center_y': 0.5},
                                          by=1,
                                        volume_screen=self,  # Pass the screen instance   
                                         height=50))
        buttons.add_widget(ChangeVolume(icon_path="images/increase_10.png", 
                                        volume_label=self.volume_label, 
                                         change = "increase", # Pass the label to update
                                         volume_screen=self,  # Pass the screen instance
                                        pos_hint={'center_x': 0.5, 'center_y': 0.5},
                                          by=10, height=50))
        self.add_widget(header)
        self.add_widget(buttons)
        save_anchor = AnchorLayout(
            anchor_x='center',
            anchor_y='bottom',
            size_hint=(1, None),
            height=120,
            padding=[0, 20, 0, 40]  # Padding for the anchor layout
        )
        save_anchor.add_widget(SaveButton(
            icon_path="images/save.png",
            volume_screen = self,  # Pass the screen instance
            text="Save",
            size_hint=(None, None),
            size=(120, 120)
        ))

        self.add_widget(save_anchor)

    def on_pre_enter(self):
        self.volume = load_config('config/V3.json').get('volume', 50)
        self.volume_label.text = f"{self.volume}%"


class ChangeVolume(IconTextButton):
    def __init__(self, by=1, volume_label=None, change="increase", volume_screen=None, **kwargs):
        super().__init__(**kwargs)
        self.size = (120, 120)  # Set the size of the button
        self.by = by
        self.volume_label = volume_label
        self.change = change
        self.volume_screen = volume_screen  # Reference to the screen
        self.sound = SoundLoader.load('sound/beep.wav')

    def on_press(self):
        if self.change == "increase":
            self._increase()
        elif self.change == "decrease":
            self._decrease()
        print("Volume changed by", self.by)


    def _increase(self):
        current_volume = self.volume_screen.volume
        new_volume = min(current_volume + self.by, 100)
        self.volume_screen.volume = new_volume
        self.volume_label.text = f"{new_volume}%"
        set_system_volume(new_volume)
        if self.sound:
            self.sound.play()


    def _decrease(self):
        current_volume = self.volume_screen.volume
        new_volume = max(current_volume - self.by, 0)
        self.volume_screen.volume = new_volume
        self.volume_label.text = f"{new_volume}%"
        set_system_volume(new_volume)
        if self.sound:
            self.sound.play()

class SaveButton(IconTextButton):
    def __init__(self, volume_screen=None, **kwargs):
        super().__init__(**kwargs)
        self.volume_screen = volume_screen

    def on_press(self):
        """
        Override the on_press method to save the current volume settings.
        This method is called when the save button is pressed.
        """
        # Save the current volume to the config file
        config = load_config('config/V3.json')
        config['volume'] = self.volume_screen.volume
        with open('config/V3.json', 'w') as f:
            json.dump(config, f, indent=4)
        print("Volume settings saved:", config['volume'])
        App.get_running_app().sm.current = 'menu'  # Navigate back to the menu screen

class HomeButtonVolume(IconTextButton):
    def __init__(self, volume_screen=None, **kwargs):
        super().__init__(**kwargs)
        self.volume_screen = volume_screen

    def on_press(self):
        super().on_press()
        # sound = SoundLoader.load('sound/tap.mp3')
        # sound.play()
        # self.volume_screen.volume_label.text = f"{load_config('config/V3.json').get('volume', 50)}%"
        # self.volume_screen.volume = load_config('config/V3.json').get('volume', 50)
          # Reset volume to saved value

    #raspberry pi
# def set_system_volume(percent):
#     # Clamp percent between 0 and 100
#     percent = max(0, min(100, percent))
#     os.system(f"amixer sset 'Master' {percent}%")

#macOS
def set_system_volume(percent):
    percent = max(0, min(100, percent))
    os.system(f"osascript -e 'set volume output volume {percent}'")