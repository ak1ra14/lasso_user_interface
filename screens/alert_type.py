from utils.icons import IconTextButton, ToggleButton
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import BooleanProperty
from kivy.app import App
from kivy.core.audio import SoundLoader
from utils.layout import SeparatorLine 
from utils.layout import HeaderBar, SafeScreen
from utils.icons import ToggleButton, CustomSwitch
from utils.config_loader import load_config, update_current_page, update_text_language, get_valid_value, save_config_partial, update_all_values, check_all_values_same
from utils.keyboard import show_saved_popup
from kivy.graphics import Color, RoundedRectangle
from kivy.logger import Logger

class AlertTypeScreen(SafeScreen):
    def __init__(self, **kwargs):
        super(AlertTypeScreen, self).__init__(**kwargs)
        self.config = load_config('config/settings.json','v3_json')
        self.ack_config = load_config('config/settings.json','ack_json')
        self.ack_enable = get_valid_value(self.ack_config, 'ack_enable', load_config("config/settings.json","default_json").get("ack_enable", "yes"))
        self.bed_json = load_config("config/settings.json",'bed_json')
        self.fall_json = load_config("config/settings.json",'fall_json')
        self.attach_video_bed = self.bed_json.get("attach_video", 1)
        self.attach_video_fall = self.fall_json.get("attach_video", 1)
        self.alert_checking_bed = self.bed_json.get("alert_checking", None)
        self.alert_checking_fall = self.fall_json.get("alert_checking", None)
        self.header = HeaderBar(title="alerts", icon_path="images/home.png", button_text="home", button_screen="menu")
        self.buttons = {}
        self.add_widget(self.header)

        ack_button_text = 1 if self.ack_enable == "yes" else 0
        ack_button = ToggleButton(
            text_right="auto_acknowledgement_alert",
            size_hint_y=None,
            height=50,
            switch = AlertTypeButton(ack_button_text),
            text_size_l_r=(0,350),
            pos=(50, 410),
        )
        self.buttons["ack_button"] = ack_button

        image = Image(
            source="images/bed_single.png",
            size_hint=(None, None),
            size=(70,70),
            pos = (70, 330)
        )
        self.y_axis = [290, 220, 165, 110, 55]
        self.bed_types = ["alert_with_video", "sit_up","bed_exit","sit-to-stand","lie_out"]
        self.build_bed_buttons()

        partition = SeparatorLine(
            points=[370, 370, 370, 60],
            size_hint=(None, None),
        )
        
        fall_image = Image(
            source="images/fall_single.png",
            size_hint=(None, None),
            size=(50,50),
            pos = (420, 335)
        )
        self.fall_types = ["alert_with_video","sit-to-stand","fall"]
        self.build_fall_buttons()
        

        float_layout = FloatLayout(size_hint=(1, 1))
        self.save_button = SaveButtonAT(
            icon_path="images/save.png",
            text=update_text_language('save'),
            size_hint=(None, None),
            size=(120, 120),
            pos_hint = None,
            pos=(800, 180),
            AT_screen=self,
            screen_name="menu"
        )
        float_layout.add_widget(self.save_button)
        self.add_widget(float_layout)
        self.add_widget(partition)
        self.add_widget(image)
        self.add_widget(ack_button)
        self.add_widget(fall_image)

    def build_bed_buttons(self):
        for i, bed_type in enumerate(self.bed_types):
            if i == 0:
                value = self.attach_video_bed 
            else:
                value = self.get_first_value(self.alert_checking_bed, bed_type)
            if value is None:
                value = 0        
                button = ToggleButton(
                    text_right=bed_type,
                    size_hint_y=None,
                    height=50,
                    pos=(50, self.y_axis[i]),
                    switch=AlertTypeButton(value, freeze=True),  # Disable the switch
                    text_size_l_r=(0, 180)
                )
            else:
                button = ToggleButton(
                    text_right=bed_type,
                    size_hint_y=None,
                    height=50,
                    pos=(50, self.y_axis[i]),
                    switch=AlertTypeButton(value),
                    text_size_l_r=(0, 180)
                )
            self.add_widget(button)
            if bed_type == "alert_with_video":
                self.buttons['alert_with_video_bed'] = button
            elif bed_type == "sit-to-stand":
                self.buttons['sit-to-stand_bed'] = button
            else:
                self.buttons[bed_type] = button

    def build_fall_buttons(self):
        for i, fall_type in enumerate(self.fall_types):
            if i == 0:
                value = self.attach_video_fall
            else:
                value = self.get_first_value(self.alert_checking_fall, fall_type)
            if value is None:
                value = 0        
                button = ToggleButton(
                    text_right=fall_type,
                    size_hint_y=None,
                    height=50,
                    switch=AlertTypeButton(value, freeze=True),  # Set freeze=True to disable
                    pos=(400, self.y_axis[i]),
                    text_size_l_r=(0, 200)
                )
            else:
                button = ToggleButton(
                    text_right=fall_type,
                    size_hint_y=None,
                    height=50,
                    switch=AlertTypeButton(value),
                    pos=(400, self.y_axis[i]),
                    text_size_l_r=(0, 200)
                )
            self.add_widget(button)
            if fall_type == 'alert_with_video':
                self.buttons['alert_with_video_fall'] = button
            elif fall_type == 'sit-to-stand':
                self.buttons['sit-to-stand_fall'] = button
            else:
                self.buttons[fall_type] = button


    def on_pre_enter(self):
        update_current_page('alert_type')
        status = {}
        self.config = load_config('config/settings.json','v3_json')
        self.ack_config = load_config('config/settings.json','ack_json')
        self.ack_enable = get_valid_value(self.ack_config, 'ack_enable', load_config("config/settings.json","default_json").get("ack_enable", "yes"))
        status['ack_button'] = 1 if self.ack_enable == "yes" else 0

        self.bed_json = load_config("config/settings.json",'bed_json')
        self.fall_json = load_config("config/settings.json",'fall_json')
        attach_video_bed = self.bed_json.get("attach_video", 1)
        status['alert_with_video_bed'] = attach_video_bed

        status = self.update_status_bed(status)

        attach_video_fall = self.fall_json.get("attach_video", 1)
        status['alert_with_video_fall'] = attach_video_fall

        status = self.update_status_fall(status)

        self.update_state(status)

        self.header.update_language()
        self.save_button.label.text = update_text_language('save')

    def get_first_value(self, alert_checking_list, alert_type):
        for item in alert_checking_list:
            if item[4] == alert_type:
                return item[3]
        return None
    
    def update_status_bed(self,status):
        alert_checking_bed = self.bed_json.get("alert_checking", None)
        for bed_type in self.bed_types[1:]:
            value = self.get_first_value(alert_checking_bed, bed_type)
            if bed_type == 'sit-to-stand':
                bed_type = 'sit-to-stand_bed'
            if value is not None:
                status[bed_type] = (False, value)
            else:
                status[bed_type] = (True, 0)
        return status
    
    def update_status_fall(self,status):
        alert_checking_fall = self.fall_json.get("alert_checking", None)
        for fall_type in self.fall_types[1:]:
            value = self.get_first_value(alert_checking_fall, fall_type)
            if fall_type == 'sit-to-stand':
                fall_type = 'sit-to-stand_fall'
            if value is not None:
                #Logger.debug(f"FALSE: fall_type: {fall_type}, value: {value}")
                status[fall_type] = (False, value)
            else:
                #Logger.debug(f"TRUE: fall_type: {fall_type}, value: {value}")
                status[fall_type] = (True, 0)

        return status
    
    def update_state(self, status):
        for key in self.buttons.keys():
            if isinstance(status[key], tuple):
                #Logger.debug(f"BUTTON: {key}, status: {status[key]}")
                self.buttons[key].switch.freeze = status[key][0]
                self.buttons[key].switch.active = True if status[key][1] == 1 else False
            else:
                self.buttons[key].switch.active = status[key]
            self.buttons[key].switch.update_graphics()
            self.buttons[key].update_language()
        
    
class AlertTypeButton(CustomSwitch):
    def __init__(self, value, freeze=False, **kwargs):
        # Remove freeze from kwargs before passing to parent
        if 'freeze' in kwargs:
            del kwargs['freeze']
        super().__init__(**kwargs)
        self.active = True if value == 1 else False
        self._freeze = freeze  # Use _freeze to avoid property name conflicts
        if self._freeze:
            # Make the switch appear disabled
            with self.canvas:
                self.disabled_color = Color(0.7, 0.7, 0.7, 0.5)  # Gray overlay
                self.disabled_rect = RoundedRectangle(
                    pos=self.pos, 
                    size=self.size,
                    radius=[15]
                )
            self.bind(pos=self._update_disabled_rect, size=self._update_disabled_rect)

    def toggle(self, instance, touch):
        if self._freeze:
            return False  # Ignore touches when frozen
        return super().toggle(instance, touch)  # Normal behavior when not frozen

    def _update_disabled_rect(self, *args):
        if hasattr(self, 'disabled_rect'):
            self.disabled_rect.pos = self.pos
            self.disabled_rect.size = self.size

class SaveButtonAT(IconTextButton):
    def __init__(self, AT_screen, **kwargs):
        super().__init__(**kwargs)
        self.icon_path = "images/save.png"
        self.size_hint = (None, None)
        self.size = (120, 120)
        self.pos = (800, 180)
        self.screen_name = "menu"
        self.AT_screen = AT_screen

    def on_press(self):
        ack_config = load_config('config/settings.json','ack_json')
        self.buttons = self.AT_screen.buttons
        if ack_config:
            ack_enable = "yes" if self.AT_screen.buttons['ack_button'].switch.active else "no"
            if not check_all_values_same("config/settings.json",'ack_json',key='ack_enable', value_to_check=ack_config.get('ack_enable',None)):
                save_config_partial("config/settings.json", "ack_json", key='ack_enable',value=ack_enable)
            else:
                update_all_values("config/settings.json",'ack_json', key='ack_enable', new_value= ack_enable)   

        config_bed = load_config("config/settings.json",'bed_json')
        alert_checking_bed = config_bed.get('alert_checking')
        attach_video_bed = 1 if self.AT_screen.buttons['alert_with_video_bed'].switch.active else 0
        save_config_partial('config/settings.json','bed_json',key='attach_video',value=attach_video_bed)
        # Save alert checking configurations
        alert_checking_bed = self.update_alert_checking(
            alert_checking_bed, 
            self.AT_screen.bed_types, 
            mode='bed'
        )
        save_config_partial('config/settings.json', 'bed_json', 
                       key='alert_checking', value=alert_checking_bed)

        config_fall = load_config("config/settings.json",'fall_json')
        alert_checking_fall = config_fall.get('alert_checking')
        attach_video_fall = 1 if self.AT_screen.buttons['alert_with_video_fall'].switch.active else 0
        save_config_partial('config/settings.json','fall_json',key='attach_video',value=attach_video_fall)

        alert_checking_fall = self.update_alert_checking(
            alert_checking_fall, 
            self.AT_screen.fall_types, 
            mode='fall'
        )
        save_config_partial('config/settings.json', 'fall_json', 
                        key='alert_checking', value=alert_checking_fall)
        
        show_saved_popup(update_text_language('saved'))  # Show a popup indicating the settings have been saved
        sound = SoundLoader.load('sound/tap.wav')
        if sound:
            sound.play()
        App.get_running_app().sm.current = self.screen_name

    def update_alert_checking(self, alert_checking_list, alert_types, mode='bed'):
        """
        Update alert checking list for both bed and fall modes
        
        Args:
            alert_checking_list: List of alert checking configurations
            alert_types: List of alert types to process
            mode: 'bed' or 'fall' to determine button suffix
        
        Returns:
            Updated alert checking list
        """
        for alert_type in alert_types:
            if alert_type == 'alert_with_video':
                continue
                
            # Get the correct button based on type and mode
            if alert_type == 'sit-to-stand':
                button_key = f'sit-to-stand_{mode}'
            else:
                button_key = alert_type
                
            button = self.buttons[button_key]
            
            if not button.switch.freeze:
                for i in range(len(alert_checking_list)):
                    if alert_checking_list[i][4] == alert_type:
                        value = 1 if button.switch.active else 0
                        # Preserve the first three empty arrays
                        alert_checking_list[i] = [
                            alert_checking_list[i][0],  # Keep first []
                            alert_checking_list[i][1],  # Keep second []
                            alert_checking_list[i][2],  # Keep third []
                            value,                      # Update the 0/1 value
                            alert_type                  # Update the type
                        ]
                        break
                        
        return alert_checking_list



