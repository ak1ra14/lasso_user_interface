import os,sys 

from kivy.config import Config

if sys.platform.startswith('linux'):
    Config.set('input', 'mouse', 'mouse,disable')
    Config.set('graphics', 'show_cursor', 0)

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.core.audio import SoundLoader
from kivy.uix.label import Label

class TestSoundApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
        self.label = Label(text="Press to play sound", font_size=32)
        layout.add_widget(self.label)
        btn = Button(text="Play Sound", font_size=28, size_hint=(1, 0.3))
        btn.bind(on_release=self.play_sound)
        layout.add_widget(btn)
        return layout

    def play_sound(self, instance):
        sound = SoundLoader.load('sound/tap.mp3')
        if sound:
            sound.play()
            self.label.text = "Playing sound!"
        else:
            self.label.text = "Sound file not found or unsupported format."

if __name__ == "__main__":
    TestSoundApp().run()