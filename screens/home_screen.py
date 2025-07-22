from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button  
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from utils.icons import IconTextButton, CircularImageButton
from utils.config_loader import load_config
from utils.layout import HeaderBar, Footer1Bar, Footer2Bar

class MenuScreen1(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.config = load_config('config/V3.json')
        self.location = self.config.get("location", "Room 101")
        volume = self.config.get("volume", 50)
        self.volume = f"{volume}%"
        self.mode = self.check_mode()
        self.alerts = self.has_any_alert()
        self.content_buttons = {}
        self.config_status = [self.location, self.volume, self.mode, self.alerts]
        self.main_layout = None


    def _update_bg(self, *args):
        self.bg.size = self.size
        self.bg.pos = self.pos


    def check_mode(self):
        """
        Check the current mode and return a string representation.
        """
        mode =  self.config.get("previous_mode", "fall.json")
        mode_config = load_config(f'config/{mode}')
        single_multiple = "Multiple" if mode_config.get("mincount", 99) == 99 else "Single"
        if mode == "fall.json":
            return f"Fall - {single_multiple}"
        elif mode == "bed.json":
            return f"Bed Exit - {single_multiple}"
        else:
            return f"Unknown Mode - {single_multiple}"
        
    def check_mode_for_image(self, text):
        if text.startswith("Fall"):
            return "fall_multiple" if "Multiple" in text else "fall_single"
        elif text.startswith("Bed"):
            return "bed_multiple" if "Multiple" in text else "bed_single"
    
    
    def has_any_alert(self):
        bed_alerts = load_config("config/bed.json").get("alert_checking", [])
        fall_alerts = load_config("config/fall.json").get("alert_checking", [])

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
        self.config = load_config('config/V3.json')
        self.location = self.config.get("location", "Room 101")
        volume = self.config.get("volume", 50)
        self.volume = f"{volume}%"
        self.mode = self.check_mode()
        self.alerts = self.has_any_alert()
        if not self.main_layout:
            self.build_ui()
            self.add_widget(self.main_layout)
        # Update the config status labels or other UI elements if necessary
        # For example, you might have labels to display these values
        self.update_status()
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
        self.content_buttons['mode'].image.source = 'atlas://data/images/defaulttheme/audio-volume-high'
        self.content_buttons['mode'].status.text = self.mode
        self.content_buttons['alerts'].status.text = self.alerts

    def build_ui(self):
        """
        Build the UI for the MenuScreen1.
        This method can be called to refresh the UI elements if needed.
  
      """
        self.main_layout = BoxLayout(orientation='vertical', padding= [30, 30, 30, 10], spacing=10)

        # Layer 1: Header
        header = BoxLayout(orientation='horizontal', size_hint_y=0.20, padding=[0,0,0,0], spacing=10)
        # Left-aligned widget
        header.add_widget(Image(source='atlas://data/images/defaulttheme/audio-volume-high', 
                                size=(110,110), size_hint_x=None,
                                ))
        # Spacer
        header.add_widget(Widget(size_hint_x=1))  # Spacer

        # Right-aligned buttons in a horizontal BoxLayout
        right_buttons = BoxLayout(orientation='horizontal', padding=0, spacing=20, size_hint_x=None, width=370)

        right_buttons.add_widget(IconTextButton(
            icon_path='atlas://data/images/defaulttheme/audio-volume-high',
            text="Language",
            size=(110, 110),
            screen_name='language'  # Navigate to language screen
        ))
        right_buttons.add_widget(IconTextButton(
            icon_path='atlas://data/images/defaulttheme/audio-volume-high',
            text="Monitor",
            size=(110, 110),
            screen_name='monitor',  # Navigate to monitor screen
        ))
        right_buttons.add_widget(IconTextButton(
            icon_path='atlas://data/images/defaulttheme/audio-volume-high',
            text="Power",
            size=(110, 110),
            screen_name='power'  # Navigate to power screen
        ))
        right_buttons.bind(minimum_width=right_buttons.setter('width'))  # Let width fit content


        header.add_widget(right_buttons)

        # Layer 2: Middle content (e.g., 4 buttons)
        content = BoxLayout(orientation='horizontal', spacing=50, size_hint_y=0.35)
        content_names = ["Location", "Volume", "Mode", "Alerts"]
        for i in range(4):
            content_name = content_names[i].lower()
            content_path = content_name
            if content_name == "mode":
                mode = self.check_mode()
                content_path = self.check_mode_for_image(mode)
            self.content_buttons[content_name] = IconTextButton(
                icon_path='atlas://data/images/defaulttheme/audio-volume-high',  # Placeholder for icons
                text=content_names[i],
                config=self.config_status[i],  # Pass config name
                size=(202, 202),
                screen_name=content_name,  # Navigate to respective screen
            )
            content.add_widget(self.content_buttons[content_name])

        # Combine all layers
        self.main_layout.add_widget(header)
        self.main_layout.add_widget(Widget(size_hint_y=None, height=60))  # Spacer with 40px height
        self.main_layout.add_widget(content)
        self.main_layout.add_widget(Widget(size_hint_y=None, height=30))  # Spacer with 20px height
        
        #footer
        self.main_layout.add_widget(Footer1Bar(screen_name='menu2'))  # Pass screen name for navigation
        self.main_layout.add_widget(Footer2Bar())

        time_bar = AnchorLayout(size_hint_y=0.05, )
        time_bar.add_widget(Label(text="Time Bar Placeholder",
                                size_hint_y=None, height=50,
                                pos_hint={'center_x': 0.5, 'center_y': 0.5},
                                font_size=20))
        self.main_layout.add_widget(time_bar)

class MenuScreen2(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Load configuration
        config = load_config('config/V3.json')   
        self.device_id = config.get('sensor_ID', 'N/A')
        self.version = config.get('version', 'N/A')
        screen_saver = config.get('screensaver', 160)
        self.screen_saver = f"{screen_saver} s"
        self.wifi_ssid = config.get('wifi_ssid', 'N/A')
        self.timezone = config.get('timezone', 'N/A')
        self.mqtt_address = config.get('mqtt_address', 'N/A')
        self.config_status = [self.screen_saver, self.wifi_ssid, self.timezone, self.mqtt_address]
        self.content_buttons = {}

        main_layout = BoxLayout(orientation='vertical', padding= [30, 30, 30, 10], spacing=10)
        # Layer 1: Header
        header = BoxLayout(orientation='horizontal', size_hint_y=0.20, padding=0, spacing=40)
        # Left-aligned widget
        left_layout = BoxLayout(orientation='horizontal', size_hint=(0.5,None),height = 100,spacing=10)
        left_layout.add_widget(Image(source='atlas://data/images/defaulttheme/audio-volume-high', size=(100,100), size_hint_x=None))
        left_layout.add_widget(Label(
            text=f"Version: {self.version} | Device ID: {self.device_id}",
            font_size=15,
            size_hint_x=None,
            width=300,  # Let label take remaining space
            valign="top",  # Vertically center text
        ))
        left_layout.add_widget(Widget())  # Spacer to fill remaining space
        header.add_widget(left_layout)
        header.add_widget(Widget(size_hint_x=1))  # Spacer
        # Spacer
        right_buttons = BoxLayout(orientation='horizontal', padding=0, spacing=20, size_hint_x=None, width=370)
        right_buttons.add_widget(IconTextButton(
            icon_path='atlas://data/images/defaulttheme/audio-volume-high',
            text="Language",
            size=(110,110),
            screen_name='language'  # Navigate to language screen
        ))
        right_buttons.add_widget(IconTextButton(
            icon_path='atlas://data/images/defaulttheme/audio-volume-high',
            text="Monitor",
            size=(110, 110),
            screen_name='monitor',  # Navigate to monitor screen
        ))
        right_buttons.add_widget(IconTextButton(
            icon_path='atlas://data/images/defaulttheme/audio-volume-high',
            text="Power",
            size=(110, 110),
            screen_name='power'  # Navigate to power screen
        ))
        right_buttons.bind(minimum_width=right_buttons.setter('width'))

        header.add_widget(right_buttons)

        # Layer 2: Middle content (e.g., 4 buttons)
                # Layer 2: Middle content (e.g., 4 buttons)
        content = BoxLayout(orientation='horizontal', spacing=50, size_hint_y=0.35)
        content_names = ["Screensaver", "Wi-fi", "Time Zone", "Servers"]
        image_path = ["screen_saver", "wifi", "timezone", "servers"]
        for i in range(4):
            content_name = content_names[i].lower()
            self.content_buttons[content_name] = IconTextButton(
                icon_path='atlas://data/images/defaulttheme/audio-volume-high',  # Placeholder for icons
                text=content_names[i],
                config=self.config_status[i],  # Pass config name for loading status
                size=(202, 202),
                screen_name=content_names[i].lower(),  # Navigate to respective screen
            )
            content.add_widget(self.content_buttons[content_name])



        # Combine all layers
        main_layout.add_widget(header)
        main_layout.add_widget(Widget(size_hint_y=None, height=60))  # Spacer with 40px height
        main_layout.add_widget(content)
        main_layout.add_widget(Widget(size_hint_y=None, height=30))  # Spacer with 20px height
        main_layout.add_widget(Footer1Bar(screen_name='menu'))  # Pass screen name for navigation
        main_layout.add_widget(Footer2Bar())

        time_bar = AnchorLayout(size_hint_y=0.05, )
        time_bar.add_widget(Label(text="Time Bar Placeholder",
                                size_hint_y=None, height=50,
                                pos_hint={'center_x': 0.5, 'center_y': 0.5},
                                font_size=20))
        main_layout.add_widget(time_bar)
        self.add_widget(main_layout)

    def on_pre_enter(self):
        self.config = load_config('config/V3.json')
        self.screen_saver = f"{self.config.get('screensaver', 160)} s"
        self.wifi_ssid = self.config.get('wifi_ssid', 'N/A')
        self.timezone = self.config.get('timezone', 'N/A')
        self.mqtt_address = self.config.get('mqtt_address', 'N/A')
        self.config_status = [self.screen_saver, self.wifi_ssid, self.timezone, self.mqtt_address]
        self.update_config_status()

    def update_config_status(self):
        """
        Update the configuration status labels or other UI elements.
        This method can be customized based on how you want to display the config status.
        """
        # Example: Assuming you have labels for each config status
        self.content_buttons['screensaver'].status.text = self.screen_saver
        self.content_buttons['wi-fi'].status.text = self.wifi_ssid
        self.content_buttons['time zone'].status.text = self.timezone
        self.content_buttons['servers'].status.text = self.mqtt_address