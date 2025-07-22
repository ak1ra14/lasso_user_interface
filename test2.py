from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.clock import Clock
from utils.config_loader import load_config
from utils.layout import HeaderBar

class MonitorScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        btn = Button(text="Go to Menu")
        btn.bind(on_press=self.go_to_menu)
        self.add_widget(btn)

    def go_to_menu(self, instance):
        print("Button clicked, going to Menu")
        Clock.schedule_once(lambda dt: setattr(self.manager, 'current', 'test'), 0)

class TestScreen(Screen):
    def __init__(self, **kwargs):
        super(TestScreen, self).__init__(**kwargs)
        self.config = load_config('config/V3.json')  # Read once
        self.location = self.config.get("location", "Room 101")
        volume = self.config.get("volume", 50)

        # Add header bar
        self.header = HeaderBar(title="Test Screen")
        self.add_widget(self.header)

class TestApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MonitorScreen(name='monitor'))
        sm.add_widget(TestScreen(name='test'))
        return sm

TestApp().run()