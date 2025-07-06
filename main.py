from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window


import socket
from screens.home_screen import MenuScreen1, MenuScreen2
from screens.language import LanguageScreen
from screens.monitor import MonitorScreen
from screens.power import PowerScreen
from screens.screensaver import ScreenSaverScreen
from screens.timezone import TimezoneScreen

class MyApp(App):
    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(MonitorScreen(name='monitor'))
        self.sm.add_widget(MenuScreen1(name='menu'))
        self.sm.add_widget(MenuScreen2(name='menu2'))
        self.sm.add_widget(LanguageScreen(name='language'))
        self.sm.add_widget(PowerScreen(name='power'))
        self.sm.add_widget(ScreenSaverScreen(name='screensaver'))
        self.sm.add_widget(TimezoneScreen(name='time zone'))
        self.sm.current = 'menu'  # Set the initial screen to timezone
        # self.page_indicator = PageIndicator(num_pages=2) 
        return self.sm

if __name__ == '__main__':
    Window.size = (1024, 600)  # Set the window size to 1024x600 pixels
    MyApp().run()