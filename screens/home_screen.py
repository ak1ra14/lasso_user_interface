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
        main_layout = BoxLayout(orientation='vertical', padding= 30, spacing=30)

        # Layer 1: Header
        header = BoxLayout(orientation='horizontal', size_hint_y=0.15, padding=0, spacing=10)

        # Left-aligned widget
        header.add_widget(Image(source='images/soundeye.png', size=(200, 200), size_hint_x=None))

        # Spacer
        header.add_widget(Widget())  # Spacer

        # Right-aligned buttons in a horizontal BoxLayout
        right_buttons = BoxLayout(orientation='horizontal', padding=0, spacing=10)

        right_buttons.add_widget(IconTextButton(
            icon_path='images/language.png',
            text="Language",
            size=(90, 90),
            screen_name='language'  # Navigate to language screen
        ))
        right_buttons.add_widget(IconTextButton(
            icon_path='images/monitor.png',
            text="Monitor",
            size=(90, 90),
            screen_name='monitor',  # Navigate to monitor screen
        ))
        right_buttons.add_widget(IconTextButton(
            icon_path='images/power.png',
            text="Power",
            size=(90, 90),
            screen_name='power'  # Navigate to power screen
        ))
        right_buttons.bind(minimum_width=right_buttons.setter('width'))  # Let width fit content


        header.add_widget(right_buttons)

        # Layer 2: Middle content (e.g., 4 buttons)
        content = BoxLayout(orientation='horizontal', spacing=50, size_hint_y=0.25)
        content_names = ["Location", "Volume", "Mode", "Alerts"]
        content.add_widget(Widget())  # Spacer
        for i in range(4):
            content_name = content_names[i].lower()
            content.add_widget(IconTextButton(
                icon_path=f'images/{content_name}.png',  # Placeholder for icons
                text=content_names[i],
                on_press=lambda instance, name=content_names[i]: print(f"Pressed {name}")
            ))
        content.add_widget(Widget())  # Spacer

        # Layer 3: Footer
        footer = GridLayout(cols=5, size_hint_y=0.15,spacing=10)
        footer.add_widget(CircularImageButton(
            image_path="images/left_arrow.png",
            diameter=80,
            screen_name='menu2'  # Navigate to menu2 screen
        ))
        footer.add_widget(Widget())
        footer.add_widget(Widget(width=200))  # Spacer
        footer.add_widget(Widget())
        footer.add_widget(CircularImageButton(
            image_path="images/right_arrow.png",
            diameter=80,
            screen_name='menu2'  # Navigate to menu2 screen
        ))
        footer.add_widget(Label(text="Previous", size_hint_x=None, width=100))
        footer.add_widget(Widget(size_hint_x=None))  # Spacer
        footer.add_widget(Label(text=f"Version: {load_config('config/V3.json').get('version', 'N/A')} | Device ID: {load_config('config/V3.json').get('sensor_ID', 'N/A')}", size_hint_x=None, width=200))
        footer.add_widget(Widget(size_hint_x=None))
        footer.add_widget(Label(text="Next", size_hint_x=None, width=100))

        # Combine all layers
        main_layout.add_widget(header)
        main_layout.add_widget(content)
        main_layout.add_widget(footer)

        self.add_widget(main_layout)

    def _update_bg(self, *args):
        self.bg.size = self.size
        self.bg.pos = self.pos

    def go_to_menu2(self, instance):
        self.manager.current = 'menu2'
    
    def go_to_monitor(self, instance):
        self.manager.current = 'monitor'

    def go_to_language(self, instance):
        self.manager.current = 'language'
    
class MenuScreen2(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Load configuration
        config = load_config('config/V3.json')   
        device_id = config.get('sensor_ID', 'N/A')
        version = config.get('version', 'N/A')


        main_layout = BoxLayout(orientation='vertical', padding = 30, spacing=30)
        # Layer 1: Header
        header = BoxLayout(orientation='horizontal', size_hint_y=0.15, padding=0, spacing=10)
        # Left-aligned widget
        left_layout = BoxLayout(orientation='horizontal', size_hint_x=None, width=350)
        left_layout.add_widget(Image(source='images/soundeye.png', size=(100,100), size_hint_x=None))
        left_layout.add_widget(Label(
            text=f"Version: {version} | Device ID: {device_id}",
            font_size=15,
            size_hint_x=1,  # Let label take remaining space
        ))
        header.add_widget(left_layout)
        header.add_widget(Widget(width=100))  # Spacer
        # Spacer
        right_buttons = BoxLayout(orientation='horizontal', padding=0, spacing=10)
        right_buttons.bind(minimum_width=right_buttons.setter('width'))
        right_buttons.add_widget(IconTextButton(
            icon_path='images/language.png',
            text="Language",
            size=(90, 90),
            screen_name='language'  # Navigate to language screen
        ))
        right_buttons.add_widget(IconTextButton(
            icon_path='images/monitor.png',
            text="Monitor",
            size=(90, 90),
            screen_name='monitor',  # Navigate to monitor screen
        ))
        right_buttons.add_widget(IconTextButton(
            icon_path='images/power.png',
            text="Power",
            size=(90,90),
            screen_name='power'  # Navigate to power screen
        ))
        header.add_widget(right_buttons)
        main_layout.add_widget(header)

        # Layer 2: Middle content (e.g., 4 buttons)
                # Layer 2: Middle content (e.g., 4 buttons)
        content = BoxLayout(orientation='horizontal', spacing=50, size_hint_y=0.25)
        content_names = ["Screensaver", "Wi-fi", "Time Zone", "Servers"]
        image_path = ["screen_saver", "wifi", "timezone", "servers"]
        content.add_widget(Widget(size_hint_x=None))  # Spacer
        for i in range(4):
            content.add_widget(IconTextButton(
                icon_path=f'images/{image_path[i]}.png',  # Placeholder for icons
                text=content_names[i],
                screen_name=content_names[i].lower(),  # Navigate to respective screen
            ))
        content.add_widget(Widget(size_hint_x=None))  # Spacer
        main_layout.add_widget(content)

        # Layer 3: Footer

        footer = GridLayout(cols=5, size_hint_y=0.15)

        footer.add_widget(CircularImageButton(
            image_path="images/left_arrow.png",
            diameter=80,
            screen_name='menu',  # Navigate to menu1 screen
        ))
        footer.add_widget(Widget(width = 10))

        footer.add_widget(Widget(width=600))
        footer.add_widget(Widget(width=10))
        # Spacer
        footer.add_widget(CircularImageButton(
            image_path="images/right_arrow.png",
            diameter=80,
            screen_name='menu',  # Navigate to menu1 screen
        ))

        footer.add_widget(Label(text="Previous", size_hint_x=None, width=100))
        footer.add_widget(Widget(size_hint_x=None))  # Spacer
        footer.add_widget(Label(text=f"Version: {load_config('config/V3.json').get('version', 'N/A')} | Device ID: {load_config('config/V3.json').get('sensor_ID', 'N/A')}", size_hint_x=None, width=200))
        footer.add_widget(Widget(size_hint_x=None))
        footer.add_widget(Label(text="Next", size_hint_x=None, width=100))

        main_layout.add_widget(footer)
        self.add_widget(main_layout)    

        # Let width fit content
    def go_to_menu(self, instance):
        self.manager.current = 'menu'

    def go_to_monitor(self, instance):
        self.manager.current = 'monitor'

    def go_to_language(self, instance):
        self.manager.current = 'language'   

    def go_to(self, instance, screen_name):
        self.manager.current = screen_name
