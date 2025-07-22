from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.clock import Clock
from utils.config_loader import load_config
from utils.layout import HeaderBar
from utils.icons import IconTextButton
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from utils.layout import Footer1Bar, Footer2Bar
class MonitorScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        btn = Button(text="Go to Menu")
        btn.bind(on_press=self.go_to_menu)
        self.add_widget(btn)

    def go_to_menu(self, instance):
        print("Button clicked, going to Menu")
        Clock.schedule_once(lambda dt: setattr(self.manager, 'current', 'test3'), 0)

class TestScreen(Screen):
    def __init__(self, **kwargs):
        super(TestScreen, self).__init__(**kwargs)
        print("TestScreen initialized")
        # self.config = load_config('config/V3.json')  # Read once
        # self.location = self.config.get("location", "Room 101")
        # volume = self.config.get("volume", 50)

        # Add header bar
        self.header = HeaderBar(title="Test Screen")
        self.add_widget(self.header)
        self.add_widget(
            IconTextButton(
                text="Back to Monitor",
                icon_path="images/home.png",
                size_hint=(None, None),
                size=(200, 50),
                pos_hint={'center_x': 0.5, 'top': 1},
                on_press=self.go_to_monitor
            )
        )

class TestScreen2(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.config = load_config('config/V3.json')
        self.location = self.config.get("location", "Room 101")
        volume = self.config.get("volume", 50)
        self.volume = f"{volume}%"
        self.content_buttons = {}


        main_layout = BoxLayout(orientation='vertical', padding= [30, 30, 30, 10], spacing=10)

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
        for i in range(4):
            content_name = content_names[i].lower()

            self.content_buttons[content_name] = IconTextButton(
                icon_path=f'images/{content_name}.png',  # Placeholder for icons
                text=content_names[i],
                config='test',  # Pass config name
                size=(202, 202),
                screen_name=content_name,  # Navigate to respective screen
            )
            content.add_widget(self.content_buttons[content_name])

        # Combine all layers
        main_layout.add_widget(header)
        main_layout.add_widget(Widget(size_hint_y=None, height=60))  # Spacer with 40px height
        main_layout.add_widget(content)
        main_layout.add_widget(Widget(size_hint_y=None, height=30))  # Spacer with 20px height
        
        #footer
        main_layout.add_widget(Footer1Bar(screen_name='menu2'))  # Pass screen name for navigation
        main_layout.add_widget(Footer2Bar())

        time_bar = AnchorLayout(size_hint_y=0.05, )
        time_bar.add_widget(Label(text="Time Bar Placeholder",
                                size_hint_y=None, height=50,
                                pos_hint={'center_x': 0.5, 'center_y': 0.5},
                                font_size=20))
        main_layout.add_widget(time_bar)
        self.add_widget(main_layout) 

class TestScreen3(Screen):
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

        main_layout = BoxLayout(orientation='vertical', padding= [30, 30, 30, 10], spacing=10)

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
        for i in range(4):
            content_name = content_names[i].lower()
            content_path = content_name
            if content_name == "mode":
                mode = self.check_mode()
                content_path = self.check_mode_for_image(mode)
            self.content_buttons[content_name] = IconTextButton(
                icon_path=f'images/{content_path}.png',  # Placeholder for icons
                text=content_names[i],
                config=self.config_status[i],  # Pass config name
                size=(202, 202),
                screen_name=content_name,  # Navigate to respective screen
            )
            content.add_widget(self.content_buttons[content_name])

        # Combine all layers
        main_layout.add_widget(header)
        main_layout.add_widget(Widget(size_hint_y=None, height=60))  # Spacer with 40px height
        main_layout.add_widget(content)
        main_layout.add_widget(Widget(size_hint_y=None, height=30))  # Spacer with 20px height
        
        #footer
        main_layout.add_widget(Footer1Bar(screen_name='menu2'))  # Pass screen name for navigation
        main_layout.add_widget(Footer2Bar())

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
        self.content_buttons['mode'].image.source = f'images/{mode_path}.png'
        self.content_buttons['mode'].status.text = self.mode
        self.content_buttons['alerts'].status.text = self.alerts

class TestApp(App):
    def build(self):
        self.config = load_config('config/V3.json')
        self.location = self.config.get("location", "Room 101")
        volume = self.config.get("volume", 50)
        sm = ScreenManager()
        sm.add_widget(MonitorScreen(name='monitor'))
        sm.add_widget(TestScreen3(name='test3'))
        return sm

TestApp().run()