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

class MenuScreen1(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        main_layout = BoxLayout(orientation='vertical', padding= [30, 30, 30, 10], spacing=10)

        # Layer 1: Header
        header = BoxLayout(orientation='horizontal', size_hint_y=0.20, padding=[0,0,0,0], spacing=10)
        # Left-aligned widget
        header.add_widget(Image(source='images/soundeye.png', 
                                size=(110,110), size_hint_x=None,
                                keep_ratio=True, allow_stretch=True))
        # Spacer
        header.add_widget(Widget(size_hint_x=1))  # Spacer

        # Right-aligned buttons in a horizontal BoxLayout
        right_buttons = BoxLayout(orientation='horizontal', padding=0, spacing=20, size_hint_x=None, width=370)

        right_buttons.add_widget(IconTextButton(
            icon_path='images/language.png',
            text="Language",
            size=(110, 110),
            screen_name='language'  # Navigate to language screen
        ))
        right_buttons.add_widget(IconTextButton(
            icon_path='images/monitor.png',
            text="Monitor",
            size=(110, 110),
            screen_name='monitor',  # Navigate to monitor screen
        ))
        right_buttons.add_widget(IconTextButton(
            icon_path='images/power.png',
            text="Power",
            size=(110, 110),
            screen_name='power'  # Navigate to power screen
        ))
        right_buttons.bind(minimum_width=right_buttons.setter('width'))  # Let width fit content


        header.add_widget(right_buttons)

        # Layer 2: Middle content (e.g., 4 buttons)
        content = BoxLayout(orientation='horizontal', spacing=50, size_hint_y=0.35)
        content_names = ["Location", "Volume", "Mode", "Alerts"]
        config_names = ["location", "volume", "placeholder", "placeholder"]  # Placeholder for alerts
        for i in range(4):
            content_name = content_names[i].lower()
            content.add_widget(IconTextButton(
                icon_path=f'images/{content_name}.png',  # Placeholder for icons
                text=content_names[i],
                config=config_names[i],  # Pass config name
                size=(202, 202),
                screen_name=content_name,  # Navigate to respective screen
            ))

        # Layer 3: Footer
        footer1 = BoxLayout(orientation='horizontal', size_hint_y=0.15, padding=0, spacing=0)
        footer1.add_widget(CircularImageButton(
            image_path="images/left_arrow.png",
            diameter=80,
            screen_name='menu2'  # Navigate to menu2 screen
        ))
        center = AnchorLayout(anchor_x='center', anchor_y='center', size_hint_x=1)
        center.add_widget(Label(text="Page indicator Placeholder",))
        footer1.add_widget(center)
        footer1.add_widget(CircularImageButton(
            image_path="images/right_arrow.png",
            diameter=80,
            screen_name='menu2'  # Navigate to menu2 screen
        ))

        footer2 = BoxLayout(orientation='horizontal', size_hint_y=0.05, padding=0, spacing=10)
        footer2.add_widget(Label(text="Previous", size_hint_x=None, width=100))
        footer2.add_widget(Label(text=f"Version: {load_config('config/V3.json').get('version', 'N/A')} | Device ID: {load_config('config/V3.json').get('sensor_ID', 'N/A')}",size_hint_x =1) )
        footer2.add_widget(Label(text="Next", size_hint_x=None, width=100))


        # Combine all layers
        main_layout.add_widget(header)
        main_layout.add_widget(Widget(size_hint_y=None, height=60))  # Spacer with 40px height
        main_layout.add_widget(content)
        main_layout.add_widget(Widget(size_hint_y=None, height=30))  # Spacer with 20px height
        main_layout.add_widget(footer1)
        main_layout.add_widget(footer2)

        time_bar = AnchorLayout(size_hint_y=0.05, )
        time_bar.add_widget(Label(text="Time Bar Placeholder",
                                size_hint_y=None, height=50,
                                pos_hint={'center_x': 0.5, 'center_y': 0.5},
                                font_size=20))
        main_layout.add_widget(time_bar)
        self.add_widget(main_layout)

    def _update_bg(self, *args):
        self.bg.size = self.size
        self.bg.pos = self.pos


    
class MenuScreen2(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Load configuration
        config = load_config('config/V3.json')   
        device_id = config.get('sensor_ID', 'N/A')
        version = config.get('version', 'N/A')


        main_layout = BoxLayout(orientation='vertical', padding= [30, 30, 30, 10], spacing=10)
        # Layer 1: Header
        header = BoxLayout(orientation='horizontal', size_hint_y=0.20, padding=0, spacing=40)
        # Left-aligned widget
        left_layout = BoxLayout(orientation='horizontal', size_hint=(0.5,None),height = 100,spacing=10)
        left_layout.add_widget(Image(source='images/soundeye.png', size=(100,100), size_hint_x=None))
        left_layout.add_widget(Label(
            text=f"Version: {version} | Device ID: {device_id}",
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
            icon_path='images/language.png',
            text="Language",
            size=(110,110),
            screen_name='language'  # Navigate to language screen
        ))
        right_buttons.add_widget(IconTextButton(
            icon_path='images/monitor.png',
            text="Monitor",
            size=(110, 110),
            screen_name='monitor',  # Navigate to monitor screen
        ))
        right_buttons.add_widget(IconTextButton(
            icon_path='images/power.png',
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
        config_names = ["screensaver", "wifi_ssid", "timezone", "mqtt_address"]
        for i in range(4):
            content.add_widget(IconTextButton(
                icon_path=f'images/{image_path[i]}.png',  # Placeholder for icons
                text=content_names[i],
                config=config_names[i],  # Pass config name for loading status
                size=(202, 202),
                screen_name=content_names[i].lower(),  # Navigate to respective screen
            ))

        # Layer 3: Footer
        footer1 = BoxLayout(orientation='horizontal', size_hint_y=0.15, padding=0, spacing=0)
        footer1.add_widget(CircularImageButton(
            image_path="images/left_arrow.png",
            diameter=80,
            screen_name='menu'  # Navigate to menu2 screen
        ))
        center = AnchorLayout(anchor_x='center', anchor_y='center', size_hint_x=1)
        center.add_widget(Label(text="Page indicator Placeholder",))
        footer1.add_widget(center)
        footer1.add_widget(CircularImageButton(
            image_path="images/right_arrow.png",
            diameter=80,
            screen_name='menu'  # Navigate to menu2 screen
        ))

        footer2 = BoxLayout(orientation='horizontal', size_hint_y=0.05, padding=0, spacing=10)
        footer2.add_widget(Label(text="Previous", size_hint_x=None, width=100))
        footer2.add_widget(Label(text=f"Version: {load_config('config/V3.json').get('version', 'N/A')} | Device ID: {load_config('config/V3.json').get('sensor_ID', 'N/A')}",size_hint_x =1) )
        footer2.add_widget(Label(text="Next", size_hint_x=None, width=100))


        # Combine all layers
        main_layout.add_widget(header)
        main_layout.add_widget(Widget(size_hint_y=None, height=60))  # Spacer with 40px height
        main_layout.add_widget(content)
        main_layout.add_widget(Widget(size_hint_y=None, height=30))  # Spacer with 20px height
        main_layout.add_widget(footer1)
        main_layout.add_widget(footer2)

        time_bar = AnchorLayout(size_hint_y=0.05, )
        time_bar.add_widget(Label(text="Time Bar Placeholder",
                                size_hint_y=None, height=50,
                                pos_hint={'center_x': 0.5, 'center_y': 0.5},
                                font_size=20))
        main_layout.add_widget(time_bar)
        self.add_widget(main_layout)