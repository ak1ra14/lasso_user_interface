import sys
import subprocess
import threading
from utils.layout import HeaderBar
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.clock import Clock

class WifiLoadingScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.header = HeaderBar(title=" ")
        self.add_widget(self.header)
        self.add_widget(Label(text="Scanning WiFi...", size_hint=(1, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.5}))

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
        if wifi_list:
            for ssid in wifi_list:
                self.add_widget(Label(text=ssid, size_hint=(1, None), height=40))
        else:
            self.add_widget(Label(text="No WiFi networks found.", size_hint=(1, None), height=40))


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

# Example usage:
if __name__ == "__main__":
    print(get_available_wifi())