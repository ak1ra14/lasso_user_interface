import json
from kivy.logger import Logger
from kivy.app import App

from as_utils.as_layout import HeaderBar, SafeScreen
from as_utils.as_config_loader import load_config, update_current_page, update_text_language, get_valid_value, save_config_partial, check_all_values_same, update_all_values
from as_utils.as_icons import IconTextButton
from as_utils.as_num_pad import NumberPadScreen
from as_utils.as_keyboard import KeyboardScreen, show_saved_popup


class LocationScreen(SafeScreen):
    def __init__(self, **kwargs):
        super(LocationScreen, self).__init__(**kwargs)
        self.config = load_config("as_config/settings.json", "v3_json")
        self.location_config = load_config("as_config/settings.json", "location_json")
        self.bed_config = load_config("as_config/settings.json", "bed_json")
        self.bed_no = self.bed_config.get("nbeds", [1,[' ']])[0]
        # Create a layout for the keypad
    
    def build_ui(self):
        self.header = HeaderBar(title="location", icon_path="as_images/home.png", button_text="home", button_screen="menu")
        self.add_widget(self.header)

        if self.bed_no == 2:
            self.location_icon2 = IconTextButton(
                text=update_text_language('location'),
                config = get_valid_value(self.location_config, 'location', load_config("as_config/settings.json","default_json").get("location", "N/A")),
                font_size=18,
                icon_path="as_images/location.png",
                size_hint=(None, None),
                size=(200, 200),
                pos_hint={'center_x': 0.25, 'center_y': 0.5},
                screen_name='device',
                button_mode = 'icon_status'
            )
            self.add_widget(self.location_icon2)
            self.bed1_icon2 = IconTextButton(
                text=update_text_language('bed_1'),
                config = self.bed_config.get('nbeds', [1,[' ']])[1][0],
                font_size=18,
                icon_path="as_images/bed.png",
                size_hint=(None, None),
                size=(200, 200),
                pos_hint={'center_x': 0.5, 'center_y': 0.5},
                screen_name='bed1',
                button_mode = 'icon_status'
            )
            self.add_widget(self.bed1_icon2)
            self.bed2_icon = IconTextButton(
                text=update_text_language('bed_2'),
                config = self.bed_config.get('nbeds', [1,[' ']])[1][1],
                font_size=18,
                icon_path="as_images/bed.png",
                size_hint=(None, None),
                size=(200, 200),
                pos_hint={'center_x': 0.75, 'center_y': 0.5},
                screen_name='bed2',
                button_mode = 'icon_status'
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
        self.config = load_config("as_config/settings.json", "v3_json")
        self.location_config = load_config("as_config/settings.json", "location_json")
        self.bed_config = load_config("as_config/settings.json", "bed_json")
        self.bed_no = self.bed_config.get("nbeds", [1, [' ']])[0]
        self.build_ui()
    
class Bed1Screen(KeyboardScreen):
    def __init__(self, **kwargs):
        super().__init__(title='bed_1', **kwargs)
        self.title = 'bed_1'
        self.config = load_config("as_config/settings.json", "bed_json")
        self.text = self.config.get("nbeds", [1, [' ']])[1][0]

    def press_enter(self, instance):
        """
        Override the on_enter method to set the keyboard title.
        """    
        self.config['nbeds'][1][0] = self.keyboard.text_input.text
        nbeds_value = self.config['nbeds']
        save_config_partial("as_config/settings.json", "bed_json", key = 'nbeds', value=nbeds_value)
        show_saved_popup(update_text_language('saved'))  # Show a popup indicating the settings have been saved

    def on_pre_enter(self):
        """
        Override the on_pre_enter method to set the keyboard title.
        """
        update_current_page('bed1')
        self.config = load_config("as_config/settings.json", "bed_json")
        self.keyboard.text_input.text = self.config.get("nbeds", [1, ['Bed 1']])[1][0]
        self.keyboard.actual_text_input = self.keyboard.text_input.text
        super().on_pre_enter()


class Bed2Screen(KeyboardScreen):
    def __init__(self, **kwargs):
        super().__init__(title="bed_2", **kwargs)
        self.title = 'bed_2'
        self.config = load_config("as_config/settings.json", "bed_json")
        # self.text = self.config.get("nbeds", [1, [' ']])[1][1]

    def press_enter(self, instance):
        """
        Override the on_enter method to set the keyboard title.
        """    
        self.config['nbeds'][1][1] = self.keyboard.text_input.text
        nbeds_value = self.config['nbeds']
        save_config_partial("as_config/settings.json", "bed_json", key = 'nbeds', value=nbeds_value)
        show_saved_popup(update_text_language('saved'))

    def on_pre_enter(self):
        """
        Override the on_pre_enter method to set the keyboard title.
        """
        self.keyboard.title = update_text_language('bed_2')
        self.config = load_config("as_config/settings.json", "bed_json")
        self.keyboard.text_input.text = self.config.get("nbeds", [2, [1, 2]])[1][1]
        self.keyboard.actual_text_input = self.keyboard.text_input.text
        super().on_pre_enter()


class DeviceKeyboardScreen(KeyboardScreen):
    def __init__(self, **kwargs):
        super().__init__(title="device_location", **kwargs)
        self.title = 'device_location'
        self.location_config = load_config("as_config/settings.json", "location_json")
        self.text = get_valid_value(self.location_config, 'location', load_config("as_config/settings.json","default_json").get("location", "N/A"))
        self.update_default_location()

    
    def press_enter(self, instance):
        """
        Override the on_enter method to set the keyboard title.
        """
        self.location_config = load_config("as_config/settings.json", "location_json")
        if self.location_config:
            if not check_all_values_same("as_config/settings.json",'location_json',key='location', value_to_check= self.location_config.get('location',None)):
                save_config_partial("as_config/settings.json", "location_json", key='location',value=self.keyboard.text_input.text)
            else:
                update_all_values("as_config/settings.json",'location_json', key='location',new_value= self.keyboard.text_input.text)   
        show_saved_popup(update_text_language('saved'))

    def on_pre_enter(self):
        """
        Override the on_pre_enter method to set the keyboard title.
        """
        update_current_page('device_keyboard')
        self.config = load_config("as_config/settings.json", "v3_json")
        self.location_config = load_config("as_config/settings.json", "location_json")
        self.keyboard.text_input.text = get_valid_value(self.location_config, 'location', load_config("as_config/settings.json","default_json").get("location", "N/A"))
        self.keyboard.actual_text_input = self.keyboard.text_input.text
        super().on_pre_enter()

    def update_default_location(self):
        if self.location_config:
            default_values = load_config("as_config/settings.json","default_json")
            default_values['location'] = self.location_config.get('location', default_values.get('location', 'N/A'))
            #Logger.debug('saving default location')
            save_config_partial("as_config/settings.json","default_json", key='location',value=self.location_config.get('location', default_values.get('location', 'N/A')))




