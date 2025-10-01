from kivy.logger import Logger
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.uix.anchorlayout import AnchorLayout
from kivy.app import App

from as_utils.as_icons import IconTextButton, CircularImageButton, PageIndicator
from as_utils.as_config_loader import load_config, update_current_page, update_text_language, get_valid_value
from as_utils.as_layout import HeaderBar,  SafeScreen , FooterBar

class MenuScreen(SafeScreen):
    '''
    Menu Screen Base Class (Without the main icon part)
    '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.main_layout = BoxLayout(orientation='vertical', padding= [30, 30, 30, 10], spacing=10)

    def build_header(self):
        '''
        Build the header components of the Menu Screen.
        It contains soundeye logo with three button s to go language, monitor and power screen.
        '''
        # Layer 1: Header
        self.header = BoxLayout(orientation='horizontal', size_hint_y=0.20, padding=[0,0,0,0], spacing=10)
        # Left-aligned widget
        self.header.add_widget(Image(source='as_images/soundeye.png', 
                                size=(110,110), size_hint_x=None,
                                ))
        # Spacer
        self.header.add_widget(Widget(size_hint_x=1))  # Spacer

        # Right-aligned buttons in a horizontal BoxLayout
        right_buttons = BoxLayout(orientation='horizontal', padding=0, spacing=20, size_hint_x=None, width=370)

        self.language_button = IconTextButton(
            icon_path='as_images/language.png',
            text=update_text_language("language"),
            size=(110, 110),
            screen_name='language'  # Navigate to language screen
        )
        right_buttons.add_widget(self.language_button)
        self.monitor_button = IconTextButton(
            icon_path='as_images/monitor.png',
            text=update_text_language("monitor"),
            size=(110, 110),
            screen_name='monitor',  # Navigate to monitor screen
        )
        right_buttons.add_widget(self.monitor_button)
        self.power_button = IconTextButton(
            icon_path='as_images/power.png',
            text=update_text_language("power"),
            size=(110, 110),
            screen_name='power'  # Navigate to power screen
        )
        right_buttons.add_widget(self.power_button)
        right_buttons.bind(minimum_width=right_buttons.setter('width'))  # Let width fit content
        self.header.add_widget(right_buttons)
    
    def build_footer(self, screen_name, num_pages, current_page):
        '''
        Build the footer components of the Menu Screen.
        It contains navigation buttons to go to other menu screens and page indicator.'''
        self.footer = FooterBar(screen_name=screen_name)  # Pass screen name for navigation
        self.main_layout.add_widget(self.footer)
        # Page indicator
        page_indicator = PageIndicator(num_pages=num_pages, current_page=current_page, size_hint=(None, None), width=200, height=80)
        page_indicator.pos_hint = {'center_x': 0.5, 'center_y': 0.23}
        self.add_widget(page_indicator)
        time_bar = AnchorLayout(size_hint_y=0.05)
        self.main_layout.add_widget(time_bar)

class MenuScreen1(MenuScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.config = load_config('as_config/settings.json', 'v3_json')
        self.location_config = load_config('as_config/settings.json', 'location_json')
        self.location = get_valid_value(self.location_config, "location", load_config("as_config/settings.json","default_json").get("location", "N/A"))
        volume = self.config.get("volume", 50)
        self.volume = f"{volume}%"
        self.mode = self.check_mode()
        self.alerts = self.has_any_alert()
        self.content_buttons = {}
        self.config_status = [self.location, self.volume, self.mode, self.alerts]
        self.build_ui()
        self.add_widget(self.main_layout)

    def build_ui(self):
        #header
        self.build_header()

        # Layer: Middle content
        content = BoxLayout(orientation='horizontal', spacing=50, size_hint_y=0.35)
        self.content_names = ["Location", "Volume", "Mode", "Alerts"]
        for i in range(4):
            content_name = self.content_names[i].lower()
            content_path = content_name
            if content_name == "mode":
                mode = self.check_mode()
                content_path = self.check_mode_for_image(mode)
            self.content_buttons[content_name] = IconTextButton(
                icon_path=f'as_images/{content_path}.png',
                text=update_text_language(content_name),
                config=self.config_status[i],
                size=(202, 202),
                # Do NOT set screen_name here for dynamic navigation!
            )
            if content_name == 'location':
                self.content_buttons[content_name].bind(on_press=self.go_to_location)
            else:
                # For other buttons, you can still use screen_name if you want
                self.content_buttons[content_name].screen_name = content_name
            content.add_widget(self.content_buttons[content_name])

        # Combine all layers
        self.main_layout.add_widget(self.header)
        self.main_layout.add_widget(Widget(size_hint_y=None, height=60))  # Spacer with 40px height
        self.main_layout.add_widget(content)
        self.main_layout.add_widget(Widget(size_hint_y=None, height=30))  # Spacer with 20px height

        #footer
        self.build_footer(num_pages=2, current_page=1, screen_name='menu2')

    def check_mode(self):
        """
        Check the current mode and return a string representation.
        """
        mode =  self.config.get("previous_mode", "fall.json")
        json_file = mode.replace(".","_")
        mode_config = load_config("as_config/settings.json",json_file)
        single_multiple = "multiple" if mode_config.get("minnumppl_for_noalert", 99) == 99 else "single"
        if mode == "fall.json":
            return f"{update_text_language('fall_mode')} - {update_text_language(f'fall_{single_multiple}')}"
        elif mode == "bed.json":
            return f"{update_text_language('bed_mode')} - {update_text_language(f'bed_{single_multiple}')}"
        else:
            return f"{update_text_language('unknown_mode')}"

    def check_mode_for_image(self, text):
        if text.startswith("Fall") or text.startswith("転倒"):
            return "fall_multiple" if ("Multiple" in text or "複数" in text) else "fall_single"
        elif text.startswith("Bed") or text.startswith("ベッド"):
            return "bed_multiple" if ("Multiple" in text or "複数" in text) else "bed_single"
    
    
    def has_any_alert(self):
        '''
        checks if the current config has any alert enabled and return the appropriate string
        '''
        bed_config = load_config("as_config/settings.json", 'bed_json')
        fall_config = load_config("as_config/settings.json", 'fall_json')
        bed_alerts = bed_config.get("alert_checking", [])
        fall_alerts = fall_config.get("alert_checking", [])
        has_bed_video = bed_config.get("attach_video", 0)
        has_fall_video = fall_config.get("attach_video", 0)

        # Check if any nested list's first element is 1
        bed_has_alert = any(isinstance(item, list) and len(item) > 0 and item[3] == 1 for item in bed_alerts)
        fall_has_alert = any(isinstance(item, list) and len(item) > 0 and item[3] == 1 for item in fall_alerts)

        if (bed_has_alert or has_bed_video) and (fall_has_alert or has_fall_video):
            return "bed_exit_and_fall"
        elif (bed_has_alert or has_bed_video):
            return "bed_exit"
        elif (fall_has_alert or has_fall_video):
            return "fall"
        else:
            return "no_alerts"

    def on_pre_enter(self):
        """
        Called when the screen is entered.
        Updates the location, volume, mode, and alerts based on the current configuration.
        """
        self.config = load_config('as_config/settings.json', 'v3_json')
        self.location_config = load_config("as_config/settings.json", "location_json")
        self.location = get_valid_value(self.location_config, "location", load_config("as_config/settings.json","default_json").get("location", "N/A"))
        self.volume = self.config.get("volume", 50)
        self.mode = self.check_mode()
        self.alerts = self.has_any_alert()
        # Update the config status labels or other UI elements if necessary
        # For example, you might have labels to display these values
        self.update_status()
        update_current_page('menu')
        return [self.location, self.volume, self.mode, self.alerts]
    
    def update_status(self):
        """
        Update the configuration status labels or other UI elements.
        This method can be customized based on how you want to display the config status.
        """
        # Example: Assuming you have labels for each config status
        self.content_buttons['location'].status.text = self.location
        self.content_buttons['volume'].status.text = f"{str(self.volume)}%"
        self.content_buttons['volume'].image.source = "as_images/volume.png" if self.volume != 0 else "as_images/volume_mute.png"
        self.content_buttons['mode'].status.text = self.mode
        mode_path = self.check_mode_for_image(self.mode)
        # Update the icon image directly if possible
        self.content_buttons['mode'].image.source = f'as_images/{mode_path}.png'
        self.content_buttons['mode'].status.text = self.mode
        self.content_buttons['alerts'].status.text = update_text_language(self.alerts)

    def go_to_location(self, instance):
        '''
        depending on the current mode, go to device or location screen
        '''
        self.config = load_config('as_config/settings.json', 'v3_json')
        bed_config = load_config("as_config/settings.json", 'bed_json')
        #Logger.info(f"Current mode: {self.config.get('previous_mode', 'fall.json')}, minnumppl_for_noalert: {bed_config.get('minnumppl_for_noalert',1)}") 
        if self.config.get('previous_mode', 'fall.json') == 'fall.json' or  (self.config.get('previous_mode', 'fall.json') == 'bed.json' and bed_config.get('nbeds')[0] == 1):
            self.manager.current = 'device'
        else:
            self.manager.current = 'location'

    def update_language(self):
        for content_name, button in self.content_buttons.items():
            button.label.text = update_text_language(content_name)
        self.language_button.label.text = update_text_language("language")
        self.monitor_button.label.text = update_text_language("monitor")
        self.power_button.label.text = update_text_language("power")
        self.footer.update_language()


class MenuScreen2(MenuScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Load configuration
        config = load_config('as_config/settings.json','v3_json')   
        self.device_id = config.get('sensor_ID', 'N/A')
        self.version = config.get('version', 'N/A')
        screensaver = config.get('screensaver', 160)
        self.screensaver = f"{screensaver} {update_text_language('second')}"
        self.wifi_ssid = config.get('wifi_ssid', 'N/A')
        self.timezone = config.get('timezone', 'N/A')
        self.region_address = config.get('region_address', 'N/A')
        self.config_status = [self.screensaver, self.wifi_ssid, self.timezone, self.region_address]
        self.content_buttons = {}

        self.build_ui()
        self.add_widget(self.main_layout)

        
    def build_ui(self):
        self.build_header()

        # Layer 2: Middle content (e.g., 4 buttons)
                # Layer 2: Middle content (e.g., 4 buttons)
        content = BoxLayout(orientation='horizontal', spacing=50, size_hint_y=0.35)
        content_names = ["Screensaver", "Wi-Fi", "TimeZone", "Servers"]
        image_path = ["screensaver", "wifi", "timezone", "servers"]
        for i in range(4):
            content_name = content_names[i].lower()
            self.content_buttons[content_name] = IconTextButton(
                icon_path=f'as_images/{image_path[i]}.png',  # Placeholder for icons
                text=update_text_language(content_name),
                config=self.config_status[i],  # Pass config name for loading status
                size=(202, 202),
                screen_name=content_names[i].lower(),  # Navigate to respective screen
            )
            content.add_widget(self.content_buttons[content_name])

        # Combine all layers
        self.main_layout.add_widget(self.header)
        self.main_layout.add_widget(Widget(size_hint_y=None, height=60))  # Spacer with 40px height
        self.main_layout.add_widget(content)
        self.main_layout.add_widget(Widget(size_hint_y=None, height=30))  # Spacer with 20px height
        
        #footer
        self.build_footer(screen_name='menu', num_pages=2, current_page=2)

    def on_pre_enter(self):
        self.config = load_config('as_config/settings.json', 'v3_json')
        self.screensaver =self.config.get('screensaver', 160)
        self.wifi_ssid = self.config.get('wifi_ssid', 'N/A') 
        self.wifi_ssid = update_text_language('not_connected') if self.wifi_ssid == 'Not connected' else self.wifi_ssid
        self.timezone = self.config.get('timezone', 'N/A')
        self.region_address = self.config.get('region_address', 'N/A')
        self.config_status = [self.screensaver, self.wifi_ssid, self.timezone, self.region_address]
        self.update_status()
        update_current_page('menu2')

    def update_status(self):
        """
        Update the configuration status labels or other UI elements.
        This method can be customized based on how you want to display the config status.
        """
        # Example: Assuming you have labels for each config status
        self.content_buttons['screensaver'].status.text = f"{self.screensaver} {update_text_language('second')}"
        self.content_buttons['screensaver'].image.source = "as_images/screensaver.png" if self.screensaver != 0 else "as_images/screensaver_off.png"
        self.content_buttons['wi-fi'].status.text = self.wifi_ssid
        self.content_buttons['wi-fi'].image.source = "as_images/wifi_not_connected.png" if self.wifi_ssid == update_text_language('not_connected') else "as_images/wifi.png"
        self.content_buttons['timezone'].status.text = self.timezone
        self.content_buttons['servers'].status.text = self.region_address

    def update_language(self):
        for content_name, button in self.content_buttons.items():
            button.label.text = update_text_language(content_name)
        self.language_button.label.text = update_text_language("language")
        self.monitor_button.label.text = update_text_language("monitor")
        self.power_button.label.text = update_text_language("power")
        self.footer.update_language()
