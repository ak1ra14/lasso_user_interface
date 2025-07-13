from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from utils.icons import IconTextButton, ToggleButton
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from utils.layout import SeparatorLine 
from utils.layout import HeaderBar
from utils.icons import ToggleButton
class AlertTypeScreen(Screen):
    def __init__(self, **kwargs):
        super(AlertTypeScreen, self).__init__(**kwargs)
        header = HeaderBar(title="Alert Type", icon_path="images/home.png", button_text="Home", button_screen="menu")
        self.add_widget(header)

        ack_button = ToggleButton(
            text_right="Auto-acknowledgement alert",
            size_hint_y=None,
            height=50,
            text_size_l_r=(0,250),
            pos=(50, 340),
        )

        image = Image(
            source="images/bed_single.png",
            size_hint=(None, None),
            size=(70,70),
            pos = (70, 260)
        )
        y_axis = [220, 175, 130, 85, 40]
        bed_types = ["Alert with video", "Sit up","Bed exit","Sit-to-Stand","Fall besides bed"]
        for i, bed_type in enumerate(bed_types):
            button = ToggleButton(
                text_right=bed_type,
                size_hint_y=None,
                height=50,
                pos=(50, y_axis[i]),
                text_size_l_r=(0, 150)
            )
            self.add_widget(button)
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
            button = ToggleButton(
                text_right=bed_type,
                size_hint_y=None,
                height=50,
                pos=(400, y_axis[i]),
                text_size_l_r=(0, 200)
            )
            self.add_widget(button)

        float_layout = FloatLayout(size_hint=(1, 1))
        save_button = IconTextButton(
            icon_path="images/save.png",
            text="Save",
            size_hint=(None, None),
            size=(120, 120),
            pos_hint = None,
            pos=(800, 140),
            screen_name="menu"
        )
        float_layout.add_widget(save_button)
        self.add_widget(float_layout)
        self.add_widget(partition)
        self.add_widget(image)
        self.add_widget(ack_button)
        self.add_widget(fall_image)
