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
from utils.config_loader import load_config
from kivy.properties import BooleanProperty
from kivy.clock import Clock


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
    def __init__(self, icon_path = None, text = None, font_size = 20, size=(190,190), radius=[20,], screen_name=None, config = False, pos_hint = None, **kwargs):
        super().__init__(**kwargs)
        self.config = config  # Store the config status
        if 'size_hint' not in kwargs:
            self.size_hint = (None, None)
        self.size = size
        self.screen_name = screen_name  # Store the screen name for navigation
        if pos_hint is not None:
            self.pos_hint = pos_hint

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
        layout = FloatLayout(size=self.size, size_hint=(1, 1))
        layout.size = self.size
        layout.pos = self.pos
        self.bind(pos=layout.setter('pos'), size=layout.setter('size'))
        if text is None:
            self.image = Image(
            source=icon_path,
            size_hint=(0.6,0.6),
            pos_hint={'center_x': 0.5, 'center_y': 0.50}  # Center image vertically
            )
        elif icon_path is None: #for server button 
            label = Label(
                text=text,
                font_size= font_size,  # Adjust font size based on button height
                font_name='fonts/Roboto-Bold.ttf',
                color=(1, 1, 1, 1),
                size_hint=(0.9, 0.9),
                pos_hint={'center_x': 0.5, 'center_y': 0.5},
                halign='center',
                valign='middle'
            )
            label.bind(size=lambda inst, val: setattr(inst, 'text_size', val))
            layout.add_widget(label)
            self.add_widget(layout)
            return 
        else:
            self.image = Image(
                source=icon_path,
                size_hint=(0.45,0.45),
                pos_hint={'center_x': 0.5, 'center_y': 0.65}  # Center image vertically
            )
        layout.add_widget(self.image)
        if self.config:
            label = Label(
                text=text,
                font_size= self.size[1] * 0.1,  # Adjust font size based on button height
                font_name='fonts/Roboto-Bold.ttf',  # Path to your bold font file
                color=(1, 1, 1, 1),
                size_hint=(0.7, 0.10),
                pos_hint={'center_x': 0.5, 'center_y': 0.33},
                halign='center',
                valign='middle'
            )
            label.bind(size=lambda inst, val: setattr(inst, 'text_size', val))

            self.status = Label(
                text= str(self.config),
                font_size= self.size[1] * 0.1 -3,  # Adjust font size based on button height
                font_name='fonts/Roboto-Regular.ttf',  # Path to your bold font file
                color=(1, 1, 1, 1),
                size_hint=(0.9, 0.1),
                pos_hint={'center_x': 0.5, 'center_y': 0.15},
                halign='center',
                valign='middle',
                shorten=True,
                max_lines=1,
            )
            self.status.bind(size=lambda inst, val: setattr(inst, 'text_size', val))
            layout.add_widget(label)
            layout.add_widget(self.status)

        else:
            font_size = self.size[1] * 0.1 + 5  # Adjust font size based on button height
            if text:
                label = Label(
                    text=text,
                    font_size= font_size,
                    font_name='fonts/Roboto-Bold.ttf',  # Path to your bold font file
                    color=(1, 1, 1, 1),
                    size_hint=(0.7, 0.3),
                    pos_hint={'center_x': 0.5, 'center_y': 0.25},
                    halign='center',
                    valign='middle'
                )
                #label.bind(size=lambda inst, val: setattr(inst, 'text_size', val))
                layout.add_widget(label)
        self.add_widget(layout)

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
        sound = SoundLoader.load('sound/tap.wav')
        if sound:
            sound.play()
        # Only navigate if screen_name is set and no custom handler is bound
        if self.screen_name and not self.has_custom_handler():
            App.get_running_app().sm.current = self.screen_name

    def has_custom_handler(self):
        # Check if more than one handler is bound to on_press (the default and a custom one)
        return len(self.get_property_observers('on_press')) > 1

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

        self.img = Image(source=image_path, size_hint=(0.6, 0.6))
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
        sound = SoundLoader.load('sound/tap.wav')
        if sound:
            sound.play()
        App.get_running_app().sm.current = self.screen_name  # Navigate to the screen



class CustomSwitch(FloatLayout):
    active = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (120 * 0.75, 40 * 0.75)  # 3/4 of original size

        with self.canvas:
            self.bg_color = Color(0.15, 0.55, 0.75, 1)
            self.bg = RoundedRectangle(pos=self.pos, size=self.size, radius=[15])  # Adjust radius
            self.thumb_color = Color(0, 0, 0, 1)
            self.thumb = Ellipse(pos=(self.x + 2, self.y + 2), size=(36 * 0.75, 36 * 0.75))

        self.bind(pos=self.update_graphics, size=self.update_graphics)
        self.bind(active=self.update_graphics)
        self.bind(on_touch_down=self.toggle)

    def update_graphics(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size

        thumb_size = 36 * 0.75
        if self.active:
            self.bg_color.rgba =(0.22, 0.45, 0.91, 1)
            self.thumb.pos = (self.x + self.width - thumb_size - 2, self.y + 2)
        else:
            self.bg_color.rgba = (0.6, 0.6, 0.6, 1)
            self.thumb.pos = (self.x + 2, self.y + 2)
        self.thumb.size = (thumb_size, thumb_size)

    def toggle(self, instance, touch):
        if self.collide_point(*touch.pos):
            self.active = not self.active
            return True
        return False


class ToggleButton(BoxLayout):
    def __init__(self, text_left="", text_right="", text_size_l_r=(75, 112), switch=None, **kwargs):
        super().__init__(orientation='horizontal', spacing=7.5, padding=7.5, **kwargs)
        self.size_hint = (None, None)
        self.size = (400 * 0.75, 60 * 0.75)  # 3/4 of original size
        self.text_right = text_right  # Store the right text for later use
        self.text_size_l_r = text_size_l_r
        self.text_left = text_left

        self.one_label = Label(
            text=text_left,
            color=(1, 1, 1, 1),
            size_hint=(None, None),
            size=(text_size_l_r[0], 30),
            font_size=20,
            font_name='fonts/Roboto-Bold.ttf',
            halign='right',
            valign='middle',
        )
        self.one_label.bind(size=lambda inst, val: setattr(inst, 'text_size', val))
        self.switch = switch if switch else CustomSwitch(size_hint=(None, None), size=(60 * 0.75, 30 * 0.75))
        self.two_label = Label(
            text=text_right,
            color=(1, 1, 1, 1),
            size_hint=(None, None),
            size=(text_size_l_r[1], 30),
            font_name='fonts/Roboto-Bold.ttf',
            font_size=20,
            halign='left',
            valign='middle',
        )
        #call back function to set text size
        self.two_label.text_size = self.two_label.size
        #self.two_label.bind(size=lambda inst, val: setattr(inst, 'text_size', val))


        self.add_widget(self.one_label)
        self.add_widget(self.switch)
        self.add_widget(self.two_label)


class PageIndicatorWidget(Widget):
    """
    A widget that displays a page indicator with dots.
    It can be used to indicate the current page in a multi-page layout.
    """
    def __init__(self, num_pages=2, current_page=0, **kwargs):
        super().__init__(**kwargs)
        self.num_pages = num_pages
        self.current_page = current_page - 1  # Adjust for zero-based index
        self.dots = []
        self.build_dots()

    def build_dots(self):
        self.canvas.clear()
        self.dots = []
        for i in range(self.num_pages):
            with self.canvas:
                if i == self.current_page:
                    Color(0.22, 0.45, 0.91, 1)  # Blue for active
                else:
                    Color(0.8, 0.8, 0.8, 1)  # Gray for inactive
                Ellipse(pos=(i * 30 + 10, 10), size=(20, 20))  # Adjust position and size as needed
            dot = Widget(size_hint=(None, None), size=(20, 20))
            self.dots.append(dot)
    
    def update_dots(self):
        self.canvas.clear()
        for i, dot in enumerate(self.dots):
            with self.canvas:
                if i == self.current_page:
                    Color(0.22, 0.45, 0.91, 1)
                else:
                    Color(0.8, 0.8, 0.8, 1)
                Ellipse(pos=(i * 30 + 10, 10), size=(20, 20))
            dot = Widget(size_hint=(None, None), size=(20, 20))
            self.dots.append(dot)

class PageIndicator(BoxLayout):
    def __init__(self, num_pages=2, current_page=0, **kwargs):
        super().__init__(orientation='horizontal', spacing=10, **kwargs)
        self.num_pages = num_pages
        self.width = num_pages * 30 + 20
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        self.current_page = current_page -1  # Adjust for zero-based index
        self.dots = []
        self.build_dots()

    def build_dots(self):
        self.clear_widgets()
        self.dots = []
        for i in range(self.num_pages):
            dot = Widget(size_hint=(None, None), size=(20, 20), size_hint_y=None, height=20)
            with dot.canvas:
                Color(0.8, 0.8, 0.8, 1 if i != self.current_page else 1)  # Gray for inactive
                if i == self.current_page:
                    Color(0.22, 0.45, 0.91, 1)  # Blue for active
                Ellipse(pos=(i * 30 + 10, (self.height - 20) / 2), size=(20, 20))
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