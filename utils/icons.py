from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle, Ellipse, Rectangle
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.anchorlayout import AnchorLayout
from kivy.app import App
from kivy.core.audio import SoundLoader

class ColoredLabel(Label):
    def __init__(self, **kwargs):
        bg_color = kwargs.pop('bg_color', (1, 1, 1, 1))  # Default white
        super().__init__(**kwargs)
        with self.canvas.before:
            self.bg_color = Color(*bg_color)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_bg, size=self._update_bg)

    def _update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

class IconTextButton(Button):
    """
    A custom button class that extends Kivy's Button.
    It includes properties for text and image source, and its layout
    is defined entirely in Python.
    """
    def __init__(self, icon_path, text = None, size=(120, 120), radius=[20,], screen_name=None, **kwargs):
        super().__init__(**kwargs)
        if 'size_hint' not in kwargs:
            self.size_hint = (None, None)
        self.size = size
        self.screen_name = screen_name  # Store the screen name for navigation
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}  # Optional, to center

        self.background_normal = ''
        self.background_down = ''
        self.background_color = (0,0,0,0)  # Transparent color
        with self.canvas.before:
            self.color_instruction = Color(rgba=(0.22, 0.45, 0.91, 1))
            self.rounded_rect_instruction = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=radius  # Adjust this value for more or less curvature
            )
        self.bind(pos=self._update_rect, size=self._update_rect)

        layout = BoxLayout(orientation='vertical', spacing=0, padding=5, size_hint=(1, 1))
        layout.size = self.size
        layout.pos = self.pos
        self.bind(pos=layout.setter('pos'), size=layout.setter('size'))
        image = Image(
            source=icon_path,
            allow_stretch=True,
            keep_ratio=True,
            size_hint=(0.5, 0.5),
            pos_hint={'center_x': 0.5, 'center_y': 0.7}  # Center image vertically
        )
        layout.add_widget(image)

        font_size = self.size[1] * 0.1 + 10  # Adjust font size based on button height
        if text:
            label = Label(
                text=text,
                font_size= font_size,
                font_name='fonts/Roboto-Bold.ttf',  # Path to your bold font file
                color=(1, 1, 1, 1),
                size_hint=(0.7, 0.3),
                pos_hint={'center_x': 0.5, 'center_y': 0.2},
                halign='center',
                valign='middle'
            )
            #label.bind(size=lambda inst, val: setattr(inst, 'text_size', val))
            layout.add_widget(label)
        self.add_widget(layout)

        # 🔁 Bind parent after widget is attached
        #self.bind(parent=self.on_parent_set)

    def on_parent_set(self, instance, parent):
        if parent:
            print("Parent set:", parent)
            # You could now access parent.size or position and do logic based on that
            # e.g., self.pos = (parent.width/2, parent.height/2) -- but usually unnecessary with pos_hint
    

    def _update_rect(self, instance, value):
        """Callback to update the position and size of the rounded rectangle."""
        self.rounded_rect_instruction.pos = instance.pos
        self.rounded_rect_instruction.size = instance.size

    def _update_color(self, instance, value):
        """Callback to update the color of the rounded rectangle."""
        self.color_instruction.rgba = value

    def _update_image_source(self, instance, value):
        """Callback to update the image source when button_image_source changes."""
        self.image_widget.source = value

    def _update_label_text(self, instance, value):
        """Callback to update the label text when button_text changes."""
        self.label_widget.text = value

    def on_press(self):
        """
        Override the on_press method to change the current screen.
        This method is called when the button is pressed.
        """
        sound = SoundLoader.load('sound/tap.mp3')
        if sound:
            sound.play()
        App.get_running_app().sm.current = self.screen_name

class CircularImageButton(Button):
    def __init__(self, image_path, diameter=80, screen_name=None, **kwargs):
        super().__init__(**kwargs)
        self.screen_name = screen_name  # Store the screen name for navigation
        self.size_hint = (None, None)
        self.size = (diameter, diameter)
        self.background_normal = ''
        self.background_down = ''
        self.background_color = (0, 0, 0, 0)  # Fully transparent

        with self.canvas.before:
            Color(0.22, 0.45, 0.91, 1)  # Example blue color
            self.circle = Ellipse(pos=self.pos, size=self.size)
        self.bind(pos=self._update_circle, size=self._update_circle)

        # Center the image using AnchorLayout
        self.anchor = AnchorLayout(size=self.size, size_hint=(None, None))
        self.bind(pos=self.anchor.setter('pos'), size=self.anchor.setter('size'))

        self.img = Image(source=image_path, size_hint=(0.6, 0.6), allow_stretch=True, keep_ratio=True)
        self.anchor.add_widget(self.img)
        self.add_widget(self.anchor)
        # Bind anchor size to button size
        self.bind(size=self._update_anchor)

    def _update_circle(self, *args):
        self.circle.pos = self.pos
        self.circle.size = self.size

    def _update_anchor(self, instance, value):
        self.anchor.size = self.size

    def on_press(self):
        """
        Override the on_press method to change the current screen.
        This method is called when the button is pressed.
        """
        sound = SoundLoader.load('sound/tap.mp3')
        if sound:
            sound.play()
        App.get_running_app().sm.current = self.screen_name


class PageIndicator(BoxLayout):
    def __init__(self, num_pages=2, current_page=0, **kwargs):
        super().__init__(orientation='horizontal', spacing=10, **kwargs)
        self.num_pages = num_pages
        self.current_page = current_page
        self.dots = []
        self.build_dots()

    def build_dots(self):
        self.clear_widgets()
        self.dots = []
        for i in range(self.num_pages):
            dot = Widget(size_hint=(None, None), size=(20, 20))
            with dot.canvas:
                Color(0.8, 0.8, 0.8, 1 if i != self.current_page else 1)  # Gray for inactive
                if i == self.current_page:
                    Color(0.22, 0.45, 0.91, 1)  # Blue for active
                Ellipse(pos=dot.pos, size=dot.size)
            dot.bind(pos=self.update_dot, size=self.update_dot)
            self.add_widget(dot)
            self.dots.append(dot)

    def update_dot(self, instance, value):
        instance.canvas.clear()
        i = self.dots.index(instance)
        with instance.canvas:
            if i == self.current_page:
                Color(0.22, 0.45, 0.91, 1)  # Active
            else:
                Color(0.8, 0.8, 0.8, 1)  # Inactive
            Ellipse(pos=instance.pos, size=instance.size)

    def set_page(self, page):
        self.current_page = page
        self.build_dots()