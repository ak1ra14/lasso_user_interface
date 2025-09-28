import json
from kivy.logger import Logger
from utils.layout import HeaderBar, SafeScreen
from utils.config_loader import load_config, save_config, update_current_page, update_text_language, get_valid_value
from utils.icons import IconTextButton
from utils.num_pad import NumberPadScreen
from utils.keyboard import KeyboardScreen, show_saved_popup
from kivy.app import App


class LocationScreen(SafeScreen):
    def __init__(self, **kwargs):
        super(LocationScreen, self).__init__(**kwargs)
        self.config = load_config("config/settings.json", "v3_json")
        self.location_config = load_config("config/settings.json", "location_json")
        self.bed_config = load_config("config/settings.json", "bed_json")
        self.bed_no = self.bed_config.get("nbeds", [1,[' ']])[0]
        # Create a layout for the keypad
    
    def build_ui(self):
        self.header = HeaderBar(title="location", icon_path="images/home.png", button_text="home", button_screen="menu")
        self.add_widget(self.header)

        if self.bed_no == 2:
            self.location_icon2 = IconTextButton(
                text=update_text_language('location'),
                config = get_valid_value(self.location_config, 'location', load_config("config/settings.json","default_json").get("location", "N/A")),
                font_size=18,
                icon_path="images/location.png",
                size_hint=(None, None),
                size=(200, 200),
                pos_hint={'center_x': 0.25, 'center_y': 0.5},
                screen_name='device'
            )
            self.add_widget(self.location_icon2)
            self.bed1_icon2 = IconTextButton(
                text=update_text_language('bed_1'),
                config = self.bed_config.get('nbeds', [1,[' ']])[1][0],
                font_size=18,
                icon_path="images/bed.png",
                size_hint=(None, None),
                size=(200, 200),
                pos_hint={'center_x': 0.5, 'center_y': 0.5},
                screen_name='bed1'
            )
            self.add_widget(self.bed1_icon2)
            self.bed2_icon = IconTextButton(
                text=update_text_language('bed_2'),
                config = self.bed_config.get('nbeds', [1,[' ']])[1][1],
                font_size=18,
                icon_path="images/bed.png",
                size_hint=(None, None),
                size=(200, 200),
                pos_hint={'center_x': 0.75, 'center_y': 0.5},
                screen_name='bed2'
            )
            self.add_widget(self.bed2_icon)

    def on_leave(self):
        self.clear_widgets()

    def on_pre_enter(self):
        """
        This method is called before the screen is displayed.
        It can be used to update the UI or perform any necessary actions.
        """
        update_current_page('location')
        self.config = load_config("config/settings.json", "v3_json")
        self.location_config = load_config("config/settings.json", "location_json")
        self.bed_config = load_config("config/settings.json", "bed_json")
        self.bed_no = self.bed_config.get("nbeds", [1, [' ']])[0]
        self.build_ui()
    
class Bed1Screen(KeyboardScreen):
    def __init__(self, **kwargs):
        super().__init__(title='bed_1', **kwargs)
        self.title = 'bed_1'
        self.config = load_config("config/settings.json", "bed_json")
        self.text = self.config.get("nbeds", [1, [' ']])[1][0]

    def press_enter(self, instance):
        """
        Override the on_enter method to set the keyboard title.
        """    
        self.config['nbeds'][1][0] = self.keyboard.text_input.text
        save_config("config/settings.json", "bed_json", self.config)
        show_saved_popup(update_text_language('saved'))  # Show a popup indicating the settings have been saved

    def on_pre_enter(self):
        """
        Override the on_pre_enter method to set the keyboard title.
        """
        update_current_page('bed1')
        self.config = load_config("config/settings.json", "bed_json")
        self.keyboard.text_input.text = self.config.get("nbeds", [1, ['Bed 1']])[1][0]
        self.keyboard.actual_text_input = self.keyboard.text_input.text
        super().on_pre_enter()


class Bed2Screen(KeyboardScreen):
    def __init__(self, **kwargs):
        super().__init__(title="bed_2", **kwargs)
        self.title = 'bed_2'
        self.config = load_config("config/settings.json", "bed_json")
        # self.text = self.config.get("nbeds", [1, [' ']])[1][1]

    def press_enter(self, instance):
        """
        Override the on_enter method to set the keyboard title.
        """    
        self.config['nbeds'][1][1] = self.keyboard.text_input.text
        save_config("config/settings.json", "bed_json", self.config)
        show_saved_popup(update_text_language('saved'))

    def on_pre_enter(self):
        """
        Override the on_pre_enter method to set the keyboard title.
        """
        self.keyboard.title = update_text_language('bed_2')
        self.config = load_config("config/settings.json", "bed_json")
        self.keyboard.text_input.text = self.config.get("nbeds", [2, [1, 2]])[1][1]
        self.keyboard.actual_text_input = self.keyboard.text_input.text
        super().on_pre_enter()


class DeviceKeyboardScreen(KeyboardScreen):
    def __init__(self, **kwargs):
        super().__init__(title="device_location", **kwargs)
        self.title = 'device_location'
        self.location_config = load_config("config/settings.json", "location_json")
        self.text = get_valid_value(self.location_config, 'location', load_config("config/settings.json","default_json").get("location", "N/A"))
        self.update_default_location()

    
    def press_enter(self, instance):
        """
        Override the on_enter method to set the keyboard title.
        """
        if self.location_config:
            if not self.check_all_location_values_same("config/settings.json",'location_json', self.location_config.get('location',None)):
                self.location_config['location'] = self.keyboard.text_input.text
                save_config("config/settings.json", "location_json", data=self.location_config)
            else:
                self.update_all_location_values("config/settings.json",'location_json', self.keyboard.text_input.text)
        show_saved_popup(update_text_language('saved'))

    def on_pre_enter(self):
        """
        Override the on_pre_enter method to set the keyboard title.
        """
        update_current_page('device_keyboard')
        self.config = load_config("config/settings.json", "v3_json")
        self.keyboard.text_input.text = get_valid_value(self.location_config, 'location', load_config("config/settings.json","default_json").get("location", "N/A"))
        self.keyboard.actual_text_input = self.keyboard.text_input.text
        super().on_pre_enter()

    def update_default_location(self):
        if self.location_config:
            default_values = load_config("config/settings.json","default_json")
            default_values['location'] = self.location_config.get('location', default_values.get('location', 'N/A'))
            Logger.info('saving default location')
            save_config("config/settings.json","default_json", default_values)

    def check_all_location_values_same(self,file_path, variable_name='location_json',value_to_check=None):
        with open(file_path, "r") as f:
            data = json.load(f)
        if variable_name:
            next_path = data.get(variable_name)
        all_same = True
        if isinstance(next_path, list):
            for path in next_path:
                with open(path, "r") as f:
                    config = json.load(f)
                    location_value = config.get('location', None)
                if location_value != value_to_check:
                    return False
        return all_same

    def update_all_location_values(self,file_path, variable_name='location_json', new_value=None):
        with open(file_path, "r") as f:
            data = json.load(f)
        if variable_name:
            next_path = data.get(variable_name)
        if isinstance(next_path, list):
            for path in next_path:
                with open(path, "r") as f:
                    config = json.load(f)
                config['location'] = new_value
                with open(path, "w") as f:
                    json.dump(config, f, indent=4)



