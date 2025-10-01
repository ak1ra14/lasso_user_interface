from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import BooleanProperty


from as_utils.as_icons import IconTextButton, ToggleButton, CustomSwitch
from as_utils.as_layout import SeparatorLine
from as_utils.as_layout import HeaderBar, SafeScreen
from as_utils.as_config_loader import load_config, save_config, update_current_page, update_text_language, to_json_format, save_config_partial
from as_utils.as_freeze_screen import freeze_ui   


class AlertModeScreen(Screen):
    """
    Alert Mode Screen
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.modes = load_config('as_config/settings.json','v3_json').get('previous_mode', 'fall.json')
        self.single_multiple = load_config(f"as_config/{self.modes}").get('minnumppl_for_noalert', 99)
        self.no_beds = load_config("as_config/settings.json",'bed_json').get('nbeds', [1, 1])[0] == 2
        self.header = HeaderBar(title="mode", icon_path="as_images/home.png", button_text="home", button_screen="menu")
        main_layout = BoxLayout(orientation='horizontal', padding=[50, 0, 50, 0], spacing=50,size_hint_y=0.5, pos_hint={'center_x': 0.5,'center_y':0.4})  # Only left and right padding
        main_layout.add_widget(Widget())  # Spacer on the left
        self.icon_images = ["bed_single", "bed_multiple","fall_single", "fall_multiple"]
        self.icon_label = ["bed_mode", "bed_mode", "fall_mode", "fall_mode"]
        self.icon_status = ["bed_single", "bed_multiple", "fall_single", "fall_multiple"]
        self.buttons = []
        for i in range(len(self.icon_images)):
            if self.icon_images[i].split('_')[1] == "multiple":
                active_state = 99
            else:
                if self.icon_images[i].split('_')[0] == "fall":
                    active_state = 2
                else:
                    active_state = 1
            icon = AlertModeButton(
                icon_path=f"as_images/{self.icon_images[i]}.png",
                text=update_text_language(self.icon_label[i]),
                config = update_text_language(self.icon_status[i]),
                size_hint_y=None,
                size=(170, 170),
                pos_hint={'center_x': 0.5, 'center_y': 0.5},
                active_state=active_state, #the minnumppl_for_noalert = 1 or 99
                screen=self, #to keep track of the active button
                mode=self.icon_images[i].split("_")[0], #to keep track of the button's mode
            )
            self.buttons.append(icon)
            main_layout.add_widget(icon)
        main_layout.add_widget(Widget())
        toggle_layout = FloatLayout(size_hint_y=None, height=60, pos_hint={'center_x': 0.5, 'center_y': 0.25})
        self.toggle_button = ToggleButton(
            text_left="one_bed",
            text_right="two_bed",
            text_size_l_r=(100, 130),
            size_hint_y=None,
            switch=CustomSwitchAM(parent=self),
            pos=(130, 345)
        )

        toggle_layout.add_widget(self.toggle_button)

        partition = SeparatorLine(
            points=[512, 400, 512, 70],
            size_hint=(None, None),
        )

        self.add_widget(self.header)
        self.add_widget(toggle_layout)
        self.add_widget(partition)
        self.add_widget(main_layout)

    def on_pre_enter(self):
        """
        Called when the screen is entered.
        Updates the active state of buttons based on the current mode and single/multiple state.
        """
        update_current_page('alert_mode')
        self.modes = load_config('as_config/settings.json','fall_json').get('previous_mode', 'fall.json')
        self.single_multiple = load_config(f"as_config/{self.modes}").get('minnumppl_for_noalert', 99)
        self.no_beds = load_config("as_config/settings.json",'bed_json').get('nbeds', [1, 1])[0]
            # Update the toggle button state and graphics
        self.toggle_button.switch.no_beds = self.no_beds
        self.toggle_button.switch.active = True if self.no_beds == 2 else False
        self.toggle_button.switch.update_graphics()


    def update_language(self):
        """
        Update the language of the screen elements.
        """
        self.header.update_language()
        for i in range(len(self.buttons)):
            self.buttons[i].label.text = update_text_language(self.icon_label[i])
            self.buttons[i].status.text = update_text_language(self.icon_status[i])
        self.toggle_button.update_language()
        
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
        freeze_ui(0.3)  # Freeze UI for 0.3 secondss
        App.get_running_app().sound_manager.play_tap()
        # Change colour of icon when active and update config file
        if not self.active:
            self.active = True
            self.screen.modes = f"{self.mode}.json"
            self.screen.single_multiple = self.active_state
            config = load_config('as_config/settings.json','v3_json')
            save_config_partial("as_config/settings.json","v3_json",key='previous_mode',value=self.screen.modes)
            config = load_config(f"as_config/{self.screen.modes}")
            config['minnumppl_for_noalert'] = self.active_state
            config['multihumanpause_seconds'] = 0 if self.active_state == 99 else 5
            config['no_alert_by_overlap'] = 0 if self.active_state == 99 else 1
            save_config(f"as_config/{self.screen.modes}", data=config)
            for button in self.screen.buttons:
                if button != self:
                    button.active = False
                    button._update_active_color(button, False)

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
        nbeds_value = load_config("as_config/settings.json","bed_json").get('nbeds')
        if self.collide_point(*touch.pos):
            freeze_ui(0.3)  # Freeze UI for 0.3 seconds
            self.active = not self.active
            # Toggle between 1 and 2
            self.no_beds = 2 if self.no_beds == 1 else 1
            nbeds_value[0] = self.no_beds
            if self.no_beds == 1:  
                nbeds_value[1] = ['1']         
            elif self.no_beds == 2:
                nbeds_value[1] = ['1', '2']

            save_config_partial("as_config/settings.json", "bed_json", key='nbeds', value=nbeds_value)
            return True
        return False
            
     