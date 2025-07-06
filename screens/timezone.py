from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from utils.icons import IconTextButton
from kivy.uix.image import Image
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.button import Button
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.metrics import dp
from kivy.uix.scrollview import ScrollView

class TimezoneListView(RecycleView):
    def __init__(self, items = None, **kwargs):
        super().__init__(**kwargs)
        self.viewclass = 'Button'
        self.data = [{'text': tz} for tz in [
            "UTC", "US/Eastern", "US/Central", "US/Mountain", "US/Pacific",
            "Europe/London", "Asia/Tokyo", "Asia/Bangkok"
        ]]
        self.layout_manager = RecycleBoxLayout(
            default_size=(None, dp(56)),
            default_size_hint=(1, None),
            size_hint=(1, None),
            orientation='vertical'
        )
        self.layout_manager.bind(minimum_height=self.setter('height'))
        self.add_widget(self.layout_manager)

class TimezoneScreen(Screen):
    def __init__(self, **kwargs):
        """
        Timezone screen for the Soundeye application.
        This screen allows users to select a timezone.
        """
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', size=(400, 400), size_hint=(None,None))
        layout.bind(minimum_height=layout.setter('height'))

        for tz in ["UTC", "US/Eastern", "Asia/Tokyo"]:
            layout.add_widget(Button(text=tz, size_hint_y=None, height=200))
        scroll = ScrollView(size_hint=(1, None), size=(400,400), do_scroll_x=False)

        scroll.add_widget(layout)

        self.add_widget(scroll)

#             font_size=60,
#             font_name='fonts/Roboto-Bold.ttf',
#             pos_hint={'left': 1, 'top': 1},
#         ))
#         header.add_widget(Widget())  # Spacer
#         header.add_widget(IconTextButton(
#             icon_path="images/home.png",
#             text="Home",
#             size_hint_y=None,
#             height=50,
#             screen_name='menu',  # Navigate to menu screen
#         ))
#         body = BoxLayout(orientation='horizontal', spacing=15, size_hint_y=0.5, pos_hint={'center_x': 0.5, 'center_y': 0.5}, padding=[50,0,50,0])
#         time_zone_lst = ["Singapore (GMT+8)", "Japan (GMT+9)", "Los Angeles (GMT-7)"]
#         body.add_widget(TimezoneListView(time_zone_lst))
#         self.add_widget(header)
#         self.add_widget(body)
#         # super().__init__(**kwargs)
#         # timezones = [

