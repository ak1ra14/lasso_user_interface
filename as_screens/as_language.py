from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.properties import BooleanProperty
from kivy.app import App


from as_utils.as_freeze_screen import freeze_ui
from as_utils.as_config_loader import load_config, update_current_page, save_config, update_text_language, save_config_partial
from as_utils.as_layout import HeaderBar, SafeScreen
from as_utils.as_icons import IconTextButton


class LanguageScreen(SafeScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.buttons = []
        self.header = HeaderBar(title='language', icon_path="as_images/home.png", button_text="home", button_screen="menu")
        main_layout = BoxLayout(orientation='horizontal', spacing=80, size_hint_y=0.3, pos_hint={'center_x': 0.5, 'center_y': 0.5}, padding=[80,0,80,0])  # Only left and right padding
        main_layout.add_widget(Widget())
        self.en_button = LanguageButton(icon_path="as_images/english.png", text=update_text_language('english'), language='en', height=50)
        main_layout.add_widget(self.en_button)
        self.buttons.append(self.en_button)
        self.jp_button = LanguageButton(icon_path="as_images/japanese.png", text=update_text_language('japanese'), language='jp', height=50)
        main_layout.add_widget(self.jp_button)
        self.buttons.append(self.jp_button)
        main_layout.add_widget(Widget())
        self.add_widget(self.header)
        self.add_widget(main_layout)

    def go_to_main(self, instance):
        """
        Navigate to a specified screen.
        :param instance: The instance of the button that was pressed.
        :param screen_name: The name of the screen to navigate to.
        """
        self.manager.current = 'menu'

    def on_pre_enter(self):
        """
        This method is called when the screen is about to be displayed.
        It can be used to perform any setup or updates needed before the screen is shown.
        """
        # You can add any setup code here if needed
        update_current_page('language')
    
    def update_language(self):
        self.header.update_language()
        self.en_button.label.text = update_text_language('english')
        self.jp_button.label.text = update_text_language('japanese')


class LanguageButton(IconTextButton):
    active = BooleanProperty(False)
    def __init__(self, language, **kwargs):
        super().__init__(**kwargs)
        self.bind(on_press=self.on_button_press)
        self.language = language
        self.predefined_color()
        self.bind(active=self._update_active_color)
        self.button_mode = 'no_status'

    def on_button_press(self, instance):
        """
        Handle the button press event.
        This method can be overridden to perform specific actions when the button is pressed.
        """
        print(f"Language button pressed: {self.text}")
        # You can add additional logic here if needed


    def predefined_color(self):
        if load_config('as_config/settings.json','v3_json').get('language') == self.language:
            self.color_instruction.rgba = (0.2, 0.8, 0.2, 1)  # Green
        else:
            self.color_instruction.rgba = (0.22, 0.45, 0.91, 1)  # Blue

    def _update_active_color(self,instance, value):
        if self.active:
            self.color_instruction.rgba = (0.2, 0.8, 0.2, 1)  # Green
        else:
            self.color_instruction.rgba = (0.22, 0.45, 0.91, 1)  # Blue

    def on_press(self):
        freeze_ui(0.3)  # Freeze UI for 0.3 seconds
        App.get_running_app().sound_manager.play_tap()
        if not self.active:
            self.active = True
            App.get_running_app().language = self.language
            save_config_partial("as_config/settings.json","v3_json",key='language',value=self.language)
            for button in self.parent.parent.buttons:
                if button != self:
                    button.active = False
                    button._update_active_color(button, False)
            for screen in App.get_running_app().sm.screens:
                if hasattr(screen, 'update_language'):
                    screen.update_language()