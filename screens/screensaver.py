from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget  
from utils.icons import IconTextButton
from kivy.uix.image import Image
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout

from utils.config_loader import load_config

class ScreenSaverScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        header= BoxLayout(orientation='horizontal', pos_hint={'top': 1}, size_hint_y=0.25, padding=[50, 40, 50, 0], spacing=10)
        header.add_widget(Label(
            text="Screensaver",
            font_size=60,
            font_name='fonts/Roboto-Bold.ttf',
            pos_hint={'left': 1, 'top': 1},
        ))
        header.add_widget(Widget())  # Spacer
        header.add_widget(IconTextButton(
            icon_path="images/home.png",
            text="Home",
            size_hint_y=None,
            height=50,
            screen_name='menu',  # Navigate to menu screen
        ))
        buttons = BoxLayout(orientation='horizontal', spacing=15, size_hint_y=0.3, pos_hint={'center_x': 0.5, 'center_y': 0.5}, padding=[50,0,50,0])  # Only left and right padding
        buttons.add_widget(IconTextButton(icon_path="images/decrease_10.png", height=50))
        buttons.add_widget(IconTextButton(icon_path="images/decrease.png", height=50))
        time = BoxLayout(orientation='vertical', spacing=30, size_hint_y=0.3, pos_hint={'center_x': 0.5, 'center_y': 0.5}, padding=[20,0,20,0])
        time.add_widget(Label(
            text=f"{load_config('config/V3.json').get('screensaver', 60)}",
            font_size=80,
            font_name='fonts/Roboto-Bold.ttf',
            size_hint_y=0.7,
        ))

        time.add_widget(Label(
            text="seconds",
            font_size=20,
            font_name='fonts/Roboto-Bold.ttf',
            size_hint_y=0.3,
        ))
        buttons.add_widget(time)
        buttons.add_widget(IconTextButton(icon_path="images/increase_10.png", height=50))
        buttons.add_widget(IconTextButton(icon_path="images/increase.png",height=50))
        self.add_widget(header)
        self.add_widget(buttons)
        save_anchor = AnchorLayout(
            anchor_x='center',
            anchor_y='bottom',
            size_hint=(1, None),
            height=120,
            padding=[0, 20, 0, 40]  # Padding for the anchor layout
        )
        save_anchor.add_widget(IconTextButton(
            icon_path="images/save.png",
            text="Save",
            size_hint=(None, None),
            size=(120, 120)
        ))

        self.add_widget(save_anchor)
