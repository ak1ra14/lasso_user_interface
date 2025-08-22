from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle, Ellipse, Line
from kivy.properties import BooleanProperty
from kivy.uix.floatlayout import FloatLayout
from utils.icons import IconTextButton, FlickKey
from utils.layout import SafeScreen
from utils.freeze_screen import freeze_ui
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
import sys, os
import mozcpy
from kivy.app import App
from utils.config_loader import load_config, update_text_language


class KeyboardScreen(SafeScreen):
    def __init__(self, title, **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.keyboard = QwertyKeyboard(title=self.title, enter_callback=self.press_enter)
        self.add_widget(self.keyboard)
    
    def press_enter(self, instance):
        # Your save logic here
        print("Enter pressed from screen!")

    def update_language(self):
        self.keyboard.label.text = update_text_language(self.title)
        self.keyboard.home_button.label.text = update_text_language("home")
        
class QwertyKeyboard(FloatLayout):
    shift_activate = BooleanProperty(False)
    MAX_CHARS = 100  # Maximum characters allowed in the text input

    def __init__(self, title, enter_callback=None, **kwargs):
        super().__init__(**kwargs)
        self.enter_callback = enter_callback
        self.english_buttons = []
        self.japanese_buttons = []
        self.language_mode = 'english'  # Default language mode
        self.kanji_converter = mozcpy.Converter()  # Initialize the converter
        self.converting = False  # Flag to indicate if the text is being converted
        self.title = title
        self.actual_text_input = ""
        self.visibility = True  # Flag to indicate password visibility
        
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
                                    width=600,
                                    font_name='fonts/MPLUS1p-Regular.ttf',
                                    pos = (20, 420),
                                    multiline=False,  # Single line input
                                    halign='left',
                                    )
        
        partition = SeparatorLine(
            size_hint=(0.6, 0.05),
            pos  = (20,440),
        )
        self.add_widget(self.label)
        self.add_widget(self.text_input)
        self.add_widget(partition)

        self.shift_keys = [
            ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
            ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
            ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
            ['Shift','Z', 'X', 'C', 'V', 'B', 'N', 'M', 'Backspace'],
            ['Japanese', ',', 'Space','.', 'Enter']
        ]
        self.keys = [
            ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
            ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
            ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l'],
            ['Shift', 'z', 'x', 'c', 'v', 'b', 'n', 'm', 'Backspace'],
            ['Japanese', ',', 'Space', '.', 'Enter']
        ]
        self.subkeys = [
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            ['%', "\\", '|', '=', "[", "]", '<', '>', '{', '}'],   # 10 subkeys (correct)
            ['@', '#', '$', '_', '&', '-', '+', '(', ')'],
            [' ', '*', '\"', '\'', ':', ';', '!', '?', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ']
        ]
        self.japanese_keys = [
            ['あ', 'か', 'さ', 'た', 'な', 'は', 'ま', 'や', 'ら', 'わ','Backspace'],
            ['い', 'き', 'し', 'ち', 'に', 'ひ', 'み', '', 'り', 'を', 'Space'],
            ['う', 'く', 'す', 'つ', 'ぬ', 'ふ', 'む', 'ゆ', 'る', 'ん', 'Enter'],
            ['え', 'け', 'せ', 'て', 'ね', 'へ', 'め', '', 'れ', '。', 'Daku-on'],
            ['お', 'こ', 'そ', 'と', 'の', 'ほ', 'も', 'よ', 'ろ', '、','English']
            # Add more rows as needed
        ]
        self.japanese_subkeys = [
            ['ア', 'カ', 'サ', 'タ', 'ナ', 'ハ', 'マ', 'ヤ', 'ラ', 'ワ',''],
            ['イ', 'キ', 'シ', 'チ', 'ニ', 'ヒ', 'ミ', '', 'リ', 'ヲ',''],
            ['ウ', 'ク', 'ス', 'ツ', 'ヌ', 'フ', 'ム', 'ユ', 'ル', 'ン',''],
            ['エ', 'ケ', 'セ', 'テ', 'ネ', 'ヘ', 'メ', '', 'レ', 'ー',''],
            ['オ', 'コ', 'ソ', 'ト', 'ノ', 'ホ', 'モ', 'ヨ', 'ロ', '','']
            # Add more rows as needed
        ]
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
            ('や', 'ゃ', 'ゆ', 'ぇ', 'よ'),
            ('ら', 'り', 'る', 'れ', 'ろ'),
            ('Enter',),
            ('Daku-on',),
            ('わ', 'を', 'ん', 'ー', ''),
            ('、', '。', '?', '!', ''),
            ('English',)
        ]

        self.build_qwerty_keyboard()  # Build the QWERTY keyboard layout
        self.add_widget(self.main_layout)

        overlay = FloatLayout(size_hint=(1, 1))
        self.home_button = IconTextButton(
            text=update_text_language("home"),
            icon_path='images/home.png',
            size_hint=(None, None),
            size=(110, 110),
            pos_hint={'top': 0.95, 'right': 0.97},
            screen_name='menu',
        )
        overlay.add_widget(self.home_button)
        self.add_widget(overlay)  # Add overlay last so it's on top
    
    def build_qwerty_keyboard(self):
        self.language_mode = 'english'  # Set the language mode to English
        key_width = 90
        key_spacing = 8
        self.main_layout.clear_widgets()
        key_width = 90
        key_spacing = 8


        for row, subrow, shift_row in zip(self.keys, self.subkeys, self.shift_keys):
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
                elif key == 'Japanese':
                    btn = RoundedButton(text='', sub_key=sub_key, image=f'images/japanese.png', font_size=24, font_name='fonts/Roboto-Bold.ttf',
                                        background_color=(0.22, 0.45, 0.91, 1), size_hint_x=None, width=key_width*1.5,
                                        function='Japanese',  shift_key='')
                elif key == 'Backspace':
                    btn = RoundedButton(text='', sub_key=sub_key, image='images/backspace.png', font_size=24, font_name='fonts/Roboto-Bold.ttf',
                                        background_color=(0.22, 0.45, 0.91, 1), size_hint_x=None, width=key_width*1.5,
                                        function='Backspace',  shift_key='')
                elif key == 'Enter':
                    btn = RoundedButton(text='', sub_key=sub_key, image='images/enter.png', font_size=24, font_name='fonts/Roboto-Bold.ttf',
                                        background_color=(0.22, 0.45, 0.91, 1), size_hint_x=None, width=key_width*1.5,
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
            self.main_layout.add_widget(row_layout)
    
    def build_japanese_keyboard(self):
        key_width = 77
        key_spacing = 8
        self.main_layout.clear_widgets()  # Clear the main layout
        self.start_index = self.text_input.cursor_index()  # Save the cursor position
        self.entered = False # Flag to indicate if the Enter key has not been pressed to determine the word conversion 
        self.language_mode = 'japanese'  # Set the language mode to Japanese

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
            for key, sub_key in zip(row, subrow):
                btn = None
                if key == 'English':
                    btn = RoundedButton(text='', sub_key=sub_key, image=f'images/english.png', font_size=24, font_name='fonts/MPLUS1p-Regular.ttf',
                                        background_color=(0.22, 0.45, 0.91, 1), size_hint_x=None, width=key_width*1.5,
                                        function='Flick')
                elif key == 'Backspace':
                    btn = RoundedButton(text='', sub_key=sub_key, image='images/backspace.png', font_size=24, font_name='fonts/Roboto-Bold.ttf',
                                        background_color=(0.22, 0.45, 0.91, 1), size_hint_x=None, width=key_width*1.5,
                                        function='Backspace',  shift_key='')
                elif key == 'Enter':
                    btn = RoundedButton(text='', sub_key=sub_key, image='images/enter.png', font_size=24, font_name='fonts/MPLUS1p-Regular.ttf',
                                        background_color=(0.22, 0.45, 0.91, 1), size_hint_x=None, width=key_width*1.5,
                                        function='Enter', on_press=self.press_enter)
                elif key == 'Space':
                    btn = RoundedButton(text='空白/変換', sub_key=sub_key,  font_size=22, font_name='fonts/MPLUS1p-Regular.ttf',
                                        size_hint_x=None, width=key_width*1.5, background_color=(0.22, 0.45, 0.91, 1),
                                        function='Space')
                elif key == 'Daku-on':
                    btn = RoundedButton(text='', sub_key=sub_key, image='images/daku-on.png', font_size=24, font_name='fonts/Roboto-Bold.ttf',
                                        background_color=(0.22, 0.45, 0.91, 1), size_hint_x=None, width=key_width*1.5,
                                        function='Daku-on',  shift_key='')
                else:
                    btn = RoundedButton(text=key, sub_key=sub_key, font_size=24, font_name='fonts/MPLUS1p-Regular.ttf',
                                        size_hint_x=None, width=key_width)
                btn.bind(on_release=self.on_key_release)
                self.japanese_buttons.append(btn)
                row_layout.add_widget(btn)
            self.main_layout.add_widget(row_layout)

    def build_flick_keyboard(self):
        # Example flick mappings for common Japanese columns (10 columns)
        self.main_layout.clear_widgets()  # Clear the main layout
        grid = GridLayout(cols=4, spacing=6, padding=(100,0,100,0), size_hint_y=None, height=300)
        self.overlay = FloatLayout(size_hint=(1, 1))
        for mapping in self.flick_mappings:
            if len(mapping) == 5 and type(mapping[0]) is str:
                btn = FlickKey(mappings=mapping, text_input=self.text_input,actual_text=self.actual_text_input, overlay=self.overlay,
                            size_hint=(None, None), size=(90, 90))
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
                        text='空白/変換', sub_key='', font_size=24, font_name='fonts/MPLUS1p-Regular.ttf',
                        size_hint=(None, None), size=(120, 90), function='Space'
                    )
                elif mapping[0] == 'Daku-on':
                    btn = RoundedButton(
                        text='', sub_key='', image='images/daku-on.png', font_size=24, font_name='fonts/MPLUS1p-Regular.ttf',
                        size_hint=(None, None), size=(90, 90), function='Daku-on'
                    )
                elif mapping[0] == 'English':
                    btn = RoundedButton(
                        text='', sub_key='', image='images/english.png', font_size=24, font_name='fonts/MPLUS1p-Regular.ttf',
                        size_hint=(None, None), size=(120, 90), function='English'
                    )
            btn.bind(on_release=self.on_key_release)
            grid.add_widget(btn)
            grid.bind(minimum_height=grid.setter('height'))

        self.main_layout.add_widget(grid)
        self.add_widget(self.overlay)  # Add the overlay to the main layout

    def on_key_release(self, instance):
        ti = self.text_input #to indicate the position of the input in a word
        ti.focus = True  # Keep the text input focused
        cursor_pos = ti.cursor_index()

        self.text_input.bind(text=self.limit_text_length)  # Bind the text input to limit its length
        if hasattr(instance, 'is_long_press') and instance.is_long_press and instance.sub_key:
            # Insert subkey at cursor position
            self.actual_text_input = self.actual_text_input[:cursor_pos] + instance.sub_key + self.actual_text_input[cursor_pos:]
            if self.visibility:
                ti.text = ti.text[:cursor_pos] + instance.sub_key + ti.text[cursor_pos:]
            else:
                ti.text = ti.text[:cursor_pos] + '*' * len(instance.sub_key) + ti.text[cursor_pos:]
            ti.cursor = (cursor_pos + len(instance.sub_key), 0)
        elif instance.function == 'Space':
            if self.language_mode == 'japanese' and self.start_index < cursor_pos and not self.converting:
                # Convert the text to Kanji using the converter
                self.converting = True
                self.converted_text = self.kanji_converter.convert(ti.text[self.start_index:cursor_pos],n_best=20)
            if self.converting and len(self.converted_text) > 0:
                suggested_text = self.converted_text.pop() if self.converted_text else ti.text[self.start_index:cursor_pos]
                ti.text = ti.text[:self.start_index] + suggested_text + ti.text[cursor_pos:]
                ti.cursor = (ti.cursor_index() + len(suggested_text), 0)
            else:
                self.actual_text_input = self.actual_text_input[:cursor_pos] + ' ' + self.actual_text_input[cursor_pos:]
                if self.visibility:
                    ti.text = ti.text[:cursor_pos] + ' ' + ti.text[cursor_pos:]
                else:
                    ti.text = ti.text[:cursor_pos] + '*' + ti.text[cursor_pos:]
                ti.cursor = (cursor_pos + 1, 0)
        elif instance.function == 'Backspace':
            if cursor_pos > 0:
                self.actual_text_input = self.actual_text_input[:cursor_pos-1] + self.actual_text_input[cursor_pos:]
                ti.text = ti.text[:cursor_pos-1] + ti.text[cursor_pos:]
                ti.cursor = (cursor_pos - 1, 0)
        elif instance.function == "Shift":
                for btn in self.english_buttons:
                    btn.update_shift_text()
        elif instance.function == "Japanese":
            self.build_japanese_keyboard()
        elif instance.function == "English":
            self.build_qwerty_keyboard()
        elif instance.function == "Enter":
            pass
        elif instance.function == 'Flick':
            self.build_flick_keyboard()
        elif instance.function == "Daku-on":
            print(self.actual_text_input)
            print(self.text_input.text)
            self.actual_text_input = self.actual_text_input[:-1] + self.change_dakuon(self.actual_text_input[-1])  # Add Daku-on character
            if self.visibility:
                self.text_input.text = self.text_input.text[:-1] + self.change_dakuon(self.text_input.text[-1]) # Add Daku-on character
        else:
            if self.converting:
                self.converting = False  # Reset the converting flag
                self.start_index = cursor_pos  # Reset the start index
            self.actual_text_input = self.actual_text_input[:cursor_pos] + instance.text + self.actual_text_input[cursor_pos:]
            if self.visibility:
                    self.text_input.text = self.text_input.text[:cursor_pos] + instance.text + self.text_input.text[cursor_pos:]
            else:
                self.text_input.text = self.text_input.text[:cursor_pos] + '*' * len(instance.text) + self.text_input.text[cursor_pos:]
            ti.cursor = (cursor_pos + len(instance.text), 0)

    def press_enter(self, instance):
        if self.enter_callback:
            self.enter_callback(instance)
        App.get_running_app().show_saved_popup()  # Show a popup indicating the settings have been saved

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


class RoundedButton(Button):
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
        self.is_long_press = False
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
                font_name='fonts/MPLUS1p-Regular.ttf'
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

    def on_press(self):
        print(f"Button {self.text} pressed")
        App.get_running_app().play_sound()
        freeze_ui(0.3)


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