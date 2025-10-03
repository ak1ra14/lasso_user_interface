from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.audio import SoundLoader
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.slider import Slider
from kivy.logger import Logger

from as_utils.as_keyboard import show_saved_popup
from as_utils.as_config_loader import load_config, save_config, update_current_page, update_text_language
from as_utils.as_layout import HeaderBar, SafeScreen
from as_utils.as_freeze_screen import freeze_ui
from as_utils.as_icons import IconTextButton


class ScreenSaverScreen(SafeScreen):
    def __init__(self, **kwargs):
        
        super().__init__(**kwargs)
        self.screensaver_time = load_config('as_config/V3.json').get('screensaver', 60)
        self.save_button = SaveButton(
            icon_path="as_images/save.png",
            screensaver_screen=self,  # Pass the screen instance
            text=update_text_language("save"),  
            size_hint=(None, None),
            size=(110, 110),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            button_mode='no_status'
        )
        self.header = HeaderBar(title="screensaver", icon_path="as_images/home.png", button_text="home", button_screen="menu2", second_button=self.save_button)
        buttons = BoxLayout(orientation='horizontal', spacing=15, size_hint_y=0.3, pos_hint={'center_x': 0.5, 'center_y': 0.50}, padding=[50,0,50,0])  # Only left and right padding
        float_layout = FloatLayout(
            size_hint=(1, 1))
        #time = BoxLayout(orientation='vertical', spacing=30, pos_hint={'center_x': 0.5, 'center_y': 0.5}, padding=[50,0,50,0])
        self.screensaver_time_label = (Label(
            text=f"{self.screensaver_time}",
            font_size=120,
            font_name='as_fonts/Roboto-Bold.ttf',
            size_hint_y=0.8,
            valign='middle',
            pos_hint={'center_x': 0.5, 'center_y': 0.52},
        ))
        float_layout.add_widget(self.screensaver_time_label)
        self.second = Label(
            text= update_text_language("second"),
            font_size=20,
            font_name='as_fonts/MPLUS1p-Regular.ttf',
            valign='bottom',
            pos_hint={'center_x': 0.5, 'center_y': 0.4},
        )
        float_layout.add_widget(self.second)

        buttons.add_widget(ChangeTime(icon_path="as_images/decrease_10.png",
                                        screensaver_time_label=self.screensaver_time_label,
                                        change="decrease",
                                        screensaver_screen=self,
                                        pos_hint={'center_x': 0.5, 'center_y': 0.5},
                                        by=10, height=50, button_mode='image_only'))
        buttons.add_widget(ChangeTime(icon_path="as_images/decrease.png",
                                        screensaver_time_label=self.screensaver_time_label,
                                        change="decrease",
                                        screensaver_screen=self,  # Pass the screen instance
                                        pos_hint={'center_x': 0.5, 'center_y': 0.5},
                                        by=1, height=50, button_mode='image_only'))
        screensaver = BoxLayout(orientation='vertical', spacing=30, size_hint_y=0.3, pos_hint={'center_x': 0.5, 'center_y': 0.5}, padding=[20,0,20,0])

        buttons.add_widget(screensaver)
        buttons.add_widget(ChangeTime(icon_path="as_images/increase.png",
                                        screensaver_time_label=self.screensaver_time_label,
                                        change="increase",  # Pass the label to update
                                        by=1,
                                        pos_hint={'center_x': 0.5, 'center_y': 0.5},
                                        screensaver_screen=self,  # Pass the screen instance
                                        height=50, button_mode='image_only'))
        buttons.add_widget(ChangeTime(icon_path="as_images/increase_10.png",
                                        screensaver_time_label=self.screensaver_time_label,
                                        change="increase",  # Pass the label to update
                                        screensaver_screen=self,  # Pass the screen instance
                                        pos_hint={'center_x': 0.5, 'center_y': 0.5},
                                        by=10, height=50, button_mode='image_only'))
        self.slider = Slider(min=0, max=600, value=0, step=1, size_hint_x=None, size_hint_y=None, width=900, pos_hint={'center_x': 0.5, 'center_y': 0.3})
        
        self.slider.bind(value=self.on_slider_value_change)
        self.slider.cursor_size = (40, 40)  # Adjust as needed
        float_layout.add_widget(self.slider)

        self.add_widget(self.header)
        self.add_widget(buttons)
        self.add_widget(float_layout)

    def on_pre_enter(self):
        """
        This method is called when the screen is about to be displayed.
        It updates the screensaver time label with the current value.
        """
        update_current_page('screensaver')
        self.screensaver_time = load_config('as_config/V3.json').get('screensaver', 60)
        self.screensaver_time_label.text = f"{self.screensaver_time}"
        self.slider.value = self.screensaver_time

    def update_language(self):
        self.header.update_language()
        self.save_button.label.text = update_text_language("save")
        self.second.text = update_text_language("second")
        # self.min_button.label.text = update_text_language("minimum")
        # self.max_button.label.text = update_text_language("maximum")

    def on_slider_value_change(self, instance, value):
        self.screensaver_time = int(value)
        self.screensaver_time_label.text = f"{int(value)}"


class ChangeTime(IconTextButton):
    def __init__(self, by=1, screensaver_time_label=None, change="increase", screensaver_screen=None, size=(120, 120), **kwargs):
        super().__init__(**kwargs)
        self.size = size
        self.by = by
        self.screensaver_time_label = screensaver_time_label
        self.change = change
        self.screensaver_screen = screensaver_screen  # Reference to the screen
    def on_press(self):
        super().on_press()
        freeze_ui(0.3)  # Freeze the UI for 0.3 seconds
        if self.change == "increase":
            self._increase()
        elif self.change == "decrease":
            self._decrease()

    def _increase(self):
        current_time = self.screensaver_screen.screensaver_time
        new_time = min(current_time + self.by, 600)
        self.screensaver_screen.screensaver_time = new_time
        self.screensaver_time_label.text = f"{new_time}"
        self.screensaver_screen.slider.value = new_time

    def _decrease(self):
        current_time = self.screensaver_screen.screensaver_time
        new_time = max(current_time - self.by, 0)
        self.screensaver_screen.screensaver_time = new_time
        self.screensaver_time_label.text = f"{new_time}"
        self.screensaver_screen.slider.value = new_time

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
        show_saved_popup('saved')  # Show a popup indicating the settings have been saved
        config = load_config('as_config/settings.json','v3_json')
        config['screensaver'] = self.screensaver_screen.screensaver_time
        save_config('as_config/settings.json', 'v3_json', data=config)
        #print("Screensaver settings saved:", config['screensaver'])
        App.get_running_app().sm.current = 'menu2'
        App.get_running_app().reset_screensaver_timer()  # Reset screensaver timer

class HomeButtonScreensaver(IconTextButton):
    def __init__(self, screensaver_screen=None, **kwargs):
        super().__init__(**kwargs)
        self.screensaver_screen = screensaver_screen
        self.button_mode = 'no_status'

    def on_press(self):
        super().on_press()
        App.get_running_app().sound_manager.play_tap()
        # Navigate back to the menu screen
        self.config = load_config('as_config/settings.json', 'v3_json')
        self.screensaver_screen.screensaver_time_label.text = f"{self.config.get('screensaver', 50)}s"
        self.screensaver_screen.screensaver_time = self.config.get('screensaver', 50)
          # Reset screensaver time to saved value

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
