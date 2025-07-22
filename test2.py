from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.clock import Clock

class MonitorScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        btn = Button(text="Go to Menu")
        btn.bind(on_press=self.go_to_menu)
        self.add_widget(btn)

    def go_to_menu(self, instance):
        print("Button clicked, going to Menu")
        Clock.schedule_once(lambda dt: setattr(self.manager, 'current', 'menu'), 0)

class MenuScreen(Screen):
    def on_enter(self):
        print("MenuScreen entered")

class TestApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MonitorScreen(name='monitor'))
        sm.add_widget(MenuScreen(name='menu'))
        return sm

TestApp().run()