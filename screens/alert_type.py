from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from utils.icons import IconTextButton, ToggleButton
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import BooleanProperty
from kivy.app import App
from kivy.core.audio import SoundLoader
from utils.layout import SeparatorLine 
from utils.layout import HeaderBar
from utils.icons import ToggleButton, CustomSwitch
from utils.config_loader import load_config, save_config, update_current_page
class AlertTypeScreen(Screen):
    def __init__(self, **kwargs):
        super(AlertTypeScreen, self).__init__(**kwargs)
        self.config = load_config('config/settings.json','v3_json')
        self.ack_enable = self.config.get("ack_enable", 'Yes')
        self.bed_json = load_config("config/settings.json",'bed_json')
        self.fall_json = load_config("config/settings.json",'fall_json')
        self.attach_video_bed = self.bed_json.get("attach_video", 1)
        self.attach_video_fall = self.fall_json.get("attach_video", 1)
        self.alert_checking_bed = self.bed_json.get("alert_checking", None)
        self.alert_checking_fall = self.fall_json.get("alert_checking", None)
        header = HeaderBar(title="Alert Type", icon_path="images/home.png", button_text="Home", button_screen="menu")
        self.buttons = []
        self.add_widget(header)

        ack_button_text = 1 if self.ack_enable == "yes" else 0
        ack_button = ToggleButton(
            text_right="Auto-acknowledgement alert",
            size_hint_y=None,
            height=50,
            switch = AlertTypeButton(ack_button_text),
            text_size_l_r=(0,350),
            pos=(50, 340),
        )
        self.buttons.append(ack_button)

        image = Image(
            source="images/bed_single.png",
            size_hint=(None, None),
            size=(70,70),
            pos = (70, 260)
        )
        y_axis = [220, 175, 130, 85, 40]
        bed_types = ["Alert with video", "Sit up","Bed exit","Sit-to-Stand","Fall besides bed"]
        for i, bed_type in enumerate(bed_types):
            if i == 0:
                value = self.attach_video_bed 
            else:
                value = self.alert_checking_bed[i-1][0] if self.alert_checking_bed else 0
            button = ToggleButton(
                text_right=bed_type,
                size_hint_y=None,
                height=50,
                pos=(50, y_axis[i]),
                switch=AlertTypeButton(value),
                text_size_l_r=(0, 150)
            )
            self.add_widget(button)
            self.buttons.append(button)
        partition = SeparatorLine(
            points=[370, 300, 370, 40],
            size_hint=(None, None),
        )
        
        fall_image = Image(
            source="images/fall_single.png",
            size_hint=(None, None),
            size=(50,50),
            pos = (420, 265)
        )
        for i, bed_type in enumerate(["Alert without video","Sit-to-Stand","Fall"]):
            if i == 0:
                value = self.attach_video_bed 
            else:
                value = self.alert_checking_fall[i-1][0] if self.alert_checking_fall else 0
            button = ToggleButton(
                text_right=bed_type,
                size_hint_y=None,
                height=50,
                switch=AlertTypeButton(value),
                pos=(400, y_axis[i]),
                text_size_l_r=(0, 200)
            )
            self.add_widget(button)
            self.buttons.append(button)

        float_layout = FloatLayout(size_hint=(1, 1))
        save_button = SaveButtonAT(
            icon_path="images/save.png",
            text="Save",
            size_hint=(None, None),
            size=(120, 120),
            pos_hint = None,
            pos=(800, 140),
            AT_screen=self,
            screen_name="menu"
        )
        float_layout.add_widget(save_button)
        self.add_widget(float_layout)
        self.add_widget(partition)
        self.add_widget(image)
        self.add_widget(ack_button)
        self.add_widget(fall_image)

    def on_pre_enter(self):
        update_current_page('alert_type')
        status = []
        self.config = load_config('config/settings.json','v3_json')
        ack_enable = self.config.get("ack_enable", 'yes')
        status.append(1 if ack_enable == "yes" else 0)
        self.bed_json = load_config("config/settings.json",'bed_json')
        self.fall_json = load_config("config/settings.json",'fall_json')
        attach_video_bed = self.bed_json.get("attach_video", 1)
        status.append(attach_video_bed)
        alert_checking_bed = self.bed_json.get("alert_checking", None)
        if alert_checking_bed:
            for item in alert_checking_bed:
                status.append(item[0])
        attach_video_fall = self.fall_json.get("attach_video", 1)
        status.append(attach_video_fall)
        alert_checking_fall = self.fall_json.get("alert_checking", None)
        if alert_checking_fall:
            for item in alert_checking_fall:
                status.append(item[0])

        for i in range(len(self.buttons)):
            self.buttons[i].switch.active = status[i]
            self.buttons[i].switch.update_graphics()


class AlertTypeButton(CustomSwitch):

    active = BooleanProperty(False)
    def __init__(self, value, **kwargs):
        super().__init__(**kwargs)
        self.active = True if value == 1 else False

class SaveButtonAT(IconTextButton):
    def __init__(self, AT_screen, **kwargs):
        super().__init__(**kwargs)
        self.icon_path = "images/save.png"
        self.size_hint = (None, None)
        self.size = (120, 120)
        self.pos = (800, 140)
        self.screen_name = "menu"
        self.AT_screen = AT_screen

    def on_press(self):
        config_v3 = load_config('config/settings.json','v3_json')
        ack_enable = "yes" if self.AT_screen.buttons[0].switch.active else "no"
        config_v3['ack_enable'] = ack_enable
        save_config('config/settings.json','v3_json', data=config_v3)


        config_bed = load_config("config/settings.json",'bed_json')
        attach_video_bed = 1 if self.AT_screen.buttons[1].switch.active else 0
        config_bed['attach_video'] = attach_video_bed

        # Save alert checking configurations
        alert_checking_bed = []
        for button in self.AT_screen.buttons[2:6]:
            alert_checking_bed.append([1 if button.switch.active else 0, button.text_right.lower().replace(" ", "_")])
        config_bed['alert_checking'] = alert_checking_bed
        save_config("config/settings.json", 'bed_json', data=config_bed)

        config_fall = load_config("config/settings.json",'fall_json')
        attach_video_fall = 1 if self.AT_screen.buttons[6].switch.active else 0
        config_fall['attach_video'] = attach_video_fall

        alert_checking_fall = []
        for button in self.AT_screen.buttons[7:]:
            alert_checking_fall.append([1 if button.switch.active else 0, button.text_right.lower().replace(" ", "_")])
        config_fall['alert_checking'] = alert_checking_fall
        save_config("config/settings.json", 'fall_json', data=config_fall)

        sound = SoundLoader.load('sound/tap.wav')
        if sound:
            sound.play()
        App.get_running_app().sm.current = self.screen_name
