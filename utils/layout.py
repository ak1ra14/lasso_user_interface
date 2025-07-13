from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line
from utils.icons import IconTextButton
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

class SeparatorLine(Widget):
    def __init__(self, points=[50, 300, 950, 300], **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            Color(0.7, 0.7, 0.7, 1)  # Grey color
            self.line = Line(points=points, width=1)  # x1, y1, x2, y2

    def on_size(self, *args):
        # Optionally update line position if widget size changes
        self.line.points = [self.x, self.center_y, self.right, self.center_y]
