from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from utils.icons import IconTextButton
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from utils.config_loader import load_config, save_config, update_current_page, update_text_language
from kivy.uix.gridlayout import GridLayout
from kivy.app import App
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from utils.layout import HeaderBar, SafeScreen
import json

class TimezoneScreen(SafeScreen):
    def __init__(self, **kwargs):
        """
        Timezone screen for the Soundeye application.
        This screen allows users to select a timezone.
        """
        super().__init__(**kwargs)
        self.selected_timezone = load_config('config/settings.json', 'v3_json').get('timezone', '')
        self.timezone_list = []
        header = HeaderBar(title="timezone", icon_path="images/home.png", button_text="home", button_screen="menu2")

        ##main layout
        main = BoxLayout(orientation='horizontal', size_hint=(1,0.75),
                          padding=[50, 50, 50, 0], spacing=100, 
                          pos_hint={'center_x': 0.5, 'center_y': 0.5})
        main.bind(minimum_height=main.setter('height'))  # Ensure height is set correctly
        main.bind(minimum_width=main.setter('width'))  # Ensure width is set correctly
        main.add_widget(Widget(size_hint_y=1))  # Spacer
        list_box = GridLayout(cols=1, size=(465, 800), size_hint=(None,None), pos_hint=(None, None),)
        for tz in ["Singapore (GMT+8)", "Japan (GMT+9)", "Los Angeles (GMT-7)",]:
            button = SelectableButton(text=tz, font_size=40,
                                                font_family='fonts/Roboto-Bold.ttf', size_hint_y=None, 
                                                height=55, selection=self)
            list_box.add_widget(button)
            self.timezone_list.append(button)
            
        scroll = ScrollView(size_hint=(None, None),
                            scroll_type=['bars', 'content'],
                            bar_width=35, 
                            bar_color=(0.2, 0.6, 0.8, 1),  # Active bar color (blue)
                            bar_inactive_color=(0.7, 0.7, 0.7, 1),  # Inactive bar color (gray)
                            size=(500,300),
                            do_scroll_x=False)
        with scroll.canvas.before:
            Color(1, 1, 1, 1)  # White
            rect = Rectangle(pos=scroll.pos, size=scroll.size)
        scroll.bind(pos=lambda instance, value: setattr(rect, 'pos', value))
        scroll.bind(size=lambda instance, value: setattr(rect, 'size', value))
                
        scroll.add_widget(list_box)

        main.add_widget(scroll)

        self.save_button = TZSaveButton(text = update_current_page("save"), icon_path="images/save.png", 
                                     tz_screen=self,
                                     screen_name='menu2',
                                     pos_hint={'center_x': 0.8, 'center_y': 0.4},
                                     size_hint=(None, None), size=(120, 120))

        main.add_widget(Widget(size_hint_y=1))  # Spacer
        self.add_widget(self.save_button)
        self.add_widget(header)
        self.add_widget(main)  # Optional: add a spacer below if you want space at the bottom

    def select_timezone(self, btn):
        for b in self.timezone_list:
            if b == btn:
                continue
            b.selected = False
            b.update_color()
        btn.selected = True
        btn.update_color()
        self.selected_timezone = btn.text

    def on_pre_enter(self):
        update_current_page('timezone')
        self.save_button.label_text = update_text_language('save')

    def update_language(self):
        """
        Update the language of the screen elements.
        """
        self.header.update_language()
        self.save_button.label.text = update_text_language('save')

class SelectableButton(Button):
    """
    A button that can be selected or deselected.
    """
    def __init__(self, text,selection, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.selection = selection  # Reference to the selection manage
        self.selected = (selection.selected_timezone == text)  # Check if this button's timezone is the selected one
        self.background_normal = ''
        self.background_down = ''
        self.background_color = (1, 1, 1, 1)
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_rect, size=self._update_rect)
        self.update_color()
        #self.bind(on_release=self.on_press)
    
    def _update_rect(self, *args):
        """
        Update the rectangle size and position when the button is resized or moved.
        """
        self.rect.pos = self.pos
        self.rect.size = self.size

    def update_color(self):
        print(self.text, "selected:", self.selected)
        if self.selected:
            self.color = (1, 1, 1, 1)
            self.background_color = (0.2, 0.6, 0.8, 1)
        else:
            self.color = (0, 0, 0, 1)
            self.background_color = (1, 1, 1, 1)

    def on_press(self):
        """
        Override the on_press method to handle button press.
        """
        super().on_press()
        self.selection.selected_timezone = self.text
        print(f"Selected timezone: {self.text}")
        self.selection.select_timezone(self)

class TZSaveButton(IconTextButton):
    def __init__(self,tz_screen = None,screen_name=None,**kwargs):
        """
        Button to save the selected timezone.
        """
        super().__init__(**kwargs)
        self.tz_screen = tz_screen
        self.screen_name = screen_name
    
    def on_press(self):
        super().on_press()
        print(f"Saving timezone: {self.tz_screen.selected_timezone}")
        config = load_config('config/settings.json', 'v3_json')
        config['timezone'] = self.tz_screen.selected_timezone
        save_config('config/settings.json', 'v3_json', data=config)


        

