import sys
import subprocess
import threading
from utils.layout import HeaderBar
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle
from kivy.uix.button import Button
from utils.config_loader import load_config, save_config
from utils.icons import IconTextButton

class WifiLoadingScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.config = load_config("config/V3.json")
        self.selected_wifi = self.config.get('wifi_ssid', {})
        self.header = HeaderBar(title="Wi-Fi SSID")
        self.add_widget(self.header)
        self.add_widget(Label(text="Scanning WiFi...", size_hint=(1, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.5}))
        self.wifi_list = []

    def on_pre_enter(self):
        # Start scanning in a background thread when the screen is shown
        threading.Thread(target=self.scan_wifi, daemon=True).start()

    def scan_wifi(self):
        wifi_list = get_available_wifi()
        # Update UI on the main thread
        Clock.schedule_once(lambda dt: self.show_results(wifi_list))

    def show_results(self, wifi_list):
        self.clear_widgets()
        self.add_widget(self.header)
        list_box = GridLayout(cols=1, size=(465, 800), size_hint=(None,None), pos_hint=(None, None),)
        for wifi in wifi_list:
            button = SelectableButton(text=wifi, font_size=40,
                                                font_family='fonts/Roboto-Bold.ttf', size_hint_y=None, 
                                                height=55, selection=self)
            list_box.add_widget(button)
            self.wifi_list.append(button)
            
        scroll = ScrollView(size_hint=(None, None),
                            scroll_type=['bars', 'content'],
                            bar_width=35, 
                            bar_color=(0.2, 0.6, 0.8, 1),  # Active bar color (blue)
                            bar_inactive_color=(0.7, 0.7, 0.7, 1),  # Inactive bar color (gray)
                            pos_hint={'center_x': 0.6, 'center_y': 0.4},
                            size=(500,300),
                            do_scroll_x=False)
        with scroll.canvas.before:
            Color(1, 1, 1, 1)  # White
            rect = Rectangle(pos=scroll.pos, size=scroll.size)
        scroll.bind(pos=lambda instance, value: setattr(rect, 'pos', value))
        scroll.bind(size=lambda instance, value: setattr(rect, 'size', value))

        scan_wifi = IconTextButton(
            text="Scan WiFi",
            icon_path ='images/wifi.png',
            size = (120,120),
            pos_hint={'center_x': 0.3, 'center_y': 0.6},
            on_release=lambda x: threading.Thread(target=self.scan_wifi, daemon=True).start()
        )
        connect_wifi = IconTextButton(
            text="Connect",
            icon_path ='images/connection.png',
            size = (120,120),
            pos_hint={'center_x': 0.3, 'center_y': 0.2},
            on_release=lambda x: self.select_wifi(self.selected_wifi)
        )
                
        scroll.add_widget(list_box)
        self.add_widget(scroll)
        self.add_widget(scan_wifi)
        self.add_widget(connect_wifi)

    def select_wifi(self, btn):
        for b in self.timezone_list:
            if b == btn:
                continue
            b.selected = False
            b.update_color()
        btn.selected = True
        btn.update_color()
        self.selected_wifi = btn.text


def get_available_wifi():
    wifi_list = []
    if sys.platform == 'darwin':  # Mac
        try:
            result = subprocess.check_output(
                ["/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport", "-s"],
                universal_newlines=True
            )
            lines = result.split('\n')[1:]  # Skip header
            for line in lines:
                if line.strip():
                    ssid = line.split()[0]
                    wifi_list.append(ssid)
        except Exception as e:
            print("Error getting Wi-Fi:", e)
    elif sys.platform.startswith('linux'):
        try:
            result = subprocess.check_output(['nmcli', '-t', '-f', 'SSID', 'dev', 'wifi'], universal_newlines=True)
            wifi_list = [line for line in result.split('\n') if line]
        except Exception as e:
            print("Error getting Wi-Fi:", e)
    elif sys.platform.startswith('win'):
        try:
            result = subprocess.check_output(['netsh', 'wlan', 'show', 'networks'], universal_newlines=True)
            for line in result.split('\n'):
                if "SSID" in line:
                    ssid = line.split(":", 1)[1].strip()
                    if ssid:
                        wifi_list.append(ssid)
        except Exception as e:
            print("Error getting Wi-Fi:", e)
    return wifi_list


class SelectableButton(Button):
    """
    A button that can be selected or deselected.
    """
    def __init__(self, text,selection, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.selection = selection  # Reference to the selection manage
        self.selected = (selection.selected_wifi == text)  # Check if this button's timezone is the selected one
        self.background_normal = ''
        self.background_down = ''
        self.background_color = (1, 1, 1, 1)
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_rect, size=self._update_rect)
        self.update_color()
        self.bind(on_relase=self.on_press)
    
    def _update_rect(self, *args):
        """
        Update the rectangle size and position when the button is resized or moved.
        """
        self.rect.pos = self.pos
        self.rect.size = self.size

    def update_color(self):
        print(self.text, "selected:", self.selected)
        if self.selected:
            self.color = (1, 1, 1, 1)
            self.background_color = (0.2, 0.6, 0.8, 1)
        else:
            self.color = (0, 0, 0, 1)
            self.background_color = (1, 1, 1, 1)

    def on_press(self):
        """
        Override the on_press method to handle button press.
        """
        super().on_press()

# Example usage:
if __name__ == "__main__":
    print(get_available_wifi())