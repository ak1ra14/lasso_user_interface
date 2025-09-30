from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from utils.as_icons import IconTextButton
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from utils.as_freeze_screen import freeze_ui
import os, sys, subprocess
from kivy.uix.slider import Slider
from kivy.clock import Clock
from utils.as_config_loader import load_config, save_config, update_current_page, update_text_language, save_config_partial
from utils.as_layout import HeaderBar, SafeScreen
from utils.as_keyboard import show_saved_popup
from kivy.logger import Logger


class VolumeScreen(SafeScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.volume = load_config('config/settings.json', 'v3_json').get('volume', 50)
        self.save_button = SaveButton(
            icon_path="images/save.png",
            volume_screen=self,
            text=update_text_language("save"),  
            size_hint=(None, None),
            size=(110, 110),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.header = HeaderBar(title='volume', icon_path="images/home.png", button_text="home", button_screen="menu", second_button=self.save_button)
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
        self.slider = Slider(min=0, max=100, value=0, step=1, size_hint_x=None, size_hint_y=None, width=900, pos_hint={'center_x': 0.5, 'center_y': 0.3})
        self.slider.bind(value=self.on_slider_value_change)
        self.add_widget(self.slider)
        self.add_widget(self.header)
        self.add_widget(buttons)
        float_layout = FloatLayout(size_hint=(1, 1))
        self.add_widget(float_layout)


    def on_pre_enter(self):
        update_current_page('volume')
        self.volume = load_config('config/settings.json', 'v3_json').get('volume', 50)
        self.volume_label.text = f"{self.volume}%"
        self.header.update_language()
        self.save_button.label.text = update_text_language('save')
        self.slider.value = self.volume

    def on_slider_value_change(self, instance, value):
        self.volume = int(value)
        self.volume_label.text = f"{int(value)}%"

class ChangeVolume(IconTextButton):
    def __init__(self, by=1, volume_label=None, change="increase", volume_screen=None, **kwargs):
        super().__init__(**kwargs)
        self.size = (120, 120)  # Set the size of the button
        self.by = by
        self.volume_label = volume_label
        self.change = change
        self.volume_screen = volume_screen  # Reference to the screen

    def on_press(self):
        super().on_press()
        freeze_ui(0.3)  # Freeze the UI for 0.3 seconds
        if self.change == "increase":
            self._increase()
        elif self.change == "decrease":
            self._decrease()

    def _increase(self):
        current_volume = self.volume_screen.volume
        new_volume = min(current_volume + self.by, 100)
        self.volume_screen.volume = new_volume
        self.volume_label.text = f"{new_volume}%"
        self.volume_screen.slider.value =  new_volume
        set_system_volume(new_volume)

    def _decrease(self):
        current_volume = self.volume_screen.volume
        new_volume = max(current_volume - self.by, 0)
        self.volume_screen.volume = new_volume
        self.volume_label.text = f"{new_volume}%"
        self.volume_screen.slider.value = new_volume
        set_system_volume(new_volume)


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

        self.color_instruction.rgba = (0.2, 0.8, 0.2, 1) # Change color to green on press
        Clock.schedule_once(self._reset_color, 0.3)  # Reset color after 0.3 seconds
        freeze_ui(0.3)
        set_system_volume(self.volume_screen.volume)
        App.get_running_app().sound_manager.play_alert()

        show_saved_popup(update_text_language('saved'))  # Show a popup indicating the settings have been saved
        save_config_partial("config/settings.json", "v3_json", key = 'volume', value=self.volume_screen.volume)
        App.get_running_app().sm.current = 'menu'  # Navigate back to the menu screen

class HomeButtonVolume(IconTextButton):
    def __init__(self, volume_screen=None, **kwargs):
        super().__init__(**kwargs)
        self.volume_screen = volume_screen

def set_system_volume(percent):
    if sys.platform == 'linux':
        set_system_volume_linux(percent)
    elif sys.platform == 'darwin':  # macOS
        set_system_volume_mac(percent)

    #raspberry pi
def set_system_volume_linux(percent):
    # Clamp percent between 0 and 100
    percentage = os.popen('amixer get PCM | grep "Front Left: Playback" | ' + "awk '{print $5}'").read()
    volume_value = str(percentage).strip("b'[]\n").strip('%')
    Logger.info(f"Previous volume: {volume_value}, New volume set to {percent}")
    subprocess.Popen(['amixer', 'sset', 'Master', 'playback', f'{percent}%'], stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)

#macOS
def set_system_volume_mac(percent):
    percent = max(0, min(100, percent))
    os.system(f"osascript -e 'set volume output volume {percent}'")