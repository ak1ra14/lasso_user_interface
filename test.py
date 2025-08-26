# -*- coding: utf-8 -*-
# Kivy 日本語フリックキーボード（最小実装）
# 依存: kivy >= 2.2.0
# 実行: python main.py

from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.behaviors import ButtonBehavior
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.properties import ListProperty, StringProperty, NumericProperty, BooleanProperty, ObjectProperty
from kivy.clock import Clock
import math

# --- ユーティリティ: 濁点・半濁点、小文字化 ---
DAKUTEN_MAP = {
    'か': 'が', 'き': 'ぎ', 'く': 'ぐ', 'け': 'げ', 'こ': 'ご',
    'さ': 'ざ', 'し': 'じ', 'す': 'ず', 'せ': 'ぜ', 'そ': 'ぞ',
    'た': 'だ', 'ち': 'ぢ', 'つ': 'づ', 'て': 'で', 'と': 'ど',
    'は': 'ば', 'ひ': 'び', 'ふ': 'ぶ', 'へ': 'べ', 'ほ': 'ぼ',
    'う': 'ゔ'
}
HANDAKUTEN_MAP = {
    'は': 'ぱ', 'ひ': 'ぴ', 'ふ': 'ぷ', 'へ': 'ぺ', 'ほ': 'ぽ'
}
SMALL_MAP = {
    'あ': 'ぁ', 'い': 'ぃ', 'う': 'ぅ', 'え': 'ぇ', 'お': 'ぉ',
    'や': 'ゃ', 'ゆ': 'ゅ', 'よ': 'ょ', 'つ': 'っ', 'わ': 'ゎ'
}

# --- FlickKey ウィジェット ---
class FlickKey(ButtonBehavior, RelativeLayout):
    # variants[0] = タップ（中央）/ [1]=上, [2]=右, [3]=下, [4]=左
    variants = ListProperty(['あ', 'い', 'う', 'え', 'お'])
    label = ObjectProperty(None)
    radius = NumericProperty(12)
    selected_dir = NumericProperty(-1)
    start_pos = ListProperty([0, 0])
    moved = BooleanProperty(False)
    threshold = NumericProperty(20)  # ピクセル

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0.12, 0.12, 0.14, 1)
            self.bg = RoundedRectangle(radius=[self.radius]*4)
        self.label = Label(text=self.variants[0], font_name="fonts/MPLUS1p-Regular.ttf", font_size='24sp', color=(1,1,1,1))
        self.add_widget(self.label)
        self.bind(pos=self._update_bg, size=self._update_bg)

    def on_variants(self, *args):
        # 中央表示を更新
        if self.label:
            self.label.text = self.variants[0]

    def _update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size
        if self.label:
            self.label.center = self.center

    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            return False
        self.start_pos = touch.pos
        self.moved = False
        self.selected_dir = -1
        self._draw_radar(show=True)
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if not self.collide_point(*touch.pos):
            return False
        dx = touch.x - self.start_pos[0]
        dy = touch.y - self.start_pos[1]
        dist = math.hypot(dx, dy)
        if dist < self.threshold:
            self.moved = False
            self.selected_dir = -1
            self._draw_radar(show=True, hover=-1)
            return True
        self.moved = True
        angle = math.degrees(math.atan2(dy, dx))  # -180..180, 0が右
        # 方向を 1:上, 2:右, 3:下, 4:左 に量子化
        if -45 <= angle <= 45:
            direction = 2  # 右
        elif 45 < angle < 135:
            direction = 1  # 上
        elif -135 < angle < -45:
            direction = 3  # 下
        else:
            direction = 4  # 左
        self.selected_dir = direction
        self._draw_radar(show=True, hover=direction)
        return True

    def on_touch_up(self, touch):
        if not self.collide_point(*touch.pos):
            self._draw_radar(show=False)
            return False
        self._draw_radar(show=False)
        idx = 0
        if self.moved and self.selected_dir in (1,2,3,4):
            idx = self.selected_dir
        char = self.variants[idx] if idx < len(self.variants) else self.variants[0]
        self.dispatch('on_press')  # ButtonBehavior hooks
        self.dispatch('on_release')
        # カスタムイベントで親へ通知
        if hasattr(self.parent, 'emit_char'):
            self.parent.emit_char(char)
        return True

    # 簡易レーダー（ガイド円と方向）
    def _draw_radar(self, show=True, hover=-1):
        self.canvas.after.clear()
        if not show:
            return
        with self.canvas.after:
            Color(1,1,1,0.15)
            Line(circle=(self.center_x, self.center_y, 28), width=1)
            # 各方向のラベル
            dirs = {1:(0, 22), 2:(22, 0), 3:(0,-22), 4:(-22,0)}
            for i in range(1,5):
                dx, dy = dirs[i]
                cx, cy = self.center_x + dx, self.center_y + dy
                Color(1,1,1, 0.28 if i==hover else 0.12)
                RoundedRectangle(pos=(cx-14, cy-14), size=(28,28), radius=[10,])
                # 文字
                lab = Label(text=self.variants[i] if i < len(self.variants) else '', font_size='16sp', font_name="fonts/MPLUS1p-Regular.ttf", color=(1,1,1,0.9))
                # 一時的に配置
                w = Widget(size=(0,0), pos=(cx-8, cy-10))
                self.add_widget(w)
                lab.pos = (cx-8, cy-12)
                self.add_widget(lab)
                # すぐ消す（描画のみの簡易手段）
            # NOTE: Kivy の正攻法では Canvas + CoreLabel を使うが、簡易実装。


# --- キーボード本体 ---
class FlickKeyboard(GridLayout):
    text_target = ObjectProperty(None)

    # 12キー（3x4）: あ/か/さ, た/な/は, ま/や/ら, わ/スペース/削除
    LAYOUT = [
        ['あ', 'い', 'う', 'え', 'お'],
        ['か', 'き', 'く', 'け', 'こ'],
        ['さ', 'し', 'す', 'せ', 'そ'],
        ['た', 'ち', 'つ', 'て', 'と'],
        ['な', 'に', 'ぬ', 'ね', 'の'],
        ['は', 'ひ', 'ふ', 'へ', 'ほ'],
        ['ま', 'み', 'む', 'め', 'も'],
        ['や', 'ゃ', 'ゆ', 'ょ', 'ー'],  # 中央:や、上下左右:小/ゆ/小/長音（例）
        ['ら', 'り', 'る', 'れ', 'ろ'],
        ['わ', 'を', 'ん', 'ー', '・'],
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 3
        self.rows = 4
        self.spacing = 6
        self.padding = 6
        # キー配置
        keys = [
            ['あ', 'か', 'さ'],
            ['た', 'な', 'は'],
            ['ま', 'や', 'ら'],
            ['わ', '空白', '削除']
        ]
        # 対応するフリック配列
        group = {
            'あ': ['あ','い','う','え','お'],
            'か': ['か','き','く','け','こ'],
            'さ': ['さ','し','す','せ','そ'],
            'た': ['た','ち','つ','て','と'],
            'な': ['な','に','ぬ','ね','の'],
            'は': ['は','ひ','ふ','へ','ほ'],
            'ま': ['ま','み','む','め','も'],
            'や': ['や','ゃ','ゆ','ょ','ー'],
            'ら': ['ら','り','る','れ','ろ'],
            'わ': ['わ','を','ん','ー','・']
        }
        for r in range(4):
            for c in range(3):
                label = keys[r][c]
                if label in ('空白','削除'):
                    # 特殊キー
                    fk = FlickKey(variants=[label, label, label, label, label])
                else:
                    fk = FlickKey(variants=group[label])
                self.add_widget(fk)
        # 最下段に機能キー行を追加（濁点/半濁点/小/確定）
        self.func_row = BoxLayout(size_hint_y=None, height=56, spacing=6)
        for k in ['濁点', '半濁点', '小', '確定']:
            fk = FlickKey(variants=[k, k, k, k, k])
            self.func_row.add_widget(fk)
        wrapper = BoxLayout(orientation='vertical', spacing=6)
        wrapper.add_widget(self)
        wrapper.add_widget(self.func_row)
        self.wrapper = wrapper

    def on_parent(self, *args):
        # グリッドを wrapper に差し替える
        if isinstance(self.parent, BoxLayout):
            return

    # TextInput に文字を流す
    def emit_char(self, ch):
        ti = self.text_target
        if not ti:
            return
        if ch == '削除':
            if ti.cursor_index() > 0:
                i = ti.cursor_index()
                ti.text = ti.text[:i-1] + ti.text[i:]
                ti.cursor = (max(0, ti.cursor_col-1), ti.cursor_row)
            return
        if ch == '空白':
            ti.insert_text(' ')
            return
        if ch == '濁点':
            self._apply_voicing(ti, handaku=False)
            return
        if ch == '半濁点':
            self._apply_voicing(ti, handaku=True)
            return
        if ch == '小':
            self._apply_small(ti)
            return
        if ch == '確定':
            # 実アプリでは IME 確定や送信にマップ
            ti.insert_text('\n')
            return
        # 通常文字
        ti.insert_text(ch)

    def _apply_voicing(self, ti: TextInput, handaku=False):
        i = ti.cursor_index()
        if i == 0:
            return
        prev = ti.text[i-1]
        if handaku:
            rep = HANDAKUTEN_MAP.get(prev)
        else:
            rep = DAKUTEN_MAP.get(prev)
        if rep:
            ti.text = ti.text[:i-1] + rep + ti.text[i:]
            ti.cursor = (ti.cursor_col, ti.cursor_row)
        else:
            # 合成できなければ記号として追加
            ti.insert_text('゛' if not handaku else '゜')

    def _apply_small(self, ti: TextInput):
        i = ti.cursor_index()
        if i == 0:
            ti.insert_text('っ')
            return
        prev = ti.text[i-1]
        rep = SMALL_MAP.get(prev)
        if rep:
            ti.text = ti.text[:i-1] + rep + ti.text[i:]
        else:
            ti.insert_text('っ')


class DemoRoot(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', spacing=8, padding=8, **kwargs)
        self.preview = TextInput(hint_text='ここに入力されます', size_hint_y=None, height=120, font_size='22sp')
        self.add_widget(self.preview)
        self.kb_container = BoxLayout(orientation='vertical')
        self.add_widget(self.kb_container)
        # キーボード生成
        self.kb = FlickKeyboard()
        self.kb.text_target = self.preview
        # FlickKeyboard は wrapper(本体+機能キー行)を持つ
        self.kb_container.add_widget(self.kb.wrapper)


class FlickIMEApp(App):
    def build(self):
        self.title = 'Kivy 日本語フリックキーボード（サンプル）'
        return DemoRoot()


if __name__ == '__main__':
    FlickIMEApp().run()
