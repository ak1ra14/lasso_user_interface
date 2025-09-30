from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.floatlayout import FloatLayout
from kivy.logger import Logger
from utils.as_freeze_screen import freeze_ui

class FlickPopup(FloatLayout):
    '''
    A popup that appears to select different characters in the same character column when a flick key is pressed.
    '''
    def __init__(self, mappings, center_pos, font_name, font_size=32, **kwargs):
        super().__init__(size_hint=(None, None), **kwargs)
        self.size = (270, 270)
        self.pos = (center_pos[0] - self.size[0] // 2, center_pos[1] - self.size[1] // 2)
        self.labels = []
        # Order: center, up, right, down, left
        positions = [
            (135, 135),  # center (popup center is at (135, 135) in a 270x270 popup)
            (45, 135),   # left
            (135, 225),  # up
            (225, 135),  # right
            (135, 45),   # down
        ]

        for i, char in enumerate(mappings):
            if not char: continue
            lbl = Label(text=char, font_size=font_size, font_name=font_name,
                        size_hint=(None, None), size=(90, 90),
                        pos=(self.pos[0] + positions[i][0] - 45, self.pos[1] + positions[i][1] - 45),
                        color=(1,1,1,1))
            with lbl.canvas.before:
                lbl.bg_color = Color(0.22, 0.45, 0.91, 0.7 if i==0 else 0.5)
                lbl.bg_rect = RoundedRectangle(pos=lbl.pos, size=lbl.size, radius=[20])

            self.add_widget(lbl)
            self.labels.append(lbl)

    def highlight(self, idx):
        for i, lbl in enumerate(self.labels):
            lbl.bg_color.a = 1.0 if i == idx else (0.7 if i==0 else 0.5)

class FlickKey(Button):
    '''
    A button that supports flick gestures to input different characters.'''
    def __init__(self, mappings,keyboard, overlay=None, threshold=20, **kwargs):
        super().__init__(**kwargs)
        self.mappings = list(mappings) + [None] * (5 - len(mappings))
        self.keyboard = keyboard  # Store a reference to the keyboard
        self.overlay = overlay  # pass overlay from parent
        self._touch_start = None
        self.popup = None
        self.threshold = threshold
        self.font_size = kwargs.get('font_size', 28)
        self.text = self.mappings[0] or ''
        self.font_name = kwargs.get('font_name', 'fonts/MPLUS1p-Regular.ttf')
        self.background_normal = ''
        self.background_down = ''
        self.background_color = (0,0,0,0)
        self.chosen=None
        with self.canvas.before:
            self.color_instruction = Color(rgba=(0.2, 0.2, 0.2, 1))
            self.rounded_rect_instruction = RoundedRectangle(
                pos=self.pos, size=self.size, radius=[20,]
            )
        self.bind(pos=self._update_rect, size=self._update_rect)

    def on_touch_down(self, touch):
        '''
        Handle touch down event to show the flick popup.'''
        if not self.collide_point(*touch.pos):
            return False
        self._touch_start = touch.pos
        # Calculate FlickKey center in window coordinates
        key_cx, key_cy = self.to_window(*self.center)
        # Calculate overlay's bottom-left in window coordinates
        overlay_cx, overlay_cy = self.overlay.to_window(*self.overlay.pos)
        # Popup center relative to overlay
        popup_center = (key_cx - overlay_cx, key_cy - overlay_cy)
        if not self.popup:
            self.popup = FlickPopup(self.mappings, popup_center, self.font_name, font_size=32)
            self.overlay.add_widget(self.popup)

        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        '''
        Handle touch move event to update the highlighted character in the popup.'''
        if self._touch_start is None or not self.popup:
            return False
        dx = touch.x - self._touch_start[0]
        dy = touch.y - self._touch_start[1]
        idx = 0  # center
        if abs(dx) + abs(dy) >= self.threshold:
            if abs(dx) > abs(dy):
                idx = 3 if dx > 0 else 1
            else:
                idx = 2 if dy > 0 else 4
        self.popup.highlight(idx)
        return True

    def on_touch_up(self, touch):
        '''
        Handle touch up event to select the character and remove the popup.
        '''
        if self._touch_start is None or not self.popup:
            return super().on_touch_up(touch)
        dx = touch.x - self._touch_start[0]
        dy = touch.y - self._touch_start[1]
        idx = 0
        if abs(dx) + abs(dy) >= self.threshold:
            if abs(dx) > abs(dy):
                idx = 3 if dx > 0 else 1
            else:
                idx = 2 if dy > 0 else 4
        self.idx = idx
        self.chosen = self.mappings[idx]

        # Remove popup
        if self.popup and self.popup.parent:
            self.popup.parent.remove_widget(self.popup)
        self.popup = None
        self._touch_start = None

        # Force a release event so on_key_release will always fire
        self.dispatch('on_release')
        return True

    def _update_rect(self, instance, value):
        """Callback to update the position and size of the rounded rectangle."""
        self.rounded_rect_instruction.pos = instance.pos
        self.rounded_rect_instruction.size = instance.size
    
    def _update_color(self, instance, value):
        """Callback to update the color of the rounded rectangle."""
        self.color_instruction.rgba = value

    def on_press(self):
        if self.keyboard.last_click_space:
            print('resetting index due to space key')
            self.keyboard.last_click_space = False
            self.keyboard.converting = False
            self.keyboard.japanese_space_button.text = '空白'
            self.keyboard.flick_space_button.text = '空白'
            self.keyboard.start_index = self.keyboard.text_input.cursor_index()
        freeze_ui(0.2)



