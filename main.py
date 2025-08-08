import os, sys
#os.environ["KIVY_AUDIO"] = "pygame"

from kivy.config import Config
if sys.platform.startswith('linux'):
    Config.set('input', 'mouse', 'mouse,disable')
    Config.set('graphics', 'show_cursor', 0) 

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.core.window import Window
from utils.config_loader import load_config
from kivy.clock import Clock
from kivy.uix.progressbar import ProgressBar
from kivy.uix.floatlayout import FloatLayout

import sys
import socket
from screens.home_screen import MenuScreen1, MenuScreen2
from screens.language import LanguageScreen
from screens.monitor import MonitorScreen
from screens.power import PowerScreen
from screens.screensaver import ScreenSaverScreen, DarkScreen
from screens.timezone import TimezoneScreen
from screens.volume import VolumeScreen, set_system_volume
from screens.alert_mode import AlertModeScreen
from screens.alert_type import AlertTypeScreen
from screens.location import LocationScreen, Bed1Screen, Bed2Screen, DeviceKeyboardScreen
from screens.server import ServerScreen, MQTTTopicKeyboardScreen, RegionServerScreen, MQTTBrokerIPScreen, AlertLight1Screen, AlertLight2Screen
from utils.num_pad import NumberPadScreen
from screens.wifi import WifiLoadingScreen, WifiPasswordScreen, WifiConnectingScreen, WifiConnectedScreen, WifiErrorScreen
from kivy.core.audio import SoundLoader

class MyApp(App):
    def build(self):
        self.sm = ScreenManager(transition=NoTransition())
        self.sound = SoundLoader.load('sound/tap.mp3')  # Load sound once
        self.en_dictionary = load_config('languages/en.json')
        self.jp_dictionary = load_config('languages/jp.json')
        # Set the default volume to config setting
        self.config = load_config('config/settings.json','v3_json')
        self.language = self.config.get('language', 'en')
        set_system_volume(self.config.get('volume', 50))
        self.sm.add_widget(MonitorScreen(name='monitor'))
        self.sm.add_widget(MenuScreen1(name='menu'))
        self.sm.add_widget(MenuScreen2(name='menu2'))
        self.sm.add_widget(LanguageScreen(name='language'))
        self.sm.add_widget(PowerScreen(name='power'))
        self.sm.add_widget(ScreenSaverScreen(name='screensaver'))       
        self.sm.add_widget(TimezoneScreen(name='timezone'))
        self.sm.add_widget(VolumeScreen(name='volume'))
        self.sm.add_widget(AlertModeScreen(name='mode'))
        self.sm.add_widget(AlertTypeScreen(name='alerts'))
        self.sm.add_widget(LocationScreen(name='location'))
        self.sm.add_widget(Bed1Screen(name='bed1'))
        self.sm.add_widget(Bed2Screen(name='bed2'))
        self.sm.add_widget(DeviceKeyboardScreen(name='device'))
        self.sm.add_widget(ServerScreen(name='servers'))
        self.sm.add_widget(RegionServerScreen(name='region server'))
        self.sm.add_widget(MQTTBrokerIPScreen(name='mqtt broker ip'))
        self.sm.add_widget(AlertLight1Screen(name='alert lights 1'))
        self.sm.add_widget(AlertLight2Screen(name='alert lights 2'))
        self.sm.add_widget(MQTTTopicKeyboardScreen(name='mqtt topic'))
        self.sm.add_widget(WifiLoadingScreen(name='wi-fi'))
        self.sm.add_widget(WifiPasswordScreen(name='wifi password'))
        self.sm.add_widget(WifiConnectingScreen(name='wifi connecting'))
        self.sm.add_widget(WifiConnectedScreen(name='wifi connected'))
        self.sm.add_widget(WifiErrorScreen(name='wifi error'))

        # Add the dark screen for screensaver
        self.sm.add_widget(DarkScreen(name='dark'))
        self.sm.bind(current=self.on_screen_change)

        self.sm.current = 'monitor'
        # Set the initial screen to menu

        # Create a FloatLayout to overlay the time bar
        self.root_layout = FloatLayout()
        self.root_layout.add_widget(self.sm)

        # Create the time bar
        self.time_limit = 60
        self.time_left = self.time_limit
        self.time_bar = ProgressBar(max=self.time_limit, value=self.time_limit, size_hint=(0.94, None), height=20, pos_hint={'x': 0.03, 'y': 0.02})
        self.time_bar.opacity = 0
        self.root_layout.add_widget(self.time_bar)

        # Start timer
        self._timer_event = Clock.schedule_interval(self._update_time_bar, 1)
        self.screensaver_event = None
        self.reset_screensaver_timer()
        Window.bind(on_touch_down=self.on_user_activity)
        Window.bind(on_key_down=self.on_user_activity)

        return self.root_layout
    
    def play_sound(self):
        if self.sound:
            self.sound.stop()  # Stop if already playing
            self.sound.play()
        else:
            print("Sound file not found or unsupported format.")
    
    def on_user_activity(self, *args):
        self.reset_screensaver_timer()
        self.reset_timer()
    
    def reset_screensaver_timer(self, *args):
        if self.screensaver_event:
            self.screensaver_event.cancel()
        timeout = self.config.get('screensaver', 60)
        self.screensaver_event = Clock.schedule_once(self.activate_screensaver, timeout)

    def activate_screensaver(self, *args):
        if self.sm.current != 'dark':
            self.sm.current = 'dark'

    def _update_time_bar(self, dt):
        self.time_left -= 1
        self.time_bar.value = self.time_left
        if self.time_left <= 0:
            self._timer_event.cancel()
            if self.sm.current != 'dark':
                self.sm.current = 'monitor'  # Switch to dark screen when time runs out
            else:
                return  # Switch to monitor screen

    def reset_timer(self, *args):
        self.time_left = self.time_limit
        self.time_bar.value = self.time_limit

    def on_screen_change(self, *args):
        if self.sm.current == 'dark' or self.sm.current == 'monitor':
            self.time_bar.opacity = 0  # Hide time bar in dark screen
            if self.sm.current == 'monitor':
                self.reset_timer_event()
        else:
            self.time_bar.opacity = 1


    def reset_timer_event(self):
        if self._timer_event:
            self._timer_event.cancel()
        self.time_left = self.time_limit
        self.time_bar.value = self.time_limit
        self._timer_event = Clock.schedule_interval(self._update_time_bar, 1)

if __name__ == '__main__':
    Window.size = (1024, 600)  # Set the window size to 1024x600 pixels
    if not (sys.platform.startswith('win') or sys.platform == 'darwin'):
        Window.fullscreen = 'auto'  # Enable full screen mode
    MyApp().run()