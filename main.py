import os
os.environ["KIVY_AUDIO"] = "pygame"

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.core.window import Window
from utils.config_loader import load_config
from kivy.clock import Clock


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

class MyApp(App):
    def build(self):
        self.sm = ScreenManager(transition=NoTransition())
        # Set the default volume to config setting
        self.config = load_config('config/V3.json')
        set_system_volume(self.config.get('volume', 50))
        self.sm.add_widget(MonitorScreen(name='monitor'))
        self.sm.add_widget(MenuScreen1(name='menu'))
        self.sm.add_widget(MenuScreen2(name='menu2'))
        self.sm.add_widget(LanguageScreen(name='language'))
        self.sm.add_widget(PowerScreen(name='power'))
        self.sm.add_widget(ScreenSaverScreen(name='screensaver'))       
        self.sm.add_widget(TimezoneScreen(name='time zone'))
        self.sm.add_widget(VolumeScreen(name='volume'))
        self.sm.add_widget(AlertModeScreen(name='mode'))
        self.sm.add_widget(AlertTypeScreen(name='alerts'))
        # Add the dark screen for screensaver
        self.sm.add_widget(DarkScreen(name='dark'))

        self.sm.current = 'monitor'
        # Set the initial screen to menu

        self.screensaver_event = None
        self.reset_screensaver_timer()
        Window.bind(on_touch_down=self.on_user_activity)
        Window.bind(on_key_down=self.on_user_activity)

        # self.page_indicator = PageIndicator(num_pages=2)
        return self.sm

    def reset_screensaver_timer(self, *args):
        if self.screensaver_event:
            self.screensaver_event.cancel()
        timeout = self.config.get('screensaver', 60)
        self.screensaver_event = Clock.schedule_once(self.activate_screensaver, timeout)

    def on_user_activity(self, *args):
        self.reset_screensaver_timer()

    def activate_screensaver(self, *args):
        if self.sm.current != 'dark':
            self.sm.current = 'dark'


if __name__ == '__main__':
    Window.size = (1024, 600)  # Set the window size to 1024x600 pixels
    MyApp().run()