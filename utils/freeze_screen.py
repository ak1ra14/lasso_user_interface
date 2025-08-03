from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.app import App
from kivy.clock import Clock

class UILockOverlay(FloatLayout):
    def on_touch_down(self, touch):
        return True  # Block all touches
    def on_touch_move(self, touch):
        return True
    def on_touch_up(self, touch):
        return True

def freeze_ui(duration=0.3):
    app = App.get_running_app()
    if not hasattr(app, 'ui_lock_overlay'):
        app.ui_lock_overlay = UILockOverlay(size_hint=(1, 1))
    overlay = app.ui_lock_overlay
    if overlay.parent is None:
        Window.add_widget(overlay)  # Add overlay to the Window, not just root
        Clock.schedule_once(lambda dt: Window.remove_widget(overlay), duration)