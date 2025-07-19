from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle, Ellipse, Line
from kivy.properties import BooleanProperty
from kivy.uix.floatlayout import FloatLayout
from utils.icons import IconTextButton
from kivy.uix.image import Image
from kivy.clock import Clock


class QwertyKeyboard(FloatLayout):
    shift_activate = BooleanProperty(False)

    def __init__(self, title, **kwargs): 
        super().__init__(**kwargs)
        self.buttons = []
        main_layout = BoxLayout(
            orientation='vertical', 
            padding=20, 
            size_hint=(1, 1), 
            pos=(0, 0)
        )
        label = Label(
            text=title,
            font_size=40,
            size_hint_y=0.2,
            size_hint_x=1,
            font_name = 'fonts/Roboto-Bold.ttf',
            halign='left',
            valign='middle'
        )
        label.bind(size=lambda instance, value: setattr(instance, 'text_size', value))
        main_layout.add_widget(label)
        self.text_input = TextInput(font_size=32, size_hint_y=0.15,
                                    background_color=(0, 0, 0, 0),   # transparent background
                                    foreground_color=(1, 1, 0, 1),
                                    font_name='fonts/Roboto-Regular.ttf',
                                    )
        
        partition = SeparatorLine(
            size_hint=(0.4, 0.05),
            pos  = (20,440),
        )
        main_layout.add_widget(self.text_input)
        self.add_widget(partition)


        shift_keys = [
            ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
            ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
            ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
            ['Shift','Z', 'X', 'C', 'V', 'B', 'N', 'M', 'Backspace'],
            ['Japanese', ',', 'Space','.', 'Enter']
        ]
        keys = [
            ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
            ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
            ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l'],
            ['Shift', 'z', 'x', 'c', 'v', 'b', 'n', 'm', 'Backspace'],
            ['Japanese', ',', 'Space', '.', 'Enter']
        ]
        subkeys = [
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            ['%', "\\", '|', '=', "[", "]", '<', '>', '{', '}'],   # 10 subkeys (correct)
            ['@', '#', '$', '_', '&', '-', '+', '(', ')'],
            [' ', '*', '\"', '\'', ':', ';', '!', '?', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ']
        ]
        key_width = 90
        key_spacing = 8

        for row, subrow, shift_row in zip(keys, subkeys, shift_keys):
            if len(row) == 10:
                first_row_width = len(row) * key_width + (len(row) - 1) * key_spacing + 6
            num_keys = len(row)
            if 'Shift' in row or 'Enter' in row:
                width = first_row_width
            #     width = (num_keys - 2) * key_width + 2* key_width*1.4 + (num_keys - 1) * key_spacing + 6
            # elif 'Enter' in row:
            #     width = (num_keys-3) * key_width + 2 * key_width*1.4 + key_width*5 + (num_keys - 1) * key_spacing + 15
            else:
                width = num_keys * key_width + (num_keys - 1) * key_spacing + 6
            row_layout = GridLayout(
                cols=num_keys,
                size_hint_y=None,
                height=80,
                spacing=key_spacing,
                padding=3,
                size_hint_x=None,
                width= width,
                pos_hint={'center_x': 0.5}
            )
            for key, sub_key, shift_key in zip(row, subrow, shift_row):
                btn = None
                if key == 'Shift':
                    btn = RoundedButton(text='', sub_key=sub_key, image=f'images/shift.png', font_size=24, font_name='fonts/Roboto-Bold.ttf',
                                        background_color = (0.22, 0.45, 0.91, 1), size_hint_x=None, width=key_width*1.5,
                                        function='Shift',  shift_key='')
                elif key == key == 'Japanese':
                    btn = RoundedButton(text='', sub_key=sub_key, image=f'images/{key}.png', font_size=24, font_name='fonts/Roboto-Bold.ttf',
                                        background_color=(0.22, 0.45, 0.91, 1), size_hint_x=None, width=key_width*1.5,
                                        function='Japanese',  shift_key='')
                elif key == 'Backspace':
                    btn = RoundedButton(text='', sub_key=sub_key, image='images/backspace.png', font_size=24, font_name='fonts/Roboto-Bold.ttf',
                                        background_color=(0.22, 0.45, 0.91, 1), size_hint_x=None, width=key_width*1.5,
                                        function='Backspace',  shift_key='')
                elif key == 'Enter':
                    btn = RoundedButton(text='', sub_key=sub_key, image='images/enter.png', font_size=24, font_name='fonts/Roboto-Bold.ttf',
                                        background_color=(0.22, 0.45, 0.91, 1), size_hint_x=None, width=key_width*1.5,
                                        function='Enter',  shift_key='')
                elif key == 'Space':
                    btn = RoundedButton(text='', sub_key=sub_key,  font_size=24, font_name='fonts/Roboto-Bold.ttf',
                                        size_hint_x=None, width=key_width*5.35,
                                        function='Space',  shift_key='')
                else:
                    btn = RoundedButton(text=key, sub_key=sub_key, font_size=24, font_name='fonts/Roboto-Bold.ttf',
                                        size_hint_x=None, width=key_width, shift_key=shift_key)
                self.buttons.append(btn)
                btn.bind(on_release=self.on_key_release)
                row_layout.add_widget(btn)
            main_layout.add_widget(row_layout)
        main_layout.add_widget(Label(text='time bar will be here',size_hint_y=0.05)) # Spacer at the bottom
        self.add_widget(main_layout)

        overlay = FloatLayout(size_hint=(1, 1))
        home_button = IconTextButton(
            text='Home',
            icon_path='images/home.png',
            size_hint=(None, None),
            size=(110, 110),
            pos_hint={'top': 0.95, 'right': 0.97}
        )
        overlay.add_widget(home_button)
        self.add_widget(overlay)  # Add overlay last so it's on top
    

    def on_key_release(self, instance):
        if hasattr(instance, 'is_long_press') and instance.is_long_press and instance.sub_key:
            # Handle long press for subkeys
            self.text_input.text += instance.sub_key
        elif instance.function == 'Space':
            self.text_input.text += ' '
        elif instance.function == 'Backspace':
            self.text_input.text = self.text_input.text[:-1]
        elif instance.function == "Shift":
                for btn in self.buttons:
                    btn.update_shift_text()
        elif instance.function == "Japanese":
            pass
        else:
            self.text_input.text += instance.text


class RoundedButton(Button):
    def __init__(self, text = None,sub_key = None, shift_key = None,function = None, image = None, background_color = (0.2, 0.2, 0.2, 1), **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.sub_key = sub_key
        self.shift_key = shift_key
        self.function = function
        self.image = image
        self.background_normal = ''
        self.background_down = ''
        self.background_color = (0,0,0,0)
        self.long_press_event = None
        self.is_long_press = False

        with self.canvas.before:
            self.rect_color = Color(*background_color)
            self.rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[20,]
            )

        # Create a FloatLayout that fills the button
        self.float_layout = FloatLayout(size=self.size, pos=self.pos)
        self.bind(pos=self.update_float_layout, size=self.update_float_layout)

        if self.image:
            img = Image(
                source=self.image,
                size_hint=(0.6, 0.6),
                pos_hint={'center_x': 0.5, 'center_y': 0.5},
                allow_stretch=True,
                keep_ratio=True
            )
            self.float_layout.add_widget(img)

        if self.sub_key:
            sub_key_label = Label(
                text=self.sub_key,
                font_size=14,
                size_hint=(None, None),
                size=(self.width * 0.3, self.height * 0.3),
                pos_hint={'right': 1, 'top': 1},
                halign='right',
                valign='top',
                font_name='fonts/Roboto-Bold.ttf'
            )
            sub_key_label.bind(size=lambda instance, value: setattr(instance, 'text_size', value))
            self.float_layout.add_widget(sub_key_label)
        self.add_widget(self.float_layout)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def update_shift_text(self):
        temporary = self.text
        self.text = self.shift_key 
        self.shift_key = temporary
    
    def update_float_layout(self, *args):
        self.float_layout.pos = self.pos
        self.float_layout.size = self.size
    
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.is_long_press = False
            self.long_press_event = Clock.schedule_once(self.trigger_long_press, 2)
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        if self.long_press_event:
            self.long_press_event.cancel()
            self.long_press_event = None
        return super().on_touch_up(touch)

    def trigger_long_press(self, dt):
        self.is_long_press = True
        # You can call a callback or set a flag here


class SeparatorLine(Widget):
    def __init__(self, line_color=(1, 1, 1, 1), pos=(0, 0), **kwargs):
        super().__init__(**kwargs)
        self.pos = pos
        with self.canvas:
            Color(*line_color)
            self.line = Line(points=[self.x, self.center_y, self.x + self.width, self.center_y], width=2)
        self.bind(pos=self.update_line, size=self.update_line)

    def update_line(self, *args):
        self.line.points = [self.x, self.center_y, self.x + self.width, self.center_y]