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
        set_system_volume(load_config('config/V3.json').get('volume', 50))
        self.sm.add_widget(MonitorScreen(name='monitor'))
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
        timeout = load_config('config/V3.json').get('screensaver', 60)
        self.screensaver_event = Clock.schedule_once(self.activate_screensaver, timeout)

    def on_user_activity(self, *args):
        self.reset_screensaver_timer()

    def activate_screensaver(self, *args):
        if self.sm.current != 'dark':
            self.sm.current = 'dark'
            
    def on_icon_click(self, screen_name):
        app = App.get_running_app()
        if not app.sm.has_screen(screen_name):
            # Instantiate and add the screen only when needed
            if screen_name == 'menu':
                app.sm.add_widget(MenuScreen1(name='menu')) 
            elif screen_name == 'menu2':
                app.sm.add_widget(MenuScreen2(name='menu2'))
            elif screen_name == 'language':
                app.sm.add_widget(LanguageScreen(name='language'))
            elif screen_name == 'power':
                app.sm.add_widget(PowerScreen(name='power'))
            elif screen_name == 'screensaver':
                app.sm.add_widget(ScreenSaverScreen(name='screensaver'))
            elif screen_name == 'time zone':
                app.sm.add_widget(TimezoneScreen(name='time zone'))
            elif screen_name == 'volume':
                app.sm.add_widget(VolumeScreen(name='volume'))
            elif screen_name == 'mode':
                app.sm.add_widget(AlertModeScreen(name='mode'))
            elif screen_name == 'alerts':
                app.sm.add_widget(AlertTypeScreen(name='alerts'))  

       
        app.sm.current = screen_name


if __name__ == '__main__':
    Window.size = (1024, 600)  # Set the window size to 1024x600 pixels
    MyApp().run()