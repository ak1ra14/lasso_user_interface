from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from utils.icons import IconTextButton, ToggleButton
from kivy.uix.widget import Widget
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.switch import Switch
from kivy.uix.floatlayout import FloatLayout
from utils.layout import SeparatorLine
from utils.layout import HeaderBar
class AlertModeScreen(Screen):
    """
    Alert Mode Screen
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        header = HeaderBar(title="Alert Mode", icon_path="images/home.png", button_text="Home", button_screen="menu")
        main_layout = BoxLayout(orientation='horizontal', padding=[50, 0, 50, 0], spacing=50,size_hint_y=0.5, pos_hint={'center_x': 0.5,'center_y':0.4})  # Only left and right padding
        main_layout.add_widget(Widget())  # Spacer on the left
        icon_images = ["bed_single", "bed_multiple","fall_single", "fall_multiple"]
        for i in range(len(icon_images)):
            icon = IconTextButton(
                icon_path=f"images/{icon_images[i]}.png",
                text=icon_images[i].replace("_", " ").title(),
                size_hint_y=None,
                size=(170, 170),
                pos_hint={'center_x': 0.5, 'center_y': 0.5},
                screen_name="menu"
            )
            main_layout.add_widget(icon)
        main_layout.add_widget(Widget())
        toggle_layout = FloatLayout(size_hint_y=None, height=60, pos_hint={'center_x': 0.5, 'center_y': 0.25})
        toggle_button = ToggleButton(
            text_left="One Bed",
            text_right="Two Beds",
            size_hint_y=None,
            pos = (125,340)
  
        )
        
        toggle_layout.add_widget(toggle_button)

        partition = SeparatorLine(
            points=[512, 400, 512, 70],
            size_hint=(None, None),
        )

        self.add_widget(header)
        self.add_widget(toggle_layout)
        self.add_widget(partition)

        self.add_widget(main_layout)
