from kivy.config import Config
Config.set('input', 'mouse', 'mouse,disable')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle, Ellipse
from kivy.properties import BooleanProperty
from utils.keyboard import QwertyKeyboard
from kivy.core.window import Window


# class CustomSwitch(FloatLayout):
#     active = BooleanProperty(False)

#     def __init__(self, size=(120, 40), **kwargs):
#         super().__init__(**kwargs)
#         self.size_hint = (None, None)
#         self.size = size

#         with self.canvas:
#             self.bg_color = Color(0.15, 0.55, 0.75, 1)
#             self.bg = RoundedRectangle(pos=self.pos, size=self.size, radius=[min(self.size)//2])
#             self.thumb_color = Color(0, 0, 0, 1)
#             self.thumb = Ellipse(pos=(self.x + 2, self.y + 2), size=(self.size[1] - 4, self.size[1] - 4))

#         self.bind(pos=self.update_graphics, size=self.update_graphics)
#         self.bind(active=self.update_graphics)
#         self.bind(on_touch_down=self.toggle)

#     def update_graphics(self, *args):
#         self.bg.pos = self.pos
#         self.bg.size = self.size

#         # Move thumb left or right
#         thumb_size = self.size[1] - 4
#         if self.active:
#             self.thumb.pos = (self.x + self.width - thumb_size - 2, self.y + 2)
#         else:
#             self.thumb.pos = (self.x + 2, self.y + 2)
#         self.thumb.size = (thumb_size, thumb_size)

#     def toggle(self, instance, touch):
#         if self.collide_point(*touch.pos):
#             self.active = not self.active
#             return True
#         return False


class CustomSwitch(FloatLayout):
    active = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (120, 40)

        with self.canvas:
            self.bg_color = Color(0.15, 0.55, 0.75, 1)
            self.bg = RoundedRectangle(pos=self.pos, size=self.size, radius=[20])
            self.thumb_color = Color(0, 0, 0, 1)
            self.thumb = Ellipse(pos=(self.x + 2, self.y + 2), size=(36, 36))

        self.bind(pos=self.update_graphics, size=self.update_graphics)
        self.bind(active=self.update_graphics)

        self.bind(on_touch_down=self.toggle)

    def update_graphics(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size

        # Move thumb left or right
        if self.active:
            self.thumb.pos = (self.x + self.width - 38, self.y + 2)
        else:
            self.thumb.pos = (self.x + 2, self.y + 2)

    def toggle(self, instance, touch):
        if self.collide_point(*touch.pos):
            self.active = not self.active
            return True
        return False


class ToggleButton(BoxLayout):
    def __init__(self, text_left, text_right, **kwargs):
        super().__init__(orientation='horizontal', spacing=10, padding=10, **kwargs)
        self.size_hint = (None, None)
        self.size = (300, 60)

        self.one_label = Label(text = text_left, color=(1, 1, 1, 1), 
                               size_hint=(None, None), size=(100, 40),
                               font_size=20,
                               font_name='fonts/Roboto-Bold.ttf',
                               halign='right', valign='middle',)
        self.switch = CustomSwitch()
        self.two_label = Label(text=text_right, color=(1, 1, 1, 1), size_hint=(None, None), size=(100, 40),
                               font_name='fonts/Roboto-Bold.ttf',
                                 font_size=20,
                               halign='left', valign='middle',)

        self.add_widget(self.one_label)
        self.add_widget(self.switch)
        self.add_widget(self.two_label)

class MyApp(App):
    def build(self):
        return QwertyKeyboard(title="Custom QWERTY Keyboard")  # Initialize the keyboard with a title


if __name__ == '__main__':
    Window.size = (1024, 600)  # Set the window size to 1024x600 pixels
    MyApp().run()
    # from utils.config_loader import load_config, save_config
    # def has_any_alert():
    #     bed_alerts = load_config("config/bed.json").get("alert_checking", [])
    #     fall_alerts = load_config("config/fall.json").get("alert_checking", [])

    #     bed_has_alert = any(isinstance(item, list) and len(item) > 0 and item[0] == 1 for item in bed_alerts)
    #     fall_has_alert = any(isinstance(item, list) and len(item) > 0 and item[0] == 1 for item in fall_alerts)

    #     if bed_has_alert and fall_has_alert:
    #         return "Bed Exit & Fall"
    #     elif bed_has_alert:
    #         return "Bed Exit"
    #     elif fall_has_alert:
    #         return "Fall"
    #     else:
    #         return "No Alerts"
    # print("Active Alerts:", has_any_alert())
    
