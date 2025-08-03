from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line
from utils.icons import IconTextButton, PageIndicator, CircularImageButton, PageIndicatorWidget
from kivy.uix.anchorlayout import AnchorLayout
from utils.config_loader import load_config
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window

class HeaderBar(BoxLayout):
    def __init__(self, title="Language", icon_path="images/home.png", button_text="Home", button_screen="menu", padding=[50, 0, 50, 0], spacing=10, **kwargs):
        super().__init__(orientation='horizontal', size_hint_y=0.30, pos_hint={'top': 1}, padding=padding, spacing=spacing, **kwargs)
        title = (Label(
            text=title,
            font_size=70,
            font_name='fonts/Roboto-Bold.ttf',
            halign='left',
            valign='middle',
        ))
        title.bind(size=lambda inst, val: setattr(inst, 'text_size', val))
        self.add_widget(title)
        self.add_widget(Widget(size_hint_x=1))  # Spacer
        self.add_widget(IconTextButton(
            icon_path=icon_path,
            text=button_text,
            size_hint_y=None,
            size=(110, 110),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            height=50,
            screen_name=button_screen
        ))

class Footer1Bar(BoxLayout):
    def __init__(self, screen_name,current_page, **kwargs):
        super().__init__(orientation='horizontal', size_hint_y=0.15, padding=0, spacing=0, **kwargs)
        self.add_widget(CircularImageButton(
            image_path="images/left_arrow.png",
            diameter=80,
            screen_name=screen_name  # Navigate to menu2 screen
        ))
        self.add_widget(Widget(size_hint_x=1))
        self.add_widget(CircularImageButton(
            image_path="images/right_arrow.png",
            diameter=80,
            screen_name=screen_name  # Navigate to menu2 screen
        ))


class Footer2Bar(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='horizontal', size_hint_y=0.03, padding=0, spacing=10)
        previous = Label(text="   Previous", size_hint_x=None, width=100, halign='left')
        previous.bind(size=lambda inst, val: setattr(inst, 'text_size', val))
        self.add_widget(previous)
        self.add_widget(Label(text=f"Version: {load_config('config/V3.json').get('version', 'N/A')} | Device ID: {load_config('config/V3.json').get('sensor_ID', 'N/A')}",size_hint_x =1) )
        next = Label(text="Next      ", size_hint_x=None, width=100, halign='right')
        next.bind(size=lambda inst, val: setattr(inst, 'text_size', val))
        self.add_widget(next)


class SeparatorLine(Widget):
    def __init__(self, points=[50, 300, 950, 300], **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            Color(0.7, 0.7, 0.7, 1)  # Grey color
            self.line = Line(points=points, width=1)  # x1, y1, x2, y2

    def on_size(self, *args):
        # Optionally update line position if widget size changes
        self.line.points = [self.x, self.center_y, self.right, self.center_y]


class SafeScreen(Screen):
    """
    A Screen that delays touch activation to prevent double touches during transitions."""
    touch_enabled = False

    def on_enter(self):
        # Delay touch activation by 1s
        self.touch_enabled = False
        Clock.schedule_once(self.enable_touch, 0.5)

    def enable_touch(self, dt):
        self.touch_enabled = True

    def on_touch_down(self, touch):
        if not self.touch_enabled:
            return True  # Swallow touch during transition
        return super().on_touch_down(touch)

