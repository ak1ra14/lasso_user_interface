from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from utils.config_loader import load_config
from utils.icons import IconTextButton
from kivy.graphics import Color, RoundedRectangle, Line
from utils.keyboard import SeparatorLine

class NumberPadScreen(Screen):
    def __init__(self, title = 'Custom Numpad', **kwargs):
        super(NumberPadScreen,self).__init__(**kwargs)
        # === Left side ===
        self.title = title
        left = BoxLayout(orientation='vertical', spacing=5, pos_hint={'x':0.2, 'y':0.10}, size_hint=(0.6, 0.8))

        # IP Input Header
        self.label = Label(text=self.title, markup=True, font_size=50,
                           font_family='fonts/Roboto-Bold.ttf',
                           size_hint_y=None, height=50, halign='left')
        self.label.bind(size=self.label.setter('text_size'))
        left.add_widget(self.label)
        self.ip_input = TextInput(text='192.168.0.171', multiline=False, font_size=40,
                                  background_color=(0, 0, 0, 0),
                                  foreground_color=(1, 1, 0, 1),  # Yellow
                                  cursor_color=(1, 1, 1, 1),
                                  font_family='fonts/Roboto-Bold.ttf',
                                  size_hint_y=None, height=60,
                                  halign='left')
        self.ip_input.bind(focus=self.set_cursor_at_end)
        left.add_widget(self.ip_input)
        left.add_widget(Widget(size_hint_y=None, height=2))  # Fake underline

        # Keypad Grid
        keypad = GridLayout(cols=3, spacing=15, size_hint_y=None)
        keypad.bind(minimum_height=keypad.setter('height'))

        keys = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'DEL', '0', '.']
        for key in keys:
            btn = RoundedButton(
                text=key, font_size=40, size_hint=(None, None), height=80, width = 120,
                background_color=(0.2, 0.2, 0.2, 1), color=(1, 1, 1, 1), radius=20
            )
            btn.bind(on_press=self.on_key_press)
            keypad.add_widget(btn)
        left.add_widget(keypad)

        self.add_widget(left)

        #text input line


        # === Right side (action buttons) ===
        right = FloatLayout(size_hint=(1,1))
        right.add_widget(IconTextButton(text="Home", font_size=18,
                                        icon_path="images/home.png",
                                        screen_name="menu",
                                size_hint=(None, None), size = (120,120),
                                pos_hint = None,
                                pos = (875,450)
                             ))
        right.add_widget(IconTextButton(text="Save", font_size=18,
                                icon_path="images/save.png",
                                on_press = self.on_save,
                                size_hint=(None, None), size=(120, 120),
                                 pos=(720, 200)))
        right.bind(pos=self.setter('pos'))
        right.bind(size=self.setter('size'))
        right.add_widget(Widget())  # Spacer
        self.add_widget(right)
        partition = SeparatorLine(
            size_hint=(0.35, 0.05),
            pos  = (207,428),
        )
        self.add_widget(partition)
        
    def on_save(self, instance):
        pass

    def set_cursor_at_end(self, instance, value):
        if value:  # If focused
            instance.cursor = (len(instance.text), 0)

    def on_key_press(self, instance):
        key = instance.text
        if key == 'DEL':
            self.ip_input.text = self.ip_input.text[:-1]
        else:
            self.ip_input.text += key


class RoundedButton(Button):
    def __init__(self, radius=20, **kwargs):
        super().__init__(**kwargs)
        self.radius = radius
        self.background_normal = ''  # Remove default background
        self.background_color = (0, 0, 0, 0)  # Make background transparent
        with self.canvas.before:
            self.bg_color = Color(0.3, 0.3, 0.3, 1)  # grey color
            self.bg_rect = RoundedRectangle(
                pos=self.pos, size=self.size, radius=[self.radius]
            )
        self.bind(pos=self.update_bg, size=self.update_bg, background_color=self.update_color)

    def update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def update_color(self, *args):
        self.bg_color.rgba = self.background_color

