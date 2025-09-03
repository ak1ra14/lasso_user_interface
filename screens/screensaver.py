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
from utils.freeze_screen import freeze_ui
from kivy.uix.floatlayout import FloatLayout
import json
import os

from utils.config_loader import load_config, save_config, update_current_page, update_text_language
from utils.layout import HeaderBar, SafeScreen

class ScreenSaverScreen(SafeScreen):
    def __init__(self, **kwargs):
        
        super().__init__(**kwargs)
        self.screensaver_time = load_config('config/V3.json').get('screensaver', 60)
        self.header = HeaderBar(title="screensaver", icon_path="images/home.png", button_text="home", button_screen="menu2")
        buttons = BoxLayout(orientation='horizontal', spacing=15, size_hint_y=0.3, pos_hint={'center_x': 0.5, 'center_y': 0.5}, padding=[50,0,50,0])  # Only left and right padding
        float_layout = FloatLayout(
            size_hint=(1, 1))
        #time = BoxLayout(orientation='vertical', spacing=30, pos_hint={'center_x': 0.5, 'center_y': 0.5}, padding=[50,0,50,0])
        self.screensaver_time_label = (Label(
            text=f"{self.screensaver_time}",
            font_size=120,
            font_name='fonts/Roboto-Bold.ttf',
            size_hint_y=0.8,
            valign='middle',
            pos_hint={'center_x': 0.5, 'center_y': 0.52},
        ))
        float_layout.add_widget(self.screensaver_time_label)
        self.second = Label(
            text= update_text_language("second"),
            font_size=20,
            font_name='fonts/MPLUS1p-Regular.ttf',
            valign='bottom',
            pos_hint={'center_x': 0.5, 'center_y': 0.4},
        )
        float_layout.add_widget(self.second)

        buttons.add_widget(ChangeTime(icon_path="images/decrease_10.png",
                                        screensaver_time_label=self.screensaver_time_label,
                                        change="decrease",
                                        screensaver_screen=self,
                                        pos_hint={'center_x': 0.5, 'center_y': 0.5},
                                        by=10, height=50))
        buttons.add_widget(ChangeTime(icon_path="images/decrease.png",
                                        screensaver_time_label=self.screensaver_time_label,
                                        change="decrease",
                                        screensaver_screen=self,  # Pass the screen instance
                                        pos_hint={'center_x': 0.5, 'center_y': 0.5},
                                        by=1, height=50))
        screensaver = BoxLayout(orientation='vertical', spacing=30, size_hint_y=0.3, pos_hint={'center_x': 0.5, 'center_y': 0.5}, padding=[20,0,20,0])

        buttons.add_widget(screensaver)
        buttons.add_widget(ChangeTime(icon_path="images/increase.png",
                                        screensaver_time_label=self.screensaver_time_label,
                                        change="increase",  # Pass the label to update
                                        by=1,
                                        pos_hint={'center_x': 0.5, 'center_y': 0.5},
                                        screensaver_screen=self,  # Pass the screen instance
                                        height=50))
        buttons.add_widget(ChangeTime(icon_path="images/increase_10.png",
                                        screensaver_time_label=self.screensaver_time_label,
                                        change="increase",  # Pass the label to update
                                        screensaver_screen=self,  # Pass the screen instance
                                        pos_hint={'center_x': 0.5, 'center_y': 0.5},
                                        by=10, height=50))
        self.min_button = MinMaxButtonScreensaver(
            screensaver_screen=self,
            text=update_text_language("minimum"),
            size_hint=(None, None),
            size=(120, 40),
            pos_hint={'center_x': 0.1, 'center_y': 0.3}
        )
        float_layout.add_widget(self.min_button)
        self.max_button = MinMaxButtonScreensaver(
            screensaver_screen=self,
            text=update_text_language("maximum"),
            size_hint=(None, None),
            size=(120, 40),
            pos_hint={'center_x': 0.9, 'center_y': 0.3}
        )
        float_layout.add_widget(self.max_button)
        self.add_widget(self.header)
        self.add_widget(buttons)

        self.save_button = SaveButton(
            icon_path="images/save.png",
            screensaver_screen=self,  # Pass the screen instance
            text=update_text_language("save"),  
            size_hint=(None, None),
            size=(120, 120),
            pos_hint={'center_x': 0.5, 'center_y': 0.2}
        )
        self.add_widget(self.save_button)

        self.add_widget(float_layout)

    def on_pre_enter(self):
        """
        This method is called when the screen is about to be displayed.
        It updates the screensaver time label with the current value.
        """
        update_current_page('screensaver')
        self.screensaver_time = load_config('config/V3.json').get('screensaver', 60)
        self.screensaver_time_label.text = f"{self.screensaver_time}"

    def update_language(self):
        self.header.update_language()
        self.save_button.label.text = update_text_language("save")
        self.second.text = update_text_language("second")
        self.min_button.label.text = update_text_language("minimum")
        self.max_button.label.text = update_text_language("maximum")


class ChangeTime(IconTextButton):
    def __init__(self, by=1, screensaver_time_label=None, change="increase", screensaver_screen=None, size=(120, 120), **kwargs):
        super().__init__(**kwargs)
        self.size = size
        self.by = by
        self.screensaver_time_label = screensaver_time_label
        self.change = change
        self.screensaver_screen = screensaver_screen  # Reference to the screen
        self.sound = SoundLoader.load('sound/tap.wav')

    def on_press(self):
        super().on_press()
        freeze_ui(0.3)  # Freeze the UI for 0.3 seconds
        if self.change == "increase":
            self._increase()
        elif self.change == "decrease":
            self._decrease()
        print("Screensaver time changed by", self.by)

    def _increase(self):
        current_time = self.screensaver_screen.screensaver_time
        new_time = min(current_time + self.by, 600)
        self.screensaver_screen.screensaver_time = new_time
        self.screensaver_time_label.text = f"{new_time}"

    def _decrease(self):
        current_time = self.screensaver_screen.screensaver_time
        new_time = max(current_time - self.by, 0)
        self.screensaver_screen.screensaver_time = new_time
        self.screensaver_time_label.text = f"{new_time}"

class SaveButton(IconTextButton):
    def __init__(self, screensaver_screen=None, **kwargs):
        super().__init__(**kwargs)
        self.screensaver_screen = screensaver_screen

    def on_press(self):
        """
        Override the on_press method to save the current screensaver settings.
        This method is called when the save button is pressed.
        """
        # Save the current screensaver time to the config file
        super().on_press()
        App.get_running_app().show_saved_popup()  # Show a popup indicating the settings have been saved
        config = load_config('config/settings.json','v3_json')
        config['screensaver'] = self.screensaver_screen.screensaver_time
        save_config('config/settings.json', 'v3_json', data=config)
        print("Screensaver settings saved:", config['screensaver'])
        App.get_running_app().sm.current = 'menu2'
        App.get_running_app().reset_screensaver_timer()  # Reset screensaver timer

class HomeButtonScreensaver(IconTextButton):
    def __init__(self, screensaver_screen=None, **kwargs):
        super().__init__(**kwargs)
        self.screensaver_screen = screensaver_screen

    def on_press(self):
        super().on_press()
        App.get_running_app().play_sound()
        # Navigate back to the menu screen
        self.config = load_config('config/settings.json', 'v3_json')
        self.screensaver_screen.screensaver_time_label.text = f"{self.config.get('screensaver', 50)}s"
        self.screensaver_screen.screensaver_time = self.config.get('screensaver', 50)
          # Reset screensaver time to saved value

class MinMaxButtonScreensaver(IconTextButton):
    def __init__(self, screensaver_screen=None, **kwargs):
        super().__init__(**kwargs)
        self.screensaver_screen = screensaver_screen

    def on_press(self):
        super().on_press()
        # Set screensaver time to min or max value based on the button type
        if self.label.text == update_text_language("minimum"):
            self.screensaver_screen.screensaver_time = 0
        elif self.label.text == update_text_language("maximum"):
            self.screensaver_screen.screensaver_time = 600
        self.screensaver_screen.screensaver_time_label.text = f"{self.screensaver_screen.screensaver_time}"

class DarkScreen(SafeScreen):
    """
    A dark screen that can be used as a screensaver.
    This screen is displayed when the screensaver is active.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Button(
            background_color=(0, 0, 0, 1),  # Black background
            size_hint=(1, 1),  # Full screen
            on_press=self.stop_screensaver  # Stop screensaver on press
        ))
        # Clock.schedule_once(self.stop_screensaver, load_config('config/V3.json').get('screensaver', 60))

    def stop_screensaver(self, dt):
        App.get_running_app().sm.current = 'monitor'  # Navigate back to the menu screen after the timeout

    def on_pre_enter(self):
        update_current_page('dark_screen')
