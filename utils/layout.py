from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, Ellipse
from utils.icons import IconTextButton, PageIndicator, CircularImageButton, PageIndicatorWidget
from kivy.uix.anchorlayout import AnchorLayout
from utils.config_loader import load_config
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from utils.config_loader import update_text_language
import math

class HeaderBar(BoxLayout):
    def __init__(self, title="Language", icon_path="images/home.png", button_text="home", button_screen="menu", padding=[50, 0, 50, 0], spacing=10, **kwargs):
        super().__init__(orientation='horizontal', size_hint_y=0.30, pos_hint={'top': 1}, padding=padding, spacing=spacing, **kwargs)
        self.button_text = button_text
        self.title = title
        self.title_label = (Label(
            text=update_text_language(self.title),
            font_size=70,
            font_name='fonts/MPLUS1p-Bold.ttf',
            halign='left',
            valign='middle',
            size_hint_x = 1,
     ))
        self.title_label.bind(size=lambda inst, val: setattr(inst, 'text_size', val))
        self.add_widget(self.title_label)
        #self.add_widget(Widget())  # Spacer
        self.top_right_button = IconTextButton(
            icon_path=icon_path,
            text=update_text_language(button_text),
            size_hint_y=None,
            size=(110, 110),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            height=50,
            screen_name=button_screen
        )
        self.add_widget(self.top_right_button)

    def update_language(self):
        self.title_label.text = update_text_language(self.title)
        self.top_right_button.label.text = update_text_language(self.button_text)

class FooterBar(BoxLayout):
    def __init__(self, screen_name, **kwargs):
        super().__init__(orientation='horizontal', size_hint_y=0.2, padding=0, spacing=0, **kwargs)

        # Left button + label
        left_col = BoxLayout(orientation='vertical', size_hint_x=None, width=80, spacing=5)
        left_btn = CircularImageButton(
            image_path="images/left_arrow.png",
            diameter=80,
            screen_name=screen_name,
            halign='center'
        )
        self.left_label = Label(
            text=update_text_language("previous"),
            font_name='fonts/MPLUS1p-Regular.ttf',
            font_size=18,
            halign='center',
            valign='top',
            size_hint_y=None,
            height=30
        )
        self.left_label.bind(size=lambda inst, val: setattr(inst, 'text_size', val))
        left_col.add_widget(left_btn)
        left_col.add_widget(self.left_label)

        # Center details
        center_col = BoxLayout(orientation='vertical', size_hint_x=1, spacing=5)
        center_col.add_widget(Widget(size_hint_y=0.15))  # Spacer
        self.details = Label(
            text=f"{update_text_language('version')}: {load_config('config/V3.json').get('version', 'N/A')} | {update_text_language('device_id')}: {load_config('config/V3.json').get('sensor_ID', 'N/A')}",
            font_name='fonts/MPLUS1p-Regular.ttf',
            font_size=16,
            size_hint_y=0.05,
            halign='center',
            valign='middle'
        )
        self.details.bind(size=lambda inst, val: setattr(inst, 'text_size', val))
        center_col.add_widget(self.details)

        # Right button + label
        right_col = BoxLayout(orientation='vertical', size_hint_x=None, width=800, spacing=5)
        right_btn = CircularImageButton(
            image_path="images/right_arrow.png",
            diameter=80,
            screen_name=screen_name,
            halign='center'
        )
        self.right_label = Label(
            text=update_text_language("next"),
            font_name='fonts/MPLUS1p-Regular.ttf',
            font_size=18,
            halign='center',
            valign='top',
            size_hint_y=None,
            height=30
        )
        self.right_label.bind(size=lambda inst, val: setattr(inst, 'text_size', val))
        right_col.add_widget(right_btn)
        right_col.add_widget(self.right_label)

        # Add all columns to the horizontal layout
        self.add_widget(left_col)
        self.add_widget(center_col)
        self.add_widget(right_col)

    def update_language(self):
        """
        Update the language of the footer.
        """
        self.left_label.text = update_text_language("previous")
        self.details.text = f"{update_text_language('version')}: {load_config('config/V3.json').get('version', 'N/A')} | {update_text_language('device_id')}: {load_config('config/V3.json').get('sensor_ID', 'N/A')}"
        self.right_label.text = update_text_language("next")

class SeparatorLine(Widget):
    def __init__(self, points=[50, 300, 950, 300], **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            Color(0.7, 0.7, 0.7, 1)  # Grey color
            self.line = Line(points=points, width=1)  # x1, y1, x2, y2

    def on_size(self, *args):
        # Optionally update line position if widget size changes
        self.line.points = [self.x, self.center_y, self.right, self.center_y]


class LoadingCircle(Widget):
    def __init__(self, size=80, dot_radius=8, dot_color=(0.22, 0.45, 0.91, 1), **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (size, size)
        self.dot_radius = dot_radius
        self.dot_color = dot_color
        self.angle = 0
        self.num_dots = 8
        self._dots = []
        with self.canvas:
            for i in range(self.num_dots):
                Color(*self.dot_color)
                dot = Ellipse(size=(self.dot_radius, self.dot_radius))
                self._dots.append(dot)
        self.bind(pos=self.update_dots, size=self.update_dots)
        Clock.schedule_interval(self.animate, 1/30)

    def update_dots(self, *args):
        cx, cy = self.center
        r = (self.width - self.dot_radius) / 2
        for i, dot in enumerate(self._dots):
            angle = math.radians(self.angle + i * 360 / self.num_dots)
            x = cx + r * math.cos(angle) - self.dot_radius / 2
            y = cy + r * math.sin(angle) - self.dot_radius / 2
            dot.pos = (x, y)
            dot.size = (self.dot_radius, self.dot_radius)

    def animate(self, dt):
        self.angle = (self.angle + 8) % 360
        self.update_dots()

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

