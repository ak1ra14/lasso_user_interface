from kivy.uix.screenmanager import Screen
from utils.layout import HeaderBar
from utils.config_loader import load_config, save_config
from kivy.uix.floatlayout import FloatLayout
from utils.icons import IconTextButton
from utils.num_pad import NumberPadScreen
from utils.keyboard import KeyboardScreen

class LocationScreen(Screen):
    def __init__(self, **kwargs):
        super(LocationScreen, self).__init__(**kwargs)
        self.config = load_config("config/V3.json")            
        self.bed_config = load_config("config/bed.json")

        self.bed_no = self.bed_config.get("nbeds", [1,[' ']])[0]
        # Create a layout for the keypad
        header = HeaderBar(title="Location", icon_path="images/home.png", button_text="Home", button_screen="menu")
        self.add_widget(header)

        if self.bed_no == 1:
            self.add_widget(IconTextButton(
                text="Bed 1",
                config = self.bed_config.get("nbeds", [1,[' ']])[1][0],
                font_size=18,
                icon_path="images/bed.png",
                size_hint=(None, None),
                size=(200, 200),
                pos_hint={'center_x': 0.5, 'center_y': 0.5},
                screen_name='numpad'
            ))
        elif self.bed_no == 2:
            self.add_widget(IconTextButton(
                text="Bed 1",
                config = self.bed_config.get("nbeds", [1,[' ']])[1][0],
                font_size=18,
                icon_path="images/bed.png",
                size_hint=(None, None),
                size=(200, 200),
                pos_hint={'center_x': 0.3, 'center_y': 0.5},
                screen_name='bed1'
            ))
            self.add_widget(IconTextButton(
                text="Bed 2",
                config = self.bed_config.get("nbeds", [1,[' ']])[1][1],
                font_size=18,
                icon_path="images/bed.png",
                size_hint=(None, None),
                size=(200, 200),
                pos_hint={'center_x': 0.7, 'center_y': 0.5},
                screen_name='bed2'
            ))

        

class Bed1KeyboardScreen(KeyboardScreen):
    def __init__(self, **kwargs):
        super().__init__(title="Bed Location 1", **kwargs)
        self.config = load_config("config/bed.json")
        self.text = self.config.get("nbeds", [1, [' ']])[1][0]
    
    def press_enter(self,instance):
        """
        Override the on_enter method to set the keyboard title.
        """    
        self.config['nbeds'][1][0] = self.keyboard.text_input.text
        save_config("config/bed.json", self.config)

    def on_pre_enter(self):
        """
        Override the on_pre_enter method to set the keyboard title.
        """
        self.config = load_config("config/bed.json")
        self.keyboard.text_input.text = self.config.get("nbeds", [1, [' ']])[1][0]


class Bed2KeyboardScreen(KeyboardScreen):
    def __init__(self, **kwargs):
        super().__init__(title="Bed Location 2", **kwargs)
        self.config = load_config("config/bed.json")
        self.text = self.config.get("nbeds", [1, [' ']])[1][1]
    
    def press_enter(self, instance):
        """
        Override the on_enter method to set the keyboard title.
        """    
        self.config['nbeds'][1][1] = self.keyboard.text_input.text
        save_config("config/bed.json", self.config)
    
    def on_pre_enter(self):
        """
        Override the on_pre_enter method to set the keyboard title.
        """
        self.config = load_config("config/bed.json")
        self.keyboard.text_input.text = self.config.get("nbeds", [1, [' ']])[1][1]

class DeviceKeyboardScreen(KeyboardScreen):
    def __init__(self, **kwargs):
        super().__init__(title="Device Location", **kwargs)
        self.config = load_config("config/V3.json")
        self.text = self.config.get('location', 'Room 1')
    
    def press_enter(self, instance):
        """
        Override the on_enter method to set the keyboard title.
        """
        self.config['location'] = self.keyboard.text_input.text
        save_config("config/V3.json", self.config)

    def on_pre_enter(self):
        """
        Override the on_pre_enter method to set the keyboard title.
        """
        self.config = load_config("config/V3.json")
        self.keyboard.text_input.text = self.config.get("location", "Room 1")
