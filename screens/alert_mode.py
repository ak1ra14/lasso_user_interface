from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from utils.icons import IconTextButton, ToggleButton, CustomSwitch
from kivy.uix.widget import Widget
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.switch import Switch
from kivy.uix.floatlayout import FloatLayout
from kivy.core.audio import SoundLoader
from kivy.properties import BooleanProperty
from utils.layout import SeparatorLine
from utils.layout import HeaderBar, SafeScreen
from utils.config_loader import load_config, save_config, update_current_page
class AlertModeScreen(Screen):
    """
    Alert Mode Screen
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.modes = load_config('config/settings.json','fall_json').get('previous_mode', 'fall.json')
        self.single_multiple = load_config(f"config/{self.modes}").get('mincount', 1)
        self.no_beds = load_config("config/settings.json",'bed_json').get('nbeds', [1, 1])[0] == 2
        header = HeaderBar(title="Alert Mode", icon_path="images/home.png", button_text="Home", button_screen="menu")
        main_layout = BoxLayout(orientation='horizontal', padding=[50, 0, 50, 0], spacing=50,size_hint_y=0.5, pos_hint={'center_x': 0.5,'center_y':0.4})  # Only left and right padding
        main_layout.add_widget(Widget())  # Spacer on the left
        icon_images = ["bed_single", "bed_multiple","fall_single", "fall_multiple"]
        self.buttons = []
        for i in range(len(icon_images)):
            active_state = 99 if icon_images[i].split('_')[1] == "multiple" else 1
            icon = AlertModeButton(
                icon_path=f"images/{icon_images[i]}.png",
                text=icon_images[i].replace("_", " ").title(),
                size_hint_y=None,
                size=(170, 170),
                pos_hint={'center_x': 0.5, 'center_y': 0.5},
                active_state=active_state, #the mincount = 1 or 99 
                screen=self, #to keep track of the active button 
                mode=icon_images[i].split("_")[0], #to keep track of the button's mode 
            )
            self.buttons.append(icon)
            main_layout.add_widget(icon)
        main_layout.add_widget(Widget())
        toggle_layout = FloatLayout(size_hint_y=None, height=60, pos_hint={'center_x': 0.5, 'center_y': 0.25})
        toggle_button = ToggleButton(
            text_left="One Bed",
            text_right="Two Beds",
            size_hint_y=None,
            switch=CustomSwitchAM(parent=self),
            pos=(125, 340)

        )

        self.toggle_button = toggle_button
        
        toggle_layout.add_widget(toggle_button)

        partition = SeparatorLine(
            points=[512, 400, 512, 70],
            size_hint=(None, None),
        )

        self.add_widget(header)
        self.add_widget(toggle_layout)
        self.add_widget(partition)

        self.add_widget(main_layout)

    def on_pre_enter(self):
        """
        Called when the screen is entered.
        Updates the active state of buttons based on the current mode and single/multiple state.
        """
        update_current_page('alert_mode')
        self.modes = load_config('config/settings.json','fall_json').get('previous_mode', 'fall.json')
        self.single_multiple = load_config(f"config/{self.modes}").get('mincount', 1)
        self.no_beds = load_config("config/settings.json",'bed_json').get('nbeds', [1, 1])[0]
            # Update the toggle button state and graphics
        self.toggle_button.switch.no_beds = self.no_beds
        self.toggle_button.switch.active = True if self.no_beds == 2 else False
        self.toggle_button.switch.update_graphics()

class AlertModeButton(IconTextButton):
    """
    Custom button for alert mode with an icon and text.
    """
    active = BooleanProperty(False)

    def __init__(self, icon_path, text, screen, active_state, mode,**kwargs):
        super().__init__(icon_path=icon_path, text=text, **kwargs)
        self.active_state = active_state
        self.screen = screen
        self.mode = mode
        self.size_hint_y = None
        self.size = (170, 170)
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        self.predefined_color()
        self.bind(active=self._update_active_color)

    def predefined_color(self):
        if self.screen.modes.split('.')[0] == self.mode and self.screen.single_multiple == self.active_state:
            self.color_instruction.rgba = (0.2, 0.8, 0.2, 1)  # Green
        else:
            self.color_instruction.rgba = (0.22, 0.45, 0.91, 1)  # Blue

    def _update_active_color(self,instance, value):
        if self.active:
            self.color_instruction.rgba = (0.2, 0.8, 0.2, 1)  # Green
        else:
            self.color_instruction.rgba = (0.22, 0.45, 0.91, 1)  # Blue

    def on_press(self):
        if not self.active:
            self.active = True
            self.screen.modes = f"{self.mode}.json"
            self.screen.single_multiple = self.active_state
            config = load_config('config/settings.json','v3_json')
            config['previous_mode'] = self.screen.modes
            save_config('config/settings.json','v3_json', data=config)
            config = load_config(f"config/{self.screen.modes}")
            config['mincount'] = self.active_state
            save_config(f"config/{self.screen.modes}", data=config)
            for button in self.screen.buttons:
                if button != self:
                    button.active = False
                    button._update_active_color(button, False)
        sound = SoundLoader.load('sound/tap.mp3')
        if sound:
            sound.play()


class CustomSwitchAM(CustomSwitch):
    """
    A toggle button that switches between two states: "One Bed" and "Two Beds".
    """
    active = BooleanProperty(False)  # True for two beds, False for one bed
    def  __init__(self, parent, **kwargs):
        super().__init__(**kwargs)
        self.no_beds = parent.no_beds
        self.active = True if self.no_beds == 2 else False
        self.bind(pos=self.update_graphics, size=self.update_graphics)
        self.bind(active=self.update_graphics)
        self.bind(on_touch_down=self.toggle)

    def toggle(self, instance, touch):
        if self.collide_point(*touch.pos):
            self.active = not self.active
            # Toggle between 1 and 2
            self.no_beds = 2 if self.no_beds == 1 else 1
            config = load_config("config/bed.json")
            config['nbeds'] = [self.no_beds, load_config("config/bed.json").get('nbeds', [1])[1]]
            save_config("config/settings.json", "bed_json", data=config)
            return True
        return False
            
     