from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle, Ellipse, Line
from kivy.properties import BooleanProperty
from kivy.uix.floatlayout import FloatLayout
from utils.as_icons import IconTextButton
from utils.as_flick_key import FlickKey
from utils.as_layout import SafeScreen
from utils.as_freeze_screen import freeze_ui
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
import sys, os
import mozcpy
from kivy.app import App
from utils.as_config_loader import load_config, update_text_language
import time 
from kivy.uix.popup import Popup
from kivy.logger import Logger


class KeyboardScreen(SafeScreen):
    '''
    A screen that provides a full keyboard functionalities for user input.
    '''
    def __init__(self, title, screen_name = 'menu', **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.screen_name = screen_name
        self.keyboard = QwertyKeyboard(title=self.title, screen_name=self.screen_name, enter_callback=self.press_enter)
        self.add_widget(self.keyboard)
    
    def press_enter(self, instance):
        # Your save logic here
        print("Enter pressed from screen!")

    def update_language(self):
        self.keyboard.label.text = update_text_language(self.title)
        self.keyboard.home_button.label.text = update_text_language("home")

    def on_pre_enter(self):
        self.last_cursor_index = len(self.keyboard.actual_text_input)
        self.start_index = len(self.keyboard.actual_text_input)
        try:
            if not self.keyboard.language_button and App.get_running_app().language == 'jp':
                self.keyboard.language_button = LanguageTextButton(
                    icon_path='images/japanese.png',
                    size_hint=(None, None),
                    size=(110, 110),
                    pos_hint={'top': 0.95, 'right': 0.85},
                )
                self.keyboard.overlay.add_widget(self.keyboard.language_button)
            if self.keyboard.language_button and App.get_running_app().language == 'en':
                self.keyboard.overlay.remove_widget(self.keyboard.language_button)
                self.keyboard.language_button = None
                self.keyboard.show_layout('english')

        except AttributeError:
            pass

class QwertyKeyboard(FloatLayout):
    '''
    A full QWERTY keyboard with English and Japanese input modes, including flick input for Japanese.
    '''
    shift_activate = BooleanProperty(False)
    MAX_CHARS = 100  # Maximum characters allowed in the text input

    def __init__(self, title, screen_name='menu', enter_callback=None, **kwargs):
        super().__init__(**kwargs)
        self.enter_callback = enter_callback
        self.screen_name = screen_name
        self.english_buttons = []
        self.japanese_buttons = []
        self.keyboard_mode = ['english', 'japanese','flick']
        self.keyboard_index = 0
        self.language_mode = 'english'  # Default language mode
        self.kanji_converter = mozcpy.Converter()  # Initialize the converter
        self.converting = False  # Flag to indicate if the text is being converted
        self.title = title
        self.actual_text_input = ""
        self.visibility = True  # Flag to indicate password visibility
        self.last_cursor_index = 0  # Track the last cursor position
        self.last_click_space = False  # Track if the last click was on space
        self.start_index = 0  # Start index for conversion
        self.language_button = None

        ###layout for the keyboard screen
        self.main_layout = BoxLayout(
            orientation='vertical', 
            padding=20, 
            size_hint=(1, 1), 
            pos_hint={'center_x': 0.5, 'center_y': 0.53},
        )
        self.label = Label(
            text=update_text_language(self.title),
            font_size=40,
            size_hint_y=0.2,
            size_hint_x=1,
            font_name = 'fonts/MPLUS1p-Bold.ttf',
            halign='left',
            valign='middle',
            pos = (20, 480),
        )
        self.label.bind(size=lambda instance, value: setattr(instance, 'text_size', value))
        self.text_input = TextInput(font_size=32, size_hint_y=0.15,
                                    background_color=(0, 0, 0, 0),   # transparent background
                                    foreground_color=(1, 1, 0, 1),
                                    size_hint_x=None,
                                    width=560,
                                    font_name='fonts/MPLUS1p-Regular.ttf',
                                    pos = (20, 420),
                                    multiline=False,  # Single line input
                                    halign='left',
                                    )
        #self.text_input.bind(cursor=self.on_cursor_change)
        
        partition = SeparatorLine(
            size_hint=(0.54, 0.05),
            pos  = (20,440),
        )
        self.add_widget(self.label)
        self.add_widget(self.text_input)
        self.add_widget(partition)

#### English keyboard layouts #######
        self.shift_keys = [
            ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
            ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
            ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
            ['Shift','Z', 'X', 'C', 'V', 'B', 'N', 'M', 'Backspace'],
            ['English', ',', 'Space','.', 'Enter']
        ]
        self.keys = [
            ['1', '2', '3', '4', '5', '6', '7', '8', '9' , '0'],
            ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
            ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l'],
            ['Shift', 'z', 'x', 'c', 'v', 'b', 'n', 'm', 'Backspace'],
            ['English', ',', 'Space', '.', 'Enter']
        ]
        self.subkeys = [
            ['', '', '', '', '', '', '', '', '', ''],
            ['%', "\\", '|', '=', "[", "]", '<', '>', '{', '}'],   # 10 subkeys (correct)
            ['@', '#', '$', '_', '&', '-', '+', '(', ')'],
            ['', '*', '\"', '\'', ':', ';', '!', '?', ''],
            ['', '', '', '', '', '']
        ]

#### Japanese keyboard layouts #######
        self.japanese_keys = [
            ['あ', 'か', 'さ', 'た', 'な', 'は', 'ま', 'や', 'ら', 'わ','Backspace'],
            ['い', 'き', 'し', 'ち', 'に', 'ひ', 'み', '', 'り', 'を', 'Space'],
            ['う', 'く', 'す', 'つ', 'ぬ', 'ふ', 'む', 'ゆ', 'る', 'ん', 'Enter'],
            ['え', 'け', 'せ', 'て', 'ね', 'へ', 'め', '', 'れ', '。', 'Daku-on'],
            ['お', 'こ', 'そ', 'と', 'の', 'ほ', 'も', 'よ', 'ろ', '、','Japanese']
            # Add more rows as needed
        ]
        self.japanese_subkeys = [
            ['ア', 'カ', 'サ', 'タ', 'ナ', 'ハ', 'マ', 'ヤ', 'ラ', 'ワ',''],
            ['イ', 'キ', 'シ', 'チ', 'ニ', 'ヒ', 'ミ', '', 'リ', 'ヲ',''],
            ['ウ', 'ク', 'ス', 'ツ', 'ヌ', 'フ', 'ム', 'ユ', 'ル', 'ン',''],
            ['エ', 'ケ', 'セ', 'テ', 'ネ', 'ヘ', 'メ', '', 'レ', 'ー',''],
            ['オ', 'コ', 'ソ', 'ト', 'ノ', 'ホ', 'モ', 'ヨ', 'ロ', '、','']
            # Add more rows as needed
        ]

###### Flick keyboard layouts #######
        self.flick_mappings = [
            ('あ', 'い', 'う', 'え', 'お'),
            ('か', 'き', 'く', 'け', 'こ'),
            ('さ', 'し', 'す', 'せ', 'そ'),
            ('Backspace',),    
            ('た', 'ち', 'つ', 'て', 'と'),
            ('な', 'に', 'ぬ', 'ね', 'の'),
            ('は', 'ひ', 'ふ', 'へ', 'ほ'),
            ('Space',),
            ('ま', 'み', 'む', 'め', 'も'),
            ('や', 'ゆ', 'よ', '',''),
            ('ら', 'り', 'る', 'れ', 'ろ'),
            ('Enter',),
            ('Daku-on',),
            ('わ', 'を', 'ん', 'ー', ''),
            ('、', '。', '?', '!', ''),
            ('Flick',)
        ]
        
        self.add_widget(self.main_layout)
        #overlay used for flick key popup 
        self.overlay = FloatLayout(size_hint=(1, 1), pos=(0, 0))

        self.home_button = IconTextButton(
            text=update_text_language("home"),
            icon_path='images/home.png',
            size_hint=(None, None),
            size=(110, 110),
            pos_hint={'top': 0.95, 'right': 0.97},
            screen_name=self.screen_name,
        )
        if App.get_running_app().language == 'jp':
            self.language_button = LanguageTextButton(
                icon_path='images/japanese.png',
                size_hint=(None, None),
                size=(110, 110),
                pos_hint={'top': 0.95, 'right': 0.85},
            )
            self.overlay.add_widget(self.language_button)


        self.overlay.add_widget(self.home_button)
        self.add_widget(self.overlay)  # Add flick overlay for Japanese input
        self.build_all_keyboards()  # Build all keyboards
        self.show_layout('english')  # Show the default keyboard layout
    
    def build_qwerty_keyboard(self):
        self.language_mode = 'english'  # Set the language mode to English
        key_width = 90
        key_spacing = 8
        self.main_layout.clear_widgets()
        key_width = 90
        key_spacing = 8
        self.english_keyboard = []
        self.shift_lock = False

        for row, subrow, shift_row in zip(self.keys, self.subkeys, self.shift_keys):
            if len(row) == 10:
                first_row_width = len(row) * key_width + (len(row) - 1) * key_spacing + 6
            num_keys = len(row)
            if 'Shift' in row or 'Enter' in row:
                width = first_row_width

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
            ## Based on the key, create different buttons with functions 
            for key, sub_key, shift_key in zip(row, subrow, shift_row):
                btn = None
                if key == 'Shift':
                    btn = RoundedButton(text='', sub_key=sub_key, image=f'images/shift.png', font_size=24, font_name='fonts/Roboto-Bold.ttf',
                                        background_color = (0.22, 0.45, 0.91, 1), size_hint_x=None, width=key_width*1.54,
                                        function='Shift',  shift_key='')
                elif key == 'English':
                    btn = RoundedButton(text='', sub_key=sub_key, image=f'images/switch.png', font_size=24, font_name='fonts/Roboto-Bold.ttf',
                                        background_color=(0.22, 0.45, 0.91, 1), size_hint_x=None, width=key_width*1.54,
                                        function='English',  shift_key='')
                elif key == 'Backspace':
                    btn = RoundedButton(text='', sub_key=sub_key, image='images/backspace.png', font_size=24, font_name='fonts/Roboto-Bold.ttf',
                                        background_color=(0.22, 0.45, 0.91, 1), size_hint_x=None, width=key_width*1.54,
                                        function='Backspace',  shift_key='')
                elif key == 'Enter':
                    btn = RoundedButton(text='', sub_key=sub_key, image='images/enter.png', font_size=24, font_name='fonts/Roboto-Bold.ttf',
                                        background_color=(0.22, 0.45, 0.91, 1), size_hint_x=None, width=key_width*1.54,
                                        function='Enter',  shift_key='',on_press=self.press_enter)
                elif key == 'Space':
                    btn = RoundedButton(text='', sub_key=sub_key,  font_size=24, font_name='fonts/Roboto-Bold.ttf',
                                        size_hint_x=None, width=key_width*5.35,
                                        function='Space',  shift_key='')
                else:
                    btn = RoundedButton(text=key, sub_key=sub_key, font_size=24, font_name='fonts/Roboto-Bold.ttf',
                                        size_hint_x=None, width=key_width, shift_key=shift_key)
                self.english_buttons.append(btn)
                btn.bind(on_release=self.on_key_release)
                row_layout.add_widget(btn)
            self.english_keyboard.append(row_layout)
            #self.main_layout.add_widget(row_layout)
    
    def build_japanese_keyboard(self):
        key_width = 77
        key_spacing = 8
        self.japanese_keyboard = []

        for row, subrow in zip(self.japanese_keys, self.japanese_subkeys):
            num_keys = len(row)
            row_layout = GridLayout(
                cols=num_keys,
                size_hint_y=None,
                height=80,
                spacing=key_spacing,
                padding=3,
                size_hint_x=None,
                width=num_keys * key_width + (num_keys - 1) * key_spacing
            )
            # Based on the key, create different buttons with functions
            for key, sub_key in zip(row, subrow):
                btn = None
                if key == 'Japanese':
                    btn = RoundedButton(text='', sub_key=sub_key, image=f'images/switch.png', font_size=24, font_name='fonts/MPLUS1p-Regular.ttf',
                                        background_color=(0.22, 0.45, 0.91, 1), size_hint_x=None, width=key_width*1.5,
                                        function='Japanese')
                elif key == 'Backspace':
                    btn = RoundedButton(text='', sub_key=sub_key, image='images/backspace.png', font_size=24, font_name='fonts/Roboto-Bold.ttf',
                                        background_color=(0.22, 0.45, 0.91, 1), size_hint_x=None, width=key_width*1.5,
                                        function='Backspace',  shift_key='')
                elif key == 'Enter':
                    btn = RoundedButton(text='', sub_key=sub_key, image='images/enter.png', font_size=24, font_name='fonts/MPLUS1p-Regular.ttf',
                                        background_color=(0.22, 0.45, 0.91, 1), size_hint_x=None, width=key_width*1.5,
                                        function='Enter', on_press=self.press_enter)
                elif key == 'Space':
                    btn = RoundedButton(text='空白', sub_key=sub_key,  font_size=22, font_name='fonts/MPLUS1p-Regular.ttf',
                                        size_hint_x=None, width=key_width*1.5, background_color=(0.22, 0.45, 0.91, 1),
                                        function='Space')
                    self.japanese_space_button = btn
                elif key == 'Daku-on':
                    btn = RoundedButton(text='', sub_key=sub_key, image='images/daku-on.png', font_size=24, font_name='fonts/Roboto-Bold.ttf',
                                        background_color=(0.22, 0.45, 0.91, 1), size_hint_x=None, width=key_width*1.5,
                                        function='Daku-on',  shift_key='')
                else:
                    btn = RoundedButton(text=key, sub_key=sub_key, font_size=24, font_name='fonts/MPLUS1p-Regular.ttf',
                                        size_hint_x=None, width=key_width)
                btn.bind(on_release=self.on_key_release) # Bind the button release event
                self.japanese_buttons.append(btn)
                row_layout.add_widget(btn)
            self.japanese_keyboard.append(row_layout)
            #self.main_layout.add_widget(row_layout)

    def build_flick_keyboard(self):
        # Example flick mappings for common Japanese columns (10 columns)
        self.language_mode = 'japanese'  # Set the language mode to Japanese
        self.main_layout.clear_widgets()  # Clear the main layout

        self.flick_grid = GridLayout(cols=4, spacing=6, 
                                     padding=(100,0,100,0), size_hint_y=None,
                                      height=300)
        # Create buttons based on flick mappings
        for mapping in self.flick_mappings:
            if len(mapping) == 5 and type(mapping[0]) is str:
                btn = FlickKey(mappings=mapping,keyboard=self, overlay=self.overlay,
                            size_hint=(None, None), size=(90, 90))
                btn.bind(on_release=self.on_key_release) 
            else:
                if mapping[0] == 'Backspace':
                    btn = RoundedButton(
                        text='', sub_key='', image='images/backspace.png', font_size=24, font_name='fonts/MPLUS1p-Regular.ttf',
                        size_hint=(None, None), size=(120, 90), function='Backspace'
                    )
                elif mapping[0] == 'Enter':
                    btn = RoundedButton(
                        text='', sub_key='', image='images/enter.png', font_size=24, font_name='fonts/MPLUS1p-Regular.ttf',
                        size_hint=(None, None), size=(120, 90), function='Enter', on_press=self.press_enter
                    )
                elif mapping[0] == 'Space':
                    btn = RoundedButton(
                        text='空白', sub_key='', font_size=24, font_name='fonts/MPLUS1p-Regular.ttf',
                        size_hint=(None, None), size=(120, 90), function='Space'
                    )
                    self.flick_space_button = btn
                elif mapping[0] == 'Daku-on':
                    btn = RoundedButton(
                        text='', sub_key='', image='images/daku-on.png', font_size=24, font_name='fonts/MPLUS1p-Regular.ttf',
                        size_hint=(None, None), size=(90, 90), function='Daku-on'
                    )
                elif mapping[0] == 'Flick':
                    btn = RoundedButton(
                        text='', sub_key='', image='images/switch.png', font_size=24, font_name='fonts/MPLUS1p-Regular.ttf',
                        size_hint=(None, None), size=(120, 90), function='Flick'
                    )
                btn.bind(on_release=self.on_key_release)
            self.flick_grid.add_widget(btn)
            self.flick_grid.bind(minimum_height=self.flick_grid.setter('height'))

        #self.main_layout.add_widget(self.flick_grid)

    def build_all_keyboards(self):
        self.build_qwerty_keyboard()
        self.build_japanese_keyboard()
        self.build_flick_keyboard()

    def show_layout(self, layout):
        self.main_layout.clear_widgets()
        if layout == 'english':
            for row in self.english_keyboard:
                self.main_layout.add_widget(row)
            self.language_mode = 'english'
            self.cursor_pos = None
            self.last_click_enter = False
        elif layout == 'japanese':
            for row in self.japanese_keyboard:
                self.main_layout.add_widget(row)
            self.language_mode = 'japanese'
            self.start_index = self.text_input.cursor_index()  # Save the cursor position
            self.entered = False # Flag to indicate if the Enter key has not been pressed to determine the word conversion 
            self.last_click_space = False
            self.last_click_backspace = False
            self.last_cursor_index = self.text_input.cursor_index()
            self.cursor_pos = None
            self.last_click_enter = False
        elif layout == 'flick':
            self.main_layout.add_widget(self.flick_grid)
            self.language_mode = 'japanese'
            self.flick_index = 0 # Index to track the current selection in flick mappings
            self.start_index = self.text_input.cursor_index()  # Save the cursor position
            self.selected_flick_mappings = None # Currently selected flick mapping
            self.last_click_time = 0  # Timestamp of the last flick key click
            self.last_cursor_index = self.text_input.cursor_index() # Save the cursor position
            self.last_click_space = False
            self.flick_is_katakana = False  
            self.last_click_backspace = False
            self.last_cursor_index = self.text_input.cursor_index()
            self.cursor_pos = None
            self.last_click_enter = False

    def on_key_release(self, instance):
        '''
         Handle key release events for various keyboard buttons.'''
        #print(f"Key released: {instance.text if instance.text else instance.function}")
        ti = self.text_input #to indicate the position of the input in a word
        ti.focus = True  # Keep the text input focused
        self.cursor_pos = ti.cursor_index()

        #checking if the cursor hasbeen shifted to a new position manually 
        self.text_input.bind(text=self.limit_text_length)  # Bind the text input to limit its length        
       
        # if the same flick key is pressed within one second cycle through the options
        if hasattr(instance,'mappings'):
            now = time.time()
            #recurrent flick key pressed within one second to select other characters
            if self.selected_flick_mappings == instance.mappings and (now - self.last_click_time) < 1.0 and instance.idx == 0:
                self.last_click_time = now
                for _ in range(5):  # At most 5 tries to avoid infinite loop
                    self.flick_index = (self.flick_index + 1) % 5
                    if instance.mappings[self.flick_index]:
                        break
                ti.text = ti.text[:self.cursor_pos - 1] + instance.mappings[self.flick_index] + ti.text[self.cursor_pos:]
                self.actual_text_input = self.actual_text_input[:self.cursor_pos - 1] + instance.mappings[self.flick_index] + self.actual_text_input[self.cursor_pos:]
                ti.cursor = (self.cursor_pos,0)
            # If the flick key is pressed for the first time, initialize the flick index
            else:
                #when the conversion is done and the new word is stared being input 
                if self.converting or ti.cursor_index() != self.last_cursor_index:
                    self.converting = False  # Reset the converting flag
                    self.start_index = self.cursor_pos  # Reset the start index
                chosen = instance.chosen
                try:
                    insert_pos = self.text_input.cursor_index()
                    if self.converting:
                        self.converting = False
                        self.start_index = insert_pos
                    self.actual_text_input = (
                        self.actual_text_input[:insert_pos] +
                        chosen +
                        self.actual_text_input[insert_pos:])
                 #for the password screen when the visibility is off
                    if self.visibility:
                        self.text_input.text = self.text_input.text[:insert_pos] + chosen + self.text_input.text[insert_pos:]
                    else:
                        self.text_input.text = self.text_input.text[:insert_pos] + '*' * len(instance.text) + self.text_input.text[insert_pos:]
                    self.last_click_backspace = False
                    self.last_click_space = False
                    self.japanese_space_button.text = '変換'
                    self.flick_space_button.text = '変換'
                except Exception:
                    print('Error updating text input with chosen character')
                    self.text_input += chosen

                self.last_click_time = now
                self.selected_flick_mappings = instance.mappings
                self.flick_index = 0
                self.programmatic_cursor_change = True
                ti.cursor = (self.cursor_pos + len(instance.text), 0)
                self.programmatic_cursor_change = False
                self.last_cursor_index = ti.cursor_index()
                self.last_click_space = False
                self.last_click_backspace = False
                self.last_click_enter = False

        # Space key function 
        elif instance.function == 'Space':
            #if japanese keyboard, the space key is used for both word conversion and space insertion
            Logger.debug(f"start index{self.start_index},self.last cursor{self.last_cursor_index}, converting{self.converting},last click{self.last_click_backspace}")
            if self.language_mode == 'japanese' and self.start_index < self.last_cursor_index and not self.converting and not self.last_click_backspace:
                # Convert the text to Kanji using the converter
                self.converting = True
                self.converted_text = self.kanji_converter.convert(ti.text[self.start_index:self.cursor_pos],n_best=20)
            if self.last_cursor_index != ti.cursor_index():
                self.converting = False  # Reset the converting flag if cursor has moved
                self.japanese_space_button.text = '空白'
                self.flick_space_button.text = '空白'
                self.start_index = self.cursor_pos  # Reset the start index
            #print(f"self.converting{self.converting},self.cursorpos{self.cursor_pos},self.last_cursor_index{self.last_cursor_index}")
            if self.converting and len(self.converted_text) > 0 and self.cursor_pos == self.last_cursor_index:
                suggested_text = self.converted_text.pop() if self.converted_text else ti.text[self.start_index:self.cursor_pos]
                ti.text = ti.text[:self.start_index] + suggested_text + ti.text[self.cursor_pos:]
                self.programmatic_cursor_change = True
                ti.cursor = (self.start_index + len(suggested_text), 0)
                self.programmatic_cursor_change = False
                self.last_cursor_index = ti.cursor_index()
            else:
                Logger.debug("Inserting space")
                self.converting = False  # Reset the converting flag
                self.japanese_space_button.text = '空白'
                self.flick_space_button.text = '空白'
                self.actual_text_input = self.actual_text_input[:self.cursor_pos] + ' ' + self.actual_text_input[self.cursor_pos:]
                if self.visibility:
                    ti.text = ti.text[:self.cursor_pos] + ' ' + ti.text[self.cursor_pos:]
                else:
                    ti.text = ti.text[:self.cursor_pos] + '*' + ti.text[self.cursor_pos:]
                self.programmatic_cursor_change = True
                ti.cursor = (self.cursor_pos + 1, 0)
                self.programmatic_cursor_change = False
                self.start_index = ti.cursor_index()  # Update the start index
            if self.last_click_backspace:
                self.last_click_backspace = False
            self.last_click_space = True
            self.last_click_enter = False

        elif instance.function == 'Backspace':
            self.japanese_space_button.text = '空白'
            self.flick_space_button.text = '空白'
            if self.cursor_pos > 0:
                if  self.converting:
                    self.converting = False                
                self.actual_text_input = self.actual_text_input[:self.cursor_pos-1] + self.actual_text_input[self.cursor_pos:]
                ti.text = ti.text[:self.cursor_pos-1] + ti.text[self.cursor_pos:]
                self.programmatic_cursor_change = True
                ti.cursor = (self.cursor_pos - 1, 0)
                self.programmatic_cursor_change = False
                self.last_cursor_index = ti.cursor_index()
                #ti.cursor = ti.cursor  # Update the cursor position
                ti.scroll_x = 1
                self.cursor_pos = ti.cursor_index
            self.last_click_backspace = True
            self.last_click_space = False
            self.last_click_enter = False
            self.start_index = ti.cursor_index()

        elif instance.function == "Shift":
            if not self.shift_lock:
                for btn in self.english_buttons:
                    btn.update_shift_text()

        elif instance.function == "Japanese":
            for btn in self.japanese_buttons:
                temp = btn.text
                btn.text = btn.sub_key if btn.sub_key else btn.text
                btn.sub_key = temp
                try:
                    btn.sub_key_label.text = temp
                except AttributeError: pass
        elif instance.function == "English":
            self.shift_lock = not self.shift_lock
            for btn in self.english_buttons:
                temp = btn.text
                btn.text = btn.sub_key if btn.sub_key else btn.text
                btn.sub_key = temp
                try:
                    btn.sub_key_label.text = temp
                except AttributeError: pass
                                
        elif instance.function == "Enter":
            pass
        elif instance.function == 'Flick':
            if not self.flick_is_katakana:
                # Convert to Katakana
                for btn in self.flick_grid.children:
                    if isinstance(btn, FlickKey):
                        new_mappings = tuple(self.to_katakana(char) if char else '' for char in btn.mappings)
                        btn.mappings = new_mappings
                        btn.text = new_mappings[0] if new_mappings and new_mappings[0] else ''
                self.flick_is_katakana = True
            else:
                # Convert back to Hiragana
                for btn in self.flick_grid.children:
                    if isinstance(btn, FlickKey):
                        new_mappings = tuple(self.to_hiragana(char) if char else '' for char in btn.mappings)
                        btn.mappings = new_mappings
                        btn.text = new_mappings[0] if new_mappings and new_mappings[0] else ''
                self.flick_is_katakana = False

        elif instance.function == "Daku-on":
            try: 
                # Store current cursor position
                current_cursor = self.cursor_pos
                
                # Check if there's a character to convert
                if current_cursor > 0 and not self.converting and current_cursor == self.last_cursor_index:
                    # Get the character before cursor
                    char_to_convert = self.actual_text_input[current_cursor-1]
                    converted_char = self.change_dakuon(char_to_convert)
                    
                    # Only proceed if the character actually changed
                    if converted_char != char_to_convert:
                        self.programmatic_cursor_change = True
                        
                        # Update actual text input
                        self.actual_text_input = (
                            self.actual_text_input[:current_cursor-1] + 
                            converted_char + 
                            self.actual_text_input[current_cursor:]
                        )
                        
                        # Update visible text input
                        if self.visibility:
                            self.text_input.text = (
                                self.text_input.text[:current_cursor-1] + 
                                converted_char + 
                                self.text_input.text[current_cursor:]
                            )
                        else:
                            # For password mode, maintain asterisks
                            self.text_input.text = (
                                self.text_input.text[:current_cursor-1] + 
                                '*' + 
                                self.text_input.text[current_cursor:]
                            )
                        
                        # CRITICAL: Reset cursor to same position
                        self.text_input.cursor = (current_cursor, 0)
                        
                        # Update tracking variables
                        self.last_cursor_index = current_cursor
                        self.cursor_pos = current_cursor
                        
                        self.programmatic_cursor_change = False
                        
                        Logger.debug(f"Daku-on conversion: '{char_to_convert}' -> '{converted_char}'")
                    else:
                        Logger.debug(f"No daku-on conversion available for '{char_to_convert}'")
                else:
                    Logger.debug("No character to convert (cursor at beginning)")
                    
            except IndexError:
                Logger.error("Daku-on conversion failed: Index out of range")
            except Exception as e:
                Logger.error(f"Daku-on conversion failed: {e}")


        else:
            #when a new character is added
            if self.language_mode == 'japanese' or self.start_index == self.cursor_pos:
                self.japanese_space_button.text = '変換'
                self.flick_space_button.text = '変換'
            
            #when the conversion is done and the new word is stared being input 
            if self.converting or ti.cursor_index() != self.last_cursor_index:
                #print('index reset due to normal key press')
                self.converting = False  # Reset the converting flag
                self.start_index = self.cursor_pos  # Reset the start index
            self.actual_text_input = self.actual_text_input[:self.cursor_pos] + instance.text + self.actual_text_input[self.cursor_pos:]

            #for the password screen when the visibility is off
            if self.visibility:
                    self.text_input.text = self.text_input.text[:self.cursor_pos] + instance.text + self.text_input.text[self.cursor_pos:]
            else:
                self.text_input.text = self.text_input.text[:self.cursor_pos] + '*' * len(instance.text) + self.text_input.text[self.cursor_pos:]
            self.programmatic_cursor_change = True
            ti.cursor = (self.cursor_pos + len(instance.text), 0)
            self.programmatic_cursor_change = False
            self.last_cursor_index = ti.cursor_index()
            self.last_click_space = False
            self.last_click_backspace = False
            self.last_click_enter = False
            Logger.debug(f"Normal key entered: {instance.text},start index: {self.start_index}, self.converting: {self.converting}, cursor pos: {self.cursor_pos}, last cursor index: {self.last_cursor_index}")

    def press_enter(self, instance):
        if self.language_mode == 'japanese':
            if (not self.last_click_space and not self.last_click_backspace and not self.last_click_enter) or self.converting:
                self.last_click_enter = True
                self.japanese_space_button.text = '空白'
                self.flick_space_button.text = '空白'
                self.last_cursor_index = self.text_input.cursor_index()
                self.converting = False
                self.start_index = self.text_input.cursor_index()  # Reset the start index
                return
        if self.enter_callback:
            self.enter_callback(instance)

    def to_katakana(self, char):
        # Simple Hiragana to Katakana conversion
        # Only works for single characters; extend as needed
        hira = 'ぁあぃいぅうぇえぉおかがきぎくぐけげこごさざしじすずせぜそぞただちぢっつづてでとどなにぬねのはばぱひびぴふぶぷへべぺほぼぽまみむめもやゃゆゅよょらりるれろわをん'
        kata = 'ァアィイゥウェエォオカガキギクグケゲコゴサザシジスズセゼソゾタダチヂッツヅテデトドナニヌネノハバパヒビピフブプヘベペホボポマミムメモヤャユュヨョラリルレロワヲン'
        if char in hira:
            return kata[hira.index(char)]
        return char
    
    def to_hiragana(self, char):
        # Simple Katakana to Hiragana conversion
        kata = 'ァアィイゥウェエォオカガキギクグケゲコゴサザシジスズセゼソゾタダチヂッツヅテデトドナニヌネノハバパヒビピフブプヘベペホボポマミムメモヤャユュヨョラリルレロワヲン'
        hira = 'ぁあぃいぅうぇえぉおかがきぎくぐけげこごさざしじすずせぜそぞただちぢっつづてでとどなにぬねのはばぱひびぴふぶぷへべぺほぼぽまみむめもやゃゆゅよょらりるれろわをん'
        if char in kata:
            return hira[kata.index(char)]
        return char
        
    def change_dakuon(self, char):
        dakuon_map = {
            'か': 'が', 'き': 'ぎ', 'く': 'ぐ', 'け': 'げ', 'こ': 'ご',
            'が': 'か', 'ぎ': 'き', 'ぐ': 'く', 'げ': 'け', 'ご': 'こ',
            'さ': 'ざ', 'し': 'じ', 'す': 'ず', 'せ': 'ぜ', 'そ': 'ぞ',
            'ざ': 'さ', 'じ': 'し', 'ず': 'す', 'ぜ': 'せ', 'ぞ': 'そ',
            'た': 'だ', 'ち': 'ぢ', 'つ': 'づ', 'て': 'で', 'と': 'ど',
            'だ': 'た', 'ぢ': 'ち', 'づ': 'っ', 'で': 'て', 'ど': 'と',
            'は': 'ば', 'ひ': 'び', 'ふ': 'ぶ', 'へ': 'べ', 'ほ': 'ぼ',
            'ば': 'ぱ', 'び': 'ぴ', 'ぶ': 'ぷ', 'べ': 'ぺ', 'ぼ': 'ぽ',
            'ぱ': 'は', 'ぴ': 'ひ', 'ぷ': 'ふ', 'ぺ': 'へ', 'ぽ': 'ほ',
            'あ': 'ぁ', 'い': 'ぃ', 'う': 'ぅ', 'え': 'ぇ', 'お': 'ぉ',
            'ぁ': 'あ', 'ぃ': 'い', 'ぅ': 'う', 'ぇ': 'え', 'ぉ': 'お',
            'や': 'ゃ', 'ゆ': 'ゅ', 'よ': 'ょ','っ': 'つ',
            'ゃ': 'や', 'ゅ': 'ゆ', 'ょ': 'よ',
            'ア': 'ァ', 'イ': 'ィ', 'ウ': 'ゥ', 'エ': 'ェ', 'オ': 'ォ',
            'ァ': 'ア', 'ィ': 'イ', 'ゥ': 'ウ', 'ェ': 'エ', 'ォ': 'オ',
            'カ': 'ガ', 'キ': 'ギ', 'ク': 'グ', 'ケ': 'ゲ', 'コ': 'ゴ',
            'ガ': 'カ', 'ギ': 'キ', 'グ': 'ク', 'ゲ': 'ケ', 'ゴ': 'コ',
            'サ': 'ザ', 'シ': 'ジ', 'ス': 'ズ', 'セ': 'ゼ', 'ソ': 'ゾ',
            'ザ': 'サ', 'ジ': 'シ', 'ズ': 'ス', 'ゼ':   'セ', 'ゾ': 'ソ',
            'タ': 'ダ', 'チ': 'ヂ', 'ツ': 'ヅ', 'テ': 'デ', 'ト': 'ド',
            'ダ': 'タ', 'ヂ': 'チ', 'ヅ': 'ッ', 'デ': 'テ', 'ド': 'ト',
            'ハ': 'バ', 'ヒ': 'ビ', 'フ': 'ブ', 'ヘ': 'ベ', 'ホ': 'ボ',
            'バ': 'パ', 'ビ': 'ピ', 'ブ': 'プ', 'ベ': 'ペ', 'ボ': 'ポ',
            'パ': 'ハ', 'ピ': 'ヒ', 'プ': 'フ', 'ペ': 'ヘ', 'ポ': 'ホ',
            'ヤ': 'ャ', 'ユ': 'ュ', 'ヨ': 'ョ',
            'ャ': 'ヤ', 'ュ': 'ユ', 'ョ': 'ヨ','ッ': 'ツ',
            # Add more mappings as needed
        }
        return dakuon_map.get(char, char)

    def limit_text_length(self, instance, value):
        if len(value) > self.MAX_CHARS:
            instance.text = value[:self.MAX_CHARS]

    # def on_cursor_change(self, instance, value):
    #     # Prevent recursive calls during programmatic changes
    #     if getattr(self, 'programmatic_cursor_change', True):
    #         return

class LanguageTextButton(IconTextButton):
    def on_release(self):
        super().on_release()
        self.parent.parent.keyboard_index = (self.parent.parent.keyboard_index + 1) % len(self.parent.parent.keyboard_mode)
        self.parent.parent.language_mode = 'english' if self.parent.parent.keyboard_mode[self.parent.parent.keyboard_index] == 'english' else 'japanese'
        if self.parent.parent.keyboard_mode[self.parent.parent.keyboard_index] == 'japanese':
            self.parent.parent.show_layout('japanese')
            self.image.source = 'images/japanese.png'
        elif self.parent.parent.keyboard_mode[self.parent.parent.keyboard_index] == 'english':
            self.parent.parent.show_layout('english')
        else: 
            self.parent.parent.show_layout('flick')
            self.image.source = 'images/english.png'


class RoundedButton(Button):
    '''
    A custom button with rounded corners, optional image, sub-key display, and long-press functionality.'''
    def __init__(self, text = None,sub_key = None, shift_key = None,function = None, image = None, background_color = (0.2, 0.2, 0.2, 1), font_name='fonts/Roboto-Regular.ttf', **kwargs):
        super().__init__(font_name=font_name, **kwargs)
        self.text = text
        self.sub_key = sub_key
        self.shift_key = shift_key
        self.function = function
        self.image = image
        self.background_normal = ''
        self.background_down = ''
        self.background_color = (0,0,0,0)
        self.long_press_event = None
        self._debounce = False  # Debounce flag to prevent multiple presses

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
            )
            self.float_layout.add_widget(img)

        if self.sub_key:
            self.sub_key_label = Label(
                text=self.sub_key,
                font_size=14,
                size_hint=(None, None),
                size=(self.width * 0.3, self.height * 0.3),
                pos_hint={'right': 1, 'top': 1},
                halign='right',
                valign='top',
                font_name='fonts/MPLUS1p-Regular.ttf'
            )
            self.sub_key_label.bind(size=lambda instance, value: setattr(instance, 'text_size', value))
            self.float_layout.add_widget(self.sub_key_label)
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
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        if self.long_press_event:
            self.long_press_event.cancel()
            self.long_press_event = None
        return super().on_touch_up(touch)

    def on_press(self):
        #print(f"Button {self.text} pressed")
        App.get_running_app().sound_manager.play_tap()
        freeze_ui(0.3)  # freeze the UI for 0.3 seconds to prevent multiple presses


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

######################
def show_saved_popup(text='saved'):
    '''
    Show a popup notification that settings have been saved. when buttons are pressed 
    '''

    content = BoxLayout(orientation='vertical', padding=20)
    content.add_widget(Label(text=update_text_language(text), font_name="fonts/MPLUS1p-Regular.ttf", font_size=24))
    popup = Popup(title='Notification',
                    content=content,
                    size_hint=(None, None), size=(400, 200),
                    auto_dismiss=True)
    popup.open()
    # Auto-dismiss after 1.5 seconds
    Clock.schedule_once(lambda dt: popup.dismiss(), 1.5)