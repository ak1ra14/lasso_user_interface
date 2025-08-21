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
from utils.config_loader import load_config, update_text_language
from kivy.properties import BooleanProperty
from kivy.clock import Clock
from utils.freeze_screen import freeze_ui


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
    def __init__(self, icon_path = None, text = "", font_size = 20, size=(190,190), radius=[20,], screen_name=None, config = False, pos_hint = None, **kwargs):
        super().__init__(**kwargs)
        self.config = config  # Store the config status
        self.label_text=text
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
        if self.label_text == "": # If no label text is provided, we only show the icon
            self.image = Image(
            source=icon_path,
            size_hint=(0.6,0.6),
            pos_hint={'center_x': 0.5, 'center_y': 0.50}  # Center image vertically
            )
        elif icon_path is None: #for server button 
            self.label = Label(
                text=self.label_text,
                font_size= font_size,  # Adjust font size based on button height
                font_name='fonts/MPLUS1p-Regular.ttf',
                color=(1, 1, 1, 1),
                size_hint=(0.9, 0.9),
                pos_hint={'center_x': 0.5, 'center_y': 0.5},
                halign='center',
                valign='middle'
            )
            self.label.bind(size=lambda inst, val: setattr(inst, 'text_size', val))
            layout.add_widget(self.label)
            self.add_widget(layout)
            return
        else:  # If both icon and text are provided, we show both
            self.image = Image(
                source=icon_path,
                size_hint=(0.45,0.45),
                pos_hint={'center_x': 0.5, 'center_y': 0.65}  # Center image vertically
            )
        layout.add_widget(self.image)
        if self.config:
            self.label = Label(
                text=self.label_text,
                font_size=  self.size[1] * 0.1 - 3 if self.label_text == 'スクリーンセーバー' or self.label_text == 'Screensaver' else self.size[1] * 0.1,   # Adjust font size based on button height.
                font_name='fonts/MPLUS1p-Regular.ttf',  # Path to your bold font file
                color=(1, 1, 1, 1),
                size_hint=(0.9, 0.10),
                pos_hint={'center_x': 0.5, 'center_y': 0.33},
                halign='center',
                valign='middle'
            )
            self.label.bind(size=lambda inst, val: setattr(inst, 'text_size', val))

            self.status = Label(
                text= str(self.config),
                font_size= self.size[1] * 0.1 -3,  # Adjust font size based on button height
                font_name='fonts/MPLUS1p-Regular.ttf',  # Path to your bold font file
                color=(1, 1, 1, 1),
                size_hint=(0.9, 0.15),
                pos_hint={'center_x': 0.5, 'center_y': 0.15},
                halign='center',
                valign='middle',
                shorten=True,
                max_lines=1,
            )
            self.status.bind(size=lambda inst, val: setattr(inst, 'text_size', val))
            layout.add_widget(self.label)
            layout.add_widget(self.status)

        else:
            if self.label_text:
                self.label = Label(
                    text=self.label_text,
                    font_size= self.size[1] * 0.1 if len(self.label_text) > 5 and App.get_running_app().language == 'jp' else self.size[1]*0.1 + 5,  # Adjust font size based on button height.
                    font_name='fonts/MPLUS1p-Regular.ttf',  # Path to your bold font file
                    color=(1, 1, 1, 1),
                    size_hint=(0.8, 0.3),
                    pos_hint={'center_x': 0.5, 'center_y': 0.25},
                    halign='center',
                    valign='middle'
                )
                #label.bind(size=lambda inst, val: setattr(inst, 'text_size', val))
                layout.add_widget(self.label)
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
        App.get_running_app().play_sound()  # Play sound on button press
        self.color_instruction.rgba = (0.2, 0.8, 0.2, 1) # Change color to green on press
        Clock.schedule_once(self._reset_color, 0.3)  # Reset color after 0.3 seconds
        # Only navigate if screen_name is set and no custom handler is bound

    def on_release(self):
        if self.screen_name and not self.has_custom_handler():
            App.get_running_app().sm.current = self.screen_name

    def _reset_color(self, dt):
        self.color_instruction.rgba = (0.22, 0.45, 0.91, 1)

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
            self.color_instruction = Color(rgba=(0.22, 0.45, 0.91, 1))
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
        self.color_instruction.rgba = (0.2, 0.8, 0.2, 1)  # Change color to green on press
        Clock.schedule_once(self._reset_color, 0.3)  # Reset color after
        App.get_running_app().play_sound()  # Play sound on button press

    def _reset_color(self, dt):
        self.color_instruction.rgba = (0.22, 0.45, 0.91, 1)

    def has_custom_handler(self):
        """
        Check if more than one handler is bound to on_press (the default and a custom one).
        This is used to determine if the button should navigate to a screen.
        """
        return len(self.get_property_observers('on_press')) > 1

    def on_release(self):
        """
        Override the on_release method to handle button release.
        This method is called when the button is released.
        """
        if self.screen_name and not self.has_custom_handler():
            App.get_running_app().sm.current = self.screen_name

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
            App.get_running_app().play_sound()  # Play sound on toggle
            freeze_ui(0.3)  # Freeze UI for 0.3 seconds
            return True
        return False


class ToggleButton(BoxLayout):
    def __init__(self, text_left="", text_right="", text_size_l_r=(75, 130), switch=None, **kwargs):
        super().__init__(orientation='horizontal', spacing=7.5, padding=7.5, **kwargs)
        self.size_hint = (None, None)
        self.size = (400 * 0.75, 60 * 0.75)  # 3/4 of original size
        self.text_right = text_right  # Store the right text for later use
        self.text_size_l_r = text_size_l_r
        self.text_left = text_left

        self.one_label = Label(
            text=update_text_language(self.text_left),
            color=(1, 1, 1, 1),
            size_hint=(None, None),
            size=(text_size_l_r[0], 30),
            font_size=20,
            font_name='fonts/MPLUS1p-Regular.ttf',
            halign='right',
            valign='middle',
        )
        self.one_label.bind(size=lambda inst, val: setattr(inst, 'text_size', val))
        self.switch = switch if switch else CustomSwitch(size_hint=(None, None), size=(60 * 0.75, 30 * 0.75))
        self.two_label = Label(
            text=update_text_language(self.text_right),
            color=(1, 1, 1, 1),
            size_hint=(None, None),
            size=(text_size_l_r[1], 30),
            font_name='fonts/MPLUS1p-Regular.ttf',
            font_size=20,
            halign='left',
            valign='middle',
        )
        self.two_label.bind(size=lambda inst, val: setattr(inst, 'text_size', val))
        #call back function to set text size
        self.two_label.text_size = self.two_label.size

        self.add_widget(self.one_label)
        self.add_widget(self.switch)
        self.add_widget(self.two_label)
    
    def update_language(self):
        self.one_label.text = update_text_language(self.text_left)
        self.two_label.text = update_text_language(self.text_right)


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



class FlickKey(Button):
    """
    Buttons for japanese flick input.
    Flick key with mappings: (center, up, right, down, left).
    Tap -> center, flick up/right/down/left -> corresponding char.
    """
    def __init__(self, mappings, text_input, threshold=20, **kwargs):
        super().__init__(**kwargs)
        self.mappings = list(mappings) + [None] * (5 - len(mappings))
        self.text_input = text_input
        self._touch_start = None
        self.preview = None
        self.threshold = threshold
        self.font_size = kwargs.get('font_size', 28)
        self.text = self.mappings[0] or ''
        self.font_name = kwargs.get('font_name', 'fonts/MPLUS1p-Regular.ttf')
        self.background_normal = ''
        self.background_down = ''
        self.background_color = (0,0,0,0)  # Transparent color
        with self.canvas.before:
            self.color_instruction = Color(rgba=(0.2, 0.2, 0.2, 1)) #grey color
            self.rounded_rect_instruction = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[20,]  # Adjust this value for more or less curvature
            )
        self.bind(pos=self._update_rect, size=self._update_rect)

    def show_preview(self, char, pos):
        if not self.preview:
            self.preview = Label(size_hint=(None, None), size=(60, 40), font_name=self.font_name,
                                 font_size=24, color=(1, 1, 1, 1))
            # add to root layout (assume parent of parent is main container)
            root = self.get_root_window()
            if root:
                # add to widget tree via parent container if possible
                try:
                    self.parent.parent.add_widget(self.preview)
                except Exception:
                    # fallback: add to parent
                    try:
                        self.parent.add_widget(self.preview)
                    except Exception:
                        pass
        if self.preview:
            self.preview.text = char or ''
            self.preview.pos = (pos[0] - 30, pos[1] + 10)
            self.preview.opacity = 1

    def hide_preview(self):
        if self.preview and self.preview.parent:
            try:
                self.preview.parent.remove_widget(self.preview)
            except Exception:
                pass
            self.preview = None

    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            return False
        self._touch_start = touch.pos
        self.show_preview(self.mappings[0], touch.pos)
        return True

    def on_touch_move(self, touch):
        if self._touch_start is None:
            return False
        dx = touch.x - self._touch_start[0]
        dy = touch.y - self._touch_start[1]
        if abs(dx) + abs(dy) < self.threshold:
            char = self.mappings[0]
        else:
            if abs(dx) > abs(dy):
                char = self.mappings[3] if dx > 0 else self.mappings[1]
            else:
                char = self.mappings[2] if dy > 0 else self.mappings[4]
        self.show_preview(char, touch.pos)
        return True

    def on_touch_up(self, touch):
        if self._touch_start is None:
            return False
        dx = touch.x - self._touch_start[0]
        dy = touch.y - self._touch_start[1]
        if abs(dx) + abs(dy) < self.threshold:
            chosen = self.mappings[0]
        else:
            if abs(dx) > abs(dy):
                chosen = self.mappings[3] if dx > 0 else self.mappings[1]
            else:
                chosen = self.mappings[2] if dy > 0 else self.mappings[4]
        if chosen:
            try:
                # insert_text handles cursor and selection correctly
                self.text_input.insert_text(chosen)
            except Exception:
                # fallback append
                self.text_input.text += chosen
        self.hide_preview()
        self._touch_start = None
        return True

    def _update_rect(self, instance, value):
        """Callback to update the position and size of the rounded rectangle."""
        self.rounded_rect_instruction.pos = instance.pos
        self.rounded_rect_instruction.size = instance.size
    
    def _update_color(self, instance, value):
        """Callback to update the color of the rounded rectangle."""
        self.color_instruction.rgba = value