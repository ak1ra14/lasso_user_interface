from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from utils.icons import IconTextButton, CircularImageButton
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.widget import Widget

class LanguageScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # topleft = AnchorLayout(anchor_x='left', anchor_y='top', pos_hint={'left': 1,"top":1}, size_hint=(1, None), height=50)
        # topleft.add_widget(Label(text="Language Selection", font_size=40,font_name='fonts/Roboto-Bold.ttf', size_hint_y=None, height=50))
        # topright = AnchorLayout(anchor_x='right', anchor_y='top', pos_hint={'right': 1,"top":1},size_hint=(0.2,0.2),height=50,padding=[0,30,30,0])
        # topright.add_widget(IconTextButton(icon_path="images/home.png", text="Home", size_hint_y=None, height=50, screen_name='menu'))
        header= BoxLayout(orientation='horizontal', pos_hint={'top': 1}, size_hint_y=0.25, padding=[50, 40, 50, 0], spacing=10)
        header.add_widget(Label(
            text="Language",
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
        buttons = BoxLayout(orientation='horizontal', spacing=80, size_hint_y=0.3, pos_hint={'center_x': 0.5, 'center_y': 0.5}, padding=[80,0,80,0])  # Only left and right padding
        buttons.add_widget(Widget())
        buttons.add_widget(IconTextButton(icon_path="images/english.png", text="English", height=50))
        buttons.add_widget(IconTextButton(icon_path="images/japanese.png", text="Japanese", height=50))
        buttons.add_widget(Widget())
        self.add_widget(header)
        self.add_widget(buttons)
    
    def go_to_main(self, instance):
        """
        Navigate to a specified screen.
        :param instance: The instance of the button that was pressed.
        :param screen_name: The name of the screen to navigate to.
        """
        self.manager.current = 'menu'