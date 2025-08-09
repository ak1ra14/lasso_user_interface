from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from utils.layout import HeaderBar, SafeScreen
from utils.config_loader import load_config
from utils.icons import IconTextButton
from kivy.graphics import Line, Color, Rectangle
from utils.keyboard import KeyboardScreen
from utils.config_loader import save_config, update_current_page, update_text_language
from utils.layout import SeparatorLine
from utils.num_pad import NumberPadScreen
from kivy.app import App


class ServerScreen(SafeScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.config = load_config('config/settings.json', 'v3_json')
        self.buttons = {}
        self.build_ui()

    def build_ui(self):
        self.header = HeaderBar(title="servers", icon_path="images/home.png", button_text="home", button_screen="menu2")
        self.main_layout = FloatLayout(size_hint=(1, 1))
        self.main_layout.add_widget(self.header)

        #self.region_server = Label(text=update_text_language("region_server"), font_size=35, height=40,pos_hint={'center_x': 0.13 if App.get_running_app().language == 'en' else 0.17, 'center_y': 0.68},font_name='fonts/MPLUS1p-Bold.ttf', halign='left')
        self.region_server = Label(text=update_text_language("region_server"), font_size=35, height=40,
                                   size_hint=(None, None), size=(300, 40),
                                    pos=(5, 385) if App.get_running_app().language == 'en' else (30, 385),  # Absolute positioning
                                   font_name='fonts/MPLUS1p-Bold.ttf', halign='left')

        self.buttons['region_address'] = EditSetting( status = self.config.get('region_address'), screen_name = 'region server', pos_hint={'center_x': 0.20, 'center_y': 0.55},
                                                     )
        self.main_layout.add_widget(self.region_server)
        self.mqtt = Label(text=update_text_language('mqtt'), font_size=40, size_hint_y=None, height=40, pos_hint={'center_x': 0.446, 'center_y': 0.7}, font_name='fonts/MPLUS1p-Bold.ttf'
                            , halign='left')
        self.main_layout.add_widget(self.mqtt)
        self.mqtt_broker_ip = Label(text=update_text_language('mqtt_broker_ip'), font_size=25, size_hint_y=None, height=40, pos_hint={'center_x': 0.48, 'center_y': 0.62}, font_name='fonts/MPLUS1p-Bold.ttf', halign='left')
        self.main_layout.add_widget(self.mqtt_broker_ip)
        self.mqtt_topic = Label(text=update_text_language('mqtt_topic'), font_size=25, size_hint_y=None, height=40, 
                                size_hint=(None, None), size=(300, 40),
                                pos=(340, 185) if App.get_running_app().language == 'en' else (360, 185),  # Absolute positioning
                                font_name='fonts/MPLUS1p-Bold.ttf',halign='left')
        self.main_layout.add_widget(self.mqtt_topic)

        self.buttons['mqtt_address'] = EditSetting( status = self.config.get('mqtt_address'), screen_name = 'mqtt broker ip', pos_hint={'center_x': 0.50, 'center_y': 0.55})
        self.buttons['mqtt_topic'] = EditSetting( status = self.config.get('mqtt_topic'), screen_name = 'mqtt topic', pos_hint={'center_x': 0.50, 'center_y': 0.25})


        self.alert_lights = Label(text=update_text_language("alert_lights"), font_size=35, size_hint_y=None, height=40,
                                   size_hint=(None, None), size=(300, 40),
                                   pos=(605, 385) if App.get_running_app().language == 'en' else (625, 385),  # Absolute positioning
                                   font_name='fonts/MPLUS1p-Bold.ttf', halign='left')
        self.main_layout.add_widget(self.alert_lights)
        self.buttons['alert_lights_ip1'] = EditSetting( status = self.config.get('alert_lights_ip1'), screen_name = 'alert lights 1', pos_hint={'center_x': 0.80, 'center_y': 0.55})
        self.buttons['alert_lights_ip2'] = EditSetting( status = self.config.get('alert_lights_ip2'), screen_name = 'alert lights 2', pos_hint={'center_x': 0.80, 'center_y': 0.30})

        for button in self.buttons.values():
            self.main_layout.add_widget(button)

        # Add a separator line
        separator_1 = SeparatorLine(points=[350,450,350,250],size_hint =(None,None))
        self.main_layout.add_widget(separator_1)
        separator_2 = SeparatorLine(points=[665, 450, 665, 250], size_hint=(None, None))
        self.main_layout.add_widget(separator_2)
        self.add_widget(self.main_layout)

    def on_pre_enter(self):
        """
        This method is called before the screen is displayed.
        It can be used to update the UI or perform any necessary actions.
        """
        update_current_page('server')
        self.config = load_config('config/settings.json', 'v3_json')
        for key, button in self.buttons.items():
            button.status = self.config.get(key, '')
            button.label.text = button.status

    def update_language(self):
        self.clear_widgets()
        self.build_ui()
        # self.header.update_language()
        # for key, button in self.buttons.items():
        #     button.label.text = update_text_language(key)
        #     button.button.label.text = update_text_language('edit')
        #     button.label.bind(size=lambda inst, val: setattr(inst, 'text_size', (inst.width, None)))
        #     button.button.bind(text=lambda inst, val: setattr(inst, 'text', update_text_language('edit')))
        # self.region_server.text = update_text_language("region_server")
        # self.mqtt.text = update_text_language('mqtt')
        # self.mqtt_broker_ip.text = update_text_language('mqtt_broker_ip')
        # self.mqtt_topic.text = update_text_language('mqtt_topic')
        # self.alert_lights.text = update_text_language("alert_lights")

class EditSetting(FloatLayout):
    def __init__(self, status, screen_name,**kwargs):
        super().__init__(**kwargs)
        self.status = status
        self.screen_name = screen_name
        self.build_ui()

    def build_ui(self):
        self.button = IconTextButton(
            text=update_text_language("edit"),
            font_size=20,
            radius=[10,],
            size_hint=(None, None),
            size=(120, 40),
            pos_hint = {'center_x': 0.45, 'center_y': 0.5},
            screen_name=self.screen_name
        )
        self.label = Label(
            text=self.status,
            font_size=18,
            size_hint=(None, None),
            height=30,
            width = 200,
            pos_hint = {'center_x': 0.5, 'center_y': 0.42},
            font_family='fonts/MPLUS1p-Bold.ttf',
            shorten=True,
            shorten_from='right',
            max_lines=1,
            halign='left',
            valign='middle',
        )
        self.label.bind(size=lambda inst, val: setattr(inst, 'text_size', val))
        with self.canvas:
            self.label.color = (1, 1, 1, 1) # Text color
            self.label.text_size = self.label.size
            self.line1 = Line(points=[self.label.x - 10, self.label.y, self.label.x + self.label.width, self.label.y], width=1)
            self.line2 = Line(points=[self.label.x - 10, self.label.y, self.label.x - 10, self.label.y + self.label.height], width=1)
            self.line3 = Line(points=[self.label.x - 10, self.label.y + self.label.height, self.label.x + self.label.width, self.label.y + self.label.height], width=1)
            self.line4 = Line(points=[self.label.x + self.label.width, self.label.y, self.label.x + self.label.width, self.label.y + self.label.height], width=1)
        self.label.bind(pos=self.update_line, size=self.update_line)
        self.add_widget(self.button)
        self.add_widget(self.label)


    def update_line(self, *args):
        x1 = self.label.x - 10
        y1 = self.label.y + self.label.height 
        x2 = self.label.x + self.label.width
        y2 = self.label.y
        self.line1.points = [x1, y1, x2, y1]
        self.line2.points = [x1, y1, x1, y2]
        self.line3.points = [x1, y2, x2, y2]
        self.line4.points = [x2, y1, x2, y2]

class RegionServerScreen(NumberPadScreen):
    def __init__(self, **kwargs):
        super().__init__(title="region_address", **kwargs)
        self.config = load_config("config/settings.json", "v3_json")
        self.text = self.config.get('region_address', '')

    def on_save(self, instance):
        """
        Override the on_save method to save the region address.
        """
        self.config['region_address'] = self.input.text
        save_config("config/settings.json", "v3_json", data=self.config)

    def on_pre_enter(self):
        """
        Override the on_pre_enter method to set the keyboard title.
        """
        update_current_page('region_server')
        self.config = load_config("config/settings.json", "v3_json")
        self.input.text = self.config.get("region_address", "")
    

class MQTTBrokerIPScreen(NumberPadScreen):
    def __init__(self, **kwargs):
        super().__init__(title="mqtt_broker_ip", **kwargs)
        self.config = load_config("config/settings.json", "v3_json")
        self.text = self.config.get('mqtt_address', '')

    def on_save(self, instance):
        """
        Override the on_save method to save the MQTT broker address.
        """
        self.config['mqtt_address'] = self.input.text
        save_config("config/settings.json", "v3_json", data=self.config)

    def on_pre_enter(self):
        """
        Override the on_pre_enter method to set the keyboard title.
        """
        update_current_page('mqtt_broker_ip')
        self.config = load_config("config/settings.json", "v3_json")
        self.input.text = self.config.get("mqtt_address", "")

class AlertLight1Screen(NumberPadScreen):
    def __init__(self, **kwargs):
        super().__init__(title="alert_lights_ip1", **kwargs)
        self.config = load_config("config/settings.json", "v3_json")
        self.text = self.config.get('alert_lights_ip1', '')

    def on_save(self, instance):
        """
        Override the on_save method to save the alert light 1 address.
        """
        self.config['alert_lights_ip1'] = self.input.text
        save_config("config/settings.json", "v3_json", data=self.config)

    def on_pre_enter(self):
        """
        Override the on_pre_enter method to set the keyboard title.
        """
        update_current_page('alert_light_1')
        self.config = load_config("config/settings.json", "v3_json")
        self.input.text = self.config.get("alert_lights_ip1", "")


class AlertLight2Screen(NumberPadScreen):
    def __init__(self, **kwargs):
        super().__init__(title="alert_lights_ip2", **kwargs)
        self.config = load_config("config/settings.json", "v3_json")
        self.text = self.config.get('alert_lights_ip2', '')

    def on_save(self, instance):
        """
        Override the on_save method to save the alert light 2 address.
        """
        self.config['alert_lights_ip2'] = self.input.text
        save_config("config/settings.json", "v3_json", data=self.config)

    def on_pre_enter(self):
        """
        Override the on_pre_enter method to set the keyboard title.
        """
        update_current_page('alert_light_2')
        self.config = load_config("config/settings.json", "v3_json")
        self.input.text = self.config.get("alert_lights_ip2", "")


class MQTTTopicKeyboardScreen(KeyboardScreen):
    def __init__(self, **kwargs):
        super().__init__(title="mqtt_topic", **kwargs)
        self.config = load_config("config/settings.json", "v3_json")
        self.text = self.config.get('mqtt_topic', '')

    def press_enter(self, instance):
        """
        Override the on_enter method to set the keyboard title.
        """
        self.config['mqtt_topic'] = self.keyboard.text_input.text
        save_config("config/settings.json", "v3_json", data=self.config)

    def on_pre_enter(self):
        """
        Override the on_pre_enter method to set the keyboard title.
        """
        self.keyboard.title = "MQTT Topic"
        self.config = load_config("config/settings.json", "v3_json")
        self.keyboard.text_input.text = self.config.get("mqtt_topic", "")
