from kivy.core.audio import SoundLoader
from kivy.logger import Logger
import sys, subprocess

from as_utils.as_config_loader import load_config

class SoundManager:
    def __init__(self):
        self.tap_sound = SoundLoader.load('as_sound/tap.mp3')
        self.alert_sound = SoundLoader.load('as_sound/alertsound.mp3')
        self.sound_with_usbsoundcard = load_config("as_config/settings.json","v3_json").get("sound_with_usbsoundcard")
        # Log sound loading status
        if self.tap_sound:
            Logger.info(f"SoundManager: Tap sound loaded successfully")
        else:
            Logger.error(f"SoundManager: Failed to load tap sound")
            
        if self.alert_sound:
            Logger.info(f"SoundManager: Alert sound loaded successfully")
            # Set volume to max for alert sound
            self.alert_sound.volume = 1.0
        else:
            Logger.error(f"SoundManager: Failed to load alert sound")
            
        
    def play_tap(self):
        self.play_sound(sound_file="as_sound/tap.wav")

    def play_alert(self):
        self.play_sound(sound_file="as_sound/alertsound.wav")


    def play_sound(self,sound_file="as_sound/tap.wav"):
        try:
            if sys.platform.startswith("linux"):
                if self.sound_with_usbsoundcard:
                    subprocess.Popen(['aplay', '-D', 'plughw:2,0', sound_file], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                else:
                    subprocess.Popen(['aplay', sound_file], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            elif sys.platform == "darwin":  # macOS
                subprocess.Popen(['afplay', sound_file], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except:
            Logger.error(f"SoundManager: Failed to play sound")


