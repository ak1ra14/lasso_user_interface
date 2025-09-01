import sys, subprocess, threading, time
from utils.layout import HeaderBar, SafeScreen, LoadingCircle
from kivy.uix.image import Image
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle
from kivy.uix.button import Button
from utils.config_loader import load_config, save_config, update_current_page, update_text_language
from utils.icons import IconTextButton
from utils.keyboard import KeyboardScreen
from utils.freeze_screen import freeze_ui

class WifiLoadingScreen(SafeScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.config = load_config("config/settings.json", "v3_json")
        self.selected_wifi = self.config.get('wifi_ssid', {})
        self.header = HeaderBar(title="Wi-Fi SSID", button_screen="menu2")
        self.loading_circle = LoadingCircle(pos_hint={'center_x': 0.5, 'center_y': 0.6}, size=120,dot_color=(0.5,0,0.5,1))
        self.add_widget(self.header)
        self.scanning = Label(text=update_text_language('scanning_wifi'), font_size=30, size_hint=(1, 0.2), 
                              pos_hint={'center_x': 0.5, 'center_y': 0.4}, font_name='fonts/MPLUS1p-Regular.ttf')
        self.add_widget(self.scanning)
        self.wifi_list = []

    def on_pre_enter(self):
        # Start scanning in a background thread when the screen is shown
        update_current_page('wifi loading')
        self.pre_enter_loading()

    def pre_enter_loading(self):
        self.clear_widgets()
        self.add_widget(self.loading_circle)
        self.add_widget(self.scanning)
        threading.Thread(target=self.scan_wifi, daemon=True).start()

    def scan_wifi(self):
        wifi_list = get_available_wifi()
        # Update UI on the main thread
        Clock.schedule_once(lambda dt: self.show_results(wifi_list), 1)

    def show_results(self, wifi_list):
        self.clear_widgets()
        self.add_widget(self.header)
        if hasattr(self, 'loading_circle'):
            self.remove_widget(self.loading_circle)
        list_box = GridLayout(cols=1, size=(465, len(wifi_list) * 55), size_hint=(None,None), pos_hint=(None, None),)
        for wifi in wifi_list:
            button = SelectableButton(text=wifi, font_size=40,
                                                font_name='fonts/MPLUS1p-Regular.ttf', size_hint_y=None, 
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

        self.scan_wifi_button = IconTextButton(
            text=update_text_language("scan_wifi"),
            icon_path ='images/wifi.png',
            size = (140,140),
            pos_hint={'center_x': 0.25, 'center_y': 0.55},
            on_release=lambda x: self.pre_enter_loading()  # Re-scan Wi-Fi
        )
        self.connect_wifi_button = IconTextButton(
            text=update_text_language("connect_wifi"),
            icon_path ='images/connection.png',
            size = (140,140),
            pos_hint={'center_x': 0.25, 'center_y': 0.25},
            on_release=self.connect_wifi
        )
                
        scroll.add_widget(list_box)
        self.add_widget(scroll)
        self.add_widget(self.scan_wifi_button)
        self.add_widget(self.connect_wifi_button)

    def select_wifi(self, btn):
        for b in self.wifi_list:
            if b == btn:
                continue
            b.selected = False
            b.update_color()
        btn.selected = True
        btn.update_color()
        self.selected_wifi = btn.text
    
    def connect_wifi(self, instance):
        """
        Connect to the selected Wi-Fi network.
        """
        if not self.selected_wifi:
            print("No Wi-Fi selected")
            return
        print(f"Connecting to {self.selected_wifi}...")
        App.get_running_app().sm.current = 'wifi password'
        wifi_password_screen = App.get_running_app().sm.get_screen('wifi password')
        wifi_password_screen.wifi_name = self.selected_wifi

    def update_language(self):
        """
        Update the language of the widgets in this screen.
        """
        self.header.update_language()
        self.scanning.text = update_text_language('scanning_wifi')
        if hasattr(self, 'scan_wifi_button'):
            self.scan_wifi_button.label.text = update_text_language("scan_wifi")
        if hasattr(self, 'connect_wifi_button'):
            self.connect_wifi_button.label.text = update_text_language("connect_wifi")

def get_available_wifi():
    '''
    Get a list of available Wi-Fi networks based on the platform.
    Returns:
        list: A list of available Wi-Fi SSIDs.'''
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
            subprocess.run(['nmcli', 'dev', 'wifi', 'rescan'], check=True)
            time.sleep(1)  # Wait for the scan to complete
            result = subprocess.check_output(['nmcli', '-t', '-f', 'SSID', 'dev', 'wifi'], universal_newlines=True)
            wifi_list = [line for line in result.split('\n') if line]
        except Exception as e:
            print("Error getting Wi-Fi:", e)
    elif sys.platform.startswith('win'):
        try:
            #forcing a new scan everytime 
            subprocess.run(['nmcli', 'dev', 'wifi', 'rescan'], check=True)
            time.sleep(1)  # Wait for the scan to complete
            result = subprocess.check_output(['netsh', 'wlan', 'show', 'networks'], universal_newlines=True)
            for line in result.split('\n'):
                if "SSID" in line:
                    ssid = line.split(":", 1)[1].strip()
                    if ssid:
                        wifi_list.append(ssid)
        except Exception as e:
            print("Error getting Wi-Fi:", e)
    return wifi_list


class WifiPasswordScreen(KeyboardScreen):
    def __init__(self, title = 'wifi_password', wifi_name = None, **kwargs):
        super().__init__(**kwargs, title=title)
        self.wifi_name = wifi_name
        self.cancel_event = threading.Event()
        self.wifi_scan_button = IconTextButton(
            text="Wi-Fi SSID",
            icon_path ='images/wifi.png',
            size = (110,110),
            pos_hint={'center_x': 0.79, 'center_y': 0.86},
            on_release=self.go_to_wifi_scan
        )
        self.visibility_button = IconTextButton(
            icon_path ='images/visibility_on.png',
            size = (50,50),
            pos_hint={'center_x': 0.60, 'center_y': 0.81},
            on_press=self.freeze_ui,  # Freeze UI on press
            on_release=self.password_visibility
        )
        self.add_widget(self.wifi_scan_button)
        self.add_widget(self.visibility_button)

    def go_to_wifi_scan(self, instance):
        """
        Navigate back to the Wi-Fi scanning screen.
        """
        App.get_running_app().sm.current = 'wi-fi'
        wifi_loading_screen = App.get_running_app().sm.get_screen('wi-fi')
        wifi_loading_screen.selected_wifi = self.wifi_name

    def freeze_ui(self,instance):
        """
        Freeze the UI for a short duration to prevent rapid interactions.
        """
        freeze_ui(0.3)

    def password_visibility(self, instance):
        """
        Toggle the visibility of the password input.
        """
        self.keyboard.visibility = not self.keyboard.visibility
        if not self.keyboard.visibility:
            print("Hiding password")
            self.visibility_button.icon_path = 'images/visibility_off.png'
            self.visibility_button.image.source = self.visibility_button.icon_path  
            self.keyboard.text_input.text = "*" * len(self.keyboard.text_input.text)
        else:        
            print("Showing password")
            self.visibility_button.icon_path = 'images/visibility_on.png'
            self.visibility_button.image.source = self.visibility_button.icon_path  
            self.keyboard.text_input.text = self.keyboard.actual_text_input

    def press_enter(self, instance):
        password = self.keyboard.text_input.text.strip()
        print(f"Entered password: {password}")
        if not password:
            print("Password cannot be empty")
            return
        if not self.wifi_name:
            print("No Wi-Fi network selected")
            return
        self.cancel_event.clear()  # <-- Reset the event before starting a new connection
        app = App.get_running_app()
        app.sm.current = 'wifi connecting'
        connecting_screen = app.sm.get_screen('wifi connecting')
        connecting_screen.cancel_event = self.cancel_event  # Pass the event
        connecting_screen.process_holder = {}  

        # Connect in a background thread
        def do_connect():
            process_holder = connecting_screen.process_holder
            while not self.cancel_event.is_set():
                success = connect_wifi(self.wifi_name, password, cancel_event=self.cancel_event, process_holder=process_holder)
                # Save config and switch screen on main thread
                def after_connect(dt):
                    if success:
                        config = load_config('config/settings.json', 'v3_json')
                        config['wifi_ssid'] = self.wifi_name
                        config['wifi_password'] = password
                        save_config('config/settings.json', 'v3_json', data=config)
                        print(f"Connected to {self.wifi_name} with password: {password}")
                        App.get_running_app().sm.current = 'wifi connected'

                    else:
                        print(f"Failed to connect to {self.wifi_name} with password: {password}")
                        App.get_running_app().sm.current = 'wifi error'
                Clock.schedule_once(after_connect, 0)
                break

        threading.Thread(target=do_connect, daemon=True).start()

    def on_pre_enter(self):
        update_current_page('wifi password')
        self.keyboard.text_input.text = ""
        self.keyboard.actual_text_input = ""
 
    def update_language(self):
        return super().update_language()

class WifiConnectingScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cancel_event = None
        self.scanning = LoadingCircle(pos_hint={'center_x': 0.5, 'center_y': 0.6}, size=120, dot_color=(0.5, 0, 0.5, 1))
        self.label = Label(
            text= update_text_language('connecting'),
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.4},
            size_hint=(None, None),
            font_name='fonts/MPLUS1p-Bold.ttf',
            size=(400, 100)
        )
        self.cancel_button = IconTextButton(
            text=update_text_language("cancel"),
            font_size=30,
            size=(200, 90),
            pos_hint={'center_x': 0.5, 'center_y': 0.25},
            on_release=self.cancel_connection
        )
        
        self.add_widget(self.label)
        self.add_widget(self.scanning)
        self.add_widget(self.cancel_button)

    def update_language(self):
        """
        Update the language of the widgets in this screen.
        """
        self.label.text = update_text_language('connecting')
        self.cancel_button.label.text = update_text_language("cancel")

    def cancel_connection(self, instance):
        """
        Cancel the ongoing Wi-Fi connection attempt.
        """
        if self.cancel_event:
            self.cancel_event.set()
        if self.process_holder and 'proc' in self.process_holder:
            try:
                self.process_holder['proc'].terminate()
                print("Terminated the connection process.")
            except Exception as e:
                print(f"Error terminating process: {e}")
        App.get_running_app().sm.current = 'wifi password'

class WifiConnectedScreen(SafeScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(HeaderBar(title=" ",button_screen="menu2"))
        self.add_widget(Image(
            source='images/wifi.png',
            size_hint=(None, None),
            size=(200, 200),
            pos_hint={'center_x': 0.5, 'center_y': 0.6}
        ))

        self.connection_successful_label = Label(
            text=update_text_language('connection_successful'),
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.43},
            size_hint=(None, None),
            size=(400, 100),
            font_name='fonts/MPLUS1p-Regular.ttf'
        )
        self.add_widget(self.connection_successful_label)
        self.label = Label(
            text='temporary',
            font_size=60,
            color = (1,1,0,1),  # Yellow color for success
            pos_hint={'center_x': 0.5, 'center_y': 0.3},
            size_hint=(None, None),
            size=(400, 100),
            font_name='fonts/MPLUS1p-Regular.ttf'
        )
        self.add_widget(self.label)

    def on_pre_enter(self):
        update_current_page('wifi connected')
        wifi_name = App.get_running_app().sm.get_screen('wifi password').wifi_name
        self.label.text = wifi_name if wifi_name else "Unknown Network"

    def update_language(self):
        """
        Update the language of the widgets in this screen.
        """
        self.connection_successful_label.text = update_text_language('connection_successful')


class WifiErrorScreen(SafeScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(HeaderBar(title=" ",button_screen="menu2"))
        self.add_widget(Image(
            source='images/wifi_failed.png',
            size_hint=(None, None),
            size=(400, 400),
            pos_hint={'center_x': 0.5, 'center_y': 0.73}
        ))
        self.connection_failed = Label(
            text=update_text_language("connection_fail"),
            font_size=35,
            pos_hint={'center_x': 0.5, 'center_y': 0.6},
            size_hint=(None, None),
            size=(400, 100),
            font_name='fonts/MPLUS1p-Bold.ttf'
        )
        self.add_widget(self.connection_failed)
        self.label = Label(
            text="temporary",
            font_size=60,
            color = (1,1,0,1),  # Yellow color for error
            pos_hint={'center_x': 0.5, 'center_y': 0.48},
            size_hint=(None, None),
            size=(400, 100),
            font_name='fonts/MPLUS1p-Bold.ttf'
        )
        self.check_password_label = Label(
            text=update_text_language("check_password"),
            font_size=30,
            pos_hint={'center_x': 0.5, 'center_y': 0.38},
            size_hint=(None, None),
            font_name='fonts/MPLUS1p-Regular.ttf',
        )
        self.retry_button = IconTextButton(
            text=update_text_language("try_again"),
            size=(300,80),
            font_size=30,
            pos_hint={'center_x': 0.5, 'center_y': 0.22},
            screen_name='wifi password',
            font_name='fonts/MPLUS1p-Regular.ttf'
        )

        self.add_widget(self.label)
        self.add_widget(self.check_password_label)
        self.add_widget(self.retry_button)

    def on_pre_enter(self):
        update_current_page('wifi error')
        wifi_name = App.get_running_app().sm.get_screen('wifi password').wifi_name
        self.label.text = wifi_name if wifi_name else "Unknown Network"

    def update_language(self):
        """
        Update the language of the widgets in this screen.
        """
        self.retry_button.label.text = update_text_language("try_again")
        self.connection_failed.text = update_text_language("connection_fail")
        self.check_password_label.text = update_text_language("check_password")


####### connecting wifi #########

def connect_wifi_linux(ssid, password, cancel_event=None, process_holder=None):
    try:
        cmd = ['nmcli', 'dev', 'wifi', 'connect', ssid, 'password', password]
        proc = subprocess.Popen(cmd)
        if process_holder is not None:
            process_holder['proc'] = proc
        while proc.poll() is None:
            if cancel_event and cancel_event.is_set():
                proc.terminate()
                print("Connection cancelled by user.")
                return False
            time.sleep(0.1)
        return proc.returncode == 0
    except Exception as e:
        print(f"Failed to connect: {e}")
        return False

def connect_wifi_mac(ssid, password, cancel_event=None, process_holder=None):
    try:
        # Find your Wi-Fi device name (usually 'en0')
        device = 'en0'
        subprocess.run(['networksetup', '-setairportnetwork', device, ssid, password], check=True)
        print(f"Connected to {ssid}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to connect: {e}")
        return False

def connect_wifi_windows(ssid):
    try:
        subprocess.run(['netsh', 'wlan', 'connect', f'name={ssid}'], check=True)
        print(f"Connected to {ssid}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to connect: {e}")
        return False

def connect_wifi(ssid, password, cancel_event=None, process_holder=None):
    if sys.platform.startswith('linux'):
        return connect_wifi_linux(ssid, password, cancel_event=cancel_event, process_holder=process_holder)
    elif sys.platform == 'darwin':
        return connect_wifi_mac(ssid, password, cancel_event=cancel_event, process_holder=process_holder)
    elif sys.platform.startswith('win'):
        return connect_wifi_windows(ssid)
    else:
        print("Unsupported platform")
        return False
    

######### checking connected wifi #########
import subprocess

def get_connected_wifi_linux():
    try:
        result = subprocess.check_output(
            ['nmcli', '-t', '-f', 'active,ssid', 'dev', 'wifi'],
            universal_newlines=True
        )
        for line in result.split('\n'):
            if line.startswith('yes:'):
                return line.split(':', 1)[1]
    except Exception as e:
        print("Error getting connected Wi-Fi:", e)
    return None

import subprocess

def get_connected_wifi_mac():
    try:
        result = subprocess.check_output(
            ["/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport", "-I"],
            universal_newlines=True
        )
        for line in result.split('\n'):
            if " SSID:" in line:
                return line.split("SSID:")[1].strip()
    except Exception as e:
        print("Error getting connected Wi-Fi:", e)
    return None

import subprocess

def get_connected_wifi_windows():
    try:
        result = subprocess.check_output(
            ['netsh', 'wlan', 'show', 'interfaces'],
            universal_newlines=True
        )
        for line in result.split('\n'):
            if "SSID" in line and "BSSID" not in line:
                return line.split(":", 1)[1].strip()
    except Exception as e:
        print("Error getting connected Wi-Fi:", e)
    return None

def get_connected_wifi():
    if sys.platform == 'darwin':
        return get_connected_wifi_mac()
    elif sys.platform.startswith('linux'):
        return get_connected_wifi_linux()
    elif sys.platform.startswith('win'):
        return get_connected_wifi_windows()
    return None

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
        #self.bind(on_release=self.on_press)
    
    def _update_rect(self, *args):
        """
        Update the rectangle size and position when the button is resized or moved.
        """
        self.rect.pos = self.pos
        self.rect.size = self.size

    def update_color(self):
        #print(self.text, "selected:", self.selected)
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
        self.selection.selected_wifi = self.text
        #print(f"Selected Wi-Fi: {self.text}")
        self.selection.select_wifi(self)

