from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button  
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from utils.icons import IconTextButton, CircularImageButton, PageIndicator
from utils.config_loader import load_config, update_current_page, update_text_language
from utils.layout import HeaderBar,  SafeScreen , FooterBar


class MenuScreen1(SafeScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.config = load_config('config/settings.json', 'v3_json')
        self.location = self.config.get("location", "")
        volume = self.config.get("volume", 50)
        self.volume = f"{volume}%"
        self.mode = self.check_mode()
        self.alerts = self.has_any_alert()
        self.content_buttons = {}
        self.config_status = [self.location, self.volume, self.mode, self.alerts]

        self.build_ui()
        self.add_widget(self.main_layout)

    def build_ui(self):
        self.main_layout = BoxLayout(orientation='vertical', padding= [30, 30, 30, 10], spacing=10)

        # Layer 1: Header
        header = BoxLayout(orientation='horizontal', size_hint_y=0.20, padding=[0,0,0,0], spacing=10)
        # Left-aligned widget
        header.add_widget(Image(source='images/soundeye.png', 
                                size=(110,110), size_hint_x=None,
                                ))
        # Spacer
        header.add_widget(Widget(size_hint_x=1))  # Spacer

        # Right-aligned buttons in a horizontal BoxLayout
        right_buttons = BoxLayout(orientation='horizontal', padding=0, spacing=20, size_hint_x=None, width=370)

        self.language_button = IconTextButton(
            icon_path='images/language.png',
            text=update_text_language("language"),
            size=(110, 110),
            screen_name='language'  # Navigate to language screen
        )
        right_buttons.add_widget(self.language_button)
        self.monitor_button = IconTextButton(
            icon_path='images/monitor.png',
            text=update_text_language("monitor"),
            size=(110, 110),
            screen_name='monitor',  # Navigate to monitor screen
        )
        right_buttons.add_widget(self.monitor_button)
        self.power_button = IconTextButton(
            icon_path='images/power.png',
            text=update_text_language("power"),
            size=(110, 110),
            screen_name='power'  # Navigate to power screen
        )
        right_buttons.add_widget(self.power_button)
        
        right_buttons.bind(minimum_width=right_buttons.setter('width'))  # Let width fit content


        header.add_widget(right_buttons)

        # Layer 2: Middle content (e.g., 4 buttons)
        content = BoxLayout(orientation='horizontal', spacing=50, size_hint_y=0.35)
        self.content_names = ["Location", "Volume", "Mode", "Alerts"]
        for i in range(4):
            content_name = self.content_names[i].lower()
            content_path = content_name
            if content_name == "mode":
                mode = self.check_mode()
                content_path = self.check_mode_for_image(mode)
            self.content_buttons[content_name] = IconTextButton(
                icon_path=f'images/{content_path}.png',
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
        self.main_layout.add_widget(header)
        self.main_layout.add_widget(Widget(size_hint_y=None, height=60))  # Spacer with 40px height
        self.main_layout.add_widget(content)
        self.main_layout.add_widget(Widget(size_hint_y=None, height=30))  # Spacer with 20px height

        #footer
        self.footer = FooterBar(screen_name='menu2')
        self.main_layout.add_widget(self.footer)


        page_indicator = PageIndicator(num_pages=2, current_page=1, size_hint=(None, None), width=200, height=80)
        page_indicator.pos_hint = {'center_x': 0.5, 'center_y': 0.23}
        self.add_widget(page_indicator)

        time_bar = AnchorLayout(size_hint_y=0.05, )
        self.main_layout.add_widget(time_bar)

    def _update_bg(self, *args):
        self.bg.size = self.size
        self.bg.pos = self.pos

    def check_mode(self):
        """
        Check the current mode and return a string representation.
        """
        mode =  self.config.get("previous_mode", "fall.json")
        mode_config = load_config(f'config/{mode}')
        single_multiple = "multiple" if mode_config.get("mincount", 99) == 99 else "single"
        if mode == "fall.json":
            return f"{update_text_language('fall_mode')} - {update_text_language(f'fall_{single_multiple}')}"
        elif mode == "bed.json":
            return f"{update_text_language('bed_mode')} - {update_text_language(f'bed_{single_multiple}')}"
        else:
            return f"{update_text_language('unknown_mode')}"

    def check_mode_for_image(self, text):
        if text.startswith("Fall") or text.startswith("転倒"):
            return "fall_multiple" if "Multiple" in text else "fall_single"
        elif text.startswith("Bed") or text.startswith("ベッド"):
            return "bed_multiple" if "Multiple" in text else "bed_single"
    
    
    def has_any_alert(self):
        bed_alerts = load_config("config/settings.json", 'bed_json').get("alert_checking", [])
        fall_alerts = load_config("config/settings.json", 'fall_json').get("alert_checking", [])

        # Check if any nested list's first element is 1
        bed_has_alert = any(isinstance(item, list) and len(item) > 0 and item[0] == 1 for item in bed_alerts)
        fall_has_alert = any(isinstance(item, list) and len(item) > 0 and item[0] == 1 for item in fall_alerts)

        if bed_has_alert and fall_has_alert:
            return "Bed Exit & Fall"
        elif bed_has_alert:
            return "Bed Exit"
        elif fall_has_alert:
            return "Fall"
        else:
            return "No Alerts"
        
    def on_pre_enter(self):
        """
        Called when the screen is entered.
        Updates the location, volume, mode, and alerts based on the current configuration.
        """
        self.config = load_config('config/settings.json', 'v3_json')
        self.location = self.config.get("location", "Room 101")
        volume = self.config.get("volume", 50)
        self.volume = f"{volume}%"
        self.mode = self.check_mode()
        self.alerts = self.has_any_alert()
        # Update the config status labels or other UI elements if necessary
        # For example, you might have labels to display these values
        self.update_status()
        update_current_page('menu')
        return [self.location, self.volume, self.mode, self.alerts]
        
        # Update labels or other UI elements if necessary
        # For example, you might have labels to display these values
    
    def update_status(self):
        """
        Update the configuration status labels or other UI elements.
        This method can be customized based on how you want to display the config status.
        """
        # Example: Assuming you have labels for each config status
        self.content_buttons['location'].status.text = self.location
        self.content_buttons['volume'].status.text = str(self.volume)
        self.content_buttons['mode'].status.text = self.mode
        mode_path = self.check_mode_for_image(self.mode)
        # Update the icon image directly if possible
        self.content_buttons['mode'].image.source = f'images/{mode_path}.png'
        self.content_buttons['mode'].status.text = self.mode
        self.content_buttons['alerts'].status.text = self.alerts

    def go_to_location(self, instance):
        self.config = load_config('config/settings.json', 'v3_json')
        if self.config.get('previous_mode', 'fall.json') == 'fall.json':
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


class MenuScreen2(SafeScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Load configuration
        config = load_config('config/settings.json','v3_json')   
        self.device_id = config.get('sensor_ID', 'N/A')
        self.version = config.get('version', 'N/A')
        screen_saver = config.get('screensaver', 160)
        self.screen_saver = f"{screen_saver} {update_text_language('second')}"
        self.wifi_ssid = config.get('wifi_ssid', 'N/A')
        self.timezone = config.get('timezone', 'N/A')
        self.region_address = config.get('region_address', 'N/A')
        self.config_status = [self.screen_saver, self.wifi_ssid, self.timezone, self.region_address]
        self.content_buttons = {}

        self.build_ui()
        self.add_widget(self.main_layout)

        
    def build_ui(self):
        self.main_layout = BoxLayout(orientation='vertical', padding= [30, 30, 30, 10], spacing=10)
        # Layer 1: Header
        header = BoxLayout(orientation='horizontal', size_hint_y=0.20, padding=0, spacing=40)
        # Left-aligned widget
        header.add_widget(Image(source='images/soundeye.png', 
                                size=(110,110), size_hint_x=None,
                                ))

        header.add_widget(Widget(size_hint_x=1))  # Spacer
        # Spacer
        right_buttons = BoxLayout(orientation='horizontal', padding=0, spacing=20, size_hint_x=None, width=370)
        self.language_button = IconTextButton(
            icon_path='images/language.png',
            text=update_text_language("language"),
            size=(110, 110),
            screen_name='language'  # Navigate to language screen
        )
        right_buttons.add_widget(self.language_button)
        self.monitor_button = IconTextButton(
            icon_path='images/monitor.png',
            text=update_text_language("monitor"),
            size=(110, 110),
            screen_name='monitor',  # Navigate to monitor screen
        )
        right_buttons.add_widget(self.monitor_button)
        self.power_button = IconTextButton(
            icon_path='images/power.png',
            text=update_text_language("power"),
            size=(110, 110),
            screen_name='power'  # Navigate to power screen
        )
        right_buttons.add_widget(self.power_button)
        right_buttons.bind(minimum_width=right_buttons.setter('width'))

        header.add_widget(right_buttons)

        # Layer 2: Middle content (e.g., 4 buttons)
                # Layer 2: Middle content (e.g., 4 buttons)
        content = BoxLayout(orientation='horizontal', spacing=50, size_hint_y=0.35)
        content_names = ["Screensaver", "Wi-Fi", "TimeZone", "Servers"]
        image_path = ["screensaver", "wifi", "timezone", "servers"]
        for i in range(4):
            content_name = content_names[i].lower()
            self.content_buttons[content_name] = IconTextButton(
                icon_path=f'images/{image_path[i]}.png',  # Placeholder for icons
                text=update_text_language(content_name),
                config=self.config_status[i],  # Pass config name for loading status
                size=(202, 202),
                screen_name=content_names[i].lower(),  # Navigate to respective screen
            )
            content.add_widget(self.content_buttons[content_name])



        # Combine all layers
        self.main_layout.add_widget(header)
        self.main_layout.add_widget(Widget(size_hint_y=None, height=60))  # Spacer with 40px height
        self.main_layout.add_widget(content)
        self.main_layout.add_widget(Widget(size_hint_y=None, height=30))  # Spacer with 20px height
        self.footer = FooterBar(screen_name='menu')  # Pass screen name for navigation
        self.main_layout.add_widget(self.footer)

        # Page indicator
        page_indicator = PageIndicator(num_pages=2, current_page=2, size_hint=(None, None), width=200, height=80)
        page_indicator.pos_hint = {'center_x': 0.5, 'center_y': 0.23}
        self.add_widget(page_indicator)
        time_bar = AnchorLayout(size_hint_y=0.05)
        self.main_layout.add_widget(time_bar)

    def on_pre_enter(self):
        self.config = load_config('config/settings.json', 'v3_json')
        self.screen_saver = f"{self.config.get('screensaver', 160)} {update_text_language('second')}"
        self.wifi_ssid = self.config.get('wifi_ssid', 'N/A')
        self.timezone = self.config.get('timezone', 'N/A')
        self.region_address = self.config.get('region_address', 'N/A')
        self.config_status = [self.screen_saver, self.wifi_ssid, self.timezone, self.region_address]
        self.update_config_status()
        update_current_page('menu2')


    def update_config_status(self):
        """
        Update the configuration status labels or other UI elements.
        This method can be customized based on how you want to display the config status.
        """
        # Example: Assuming you have labels for each config status
        self.content_buttons['screensaver'].status.text = self.screen_saver
        self.content_buttons['wi-fi'].status.text = self.wifi_ssid
        self.content_buttons['timezone'].status.text = self.timezone
        self.content_buttons['servers'].status.text = self.region_address

    def update_language(self):
        for content_name, button in self.content_buttons.items():
            button.label.text = update_text_language(content_name)
        self.language_button.label.text = update_text_language("language")
        self.monitor_button.label.text = update_text_language("monitor")
        self.power_button.label.text = update_text_language("power")
        self.footer.update_language()
