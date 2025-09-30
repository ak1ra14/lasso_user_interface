from kivy.core.audio import SoundLoader
from kivy.logger import Logger
import sys
from utils.config_loader import load_config

class SoundManager:
    def __init__(self):
        self.tap_sound = SoundLoader.load('sound/tap.wav')
        self.alert_sound = SoundLoader.load('sound/alertsound.wav')
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
        try:
            if self.tap_sound:
                self.tap_sound.stop()
                self.tap_sound.play()
        except Exception as e:
            Logger.error(f"Error playing tap sound: {e}")
            
    def play_alert(self):
        try:
            if self.alert_sound:
                self.alert_sound.stop()
                self.alert_sound.play()
        except Exception as e:
            Logger.error(f"Error playing alert sound: {e}")