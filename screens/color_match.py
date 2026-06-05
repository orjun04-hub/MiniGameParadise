# screens/color_match.py 전체 코드
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.app import App
import random

FONT = 'NanumGothic'

class ColorMatchScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.score = 0
        self.app = App.get_running_app()
        
        self.color_names = ['빨강', '파랑', '초록', '노랑']
        self.color_hexes = [
            (0.9, 0.3, 0.3, 1), # 빨강
            (0.2, 0.6, 0.9, 1), # 파랑
            (0.2, 0.8, 0.4, 1), # 초록
            (0.9, 0.8, 0.2, 1)  # 노랑
        ]
        
        with self.canvas.before:
            Color(*self.app.bg_color)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        layout = BoxLayout(orientation='vertical', padding=30, spacing=15)
        
        self.info_label = Label(text='단어와 색상이 일치할 때만 [일치]를 누르세요!', font_size=18, font_name=FONT, size_hint_y=0.15, color=self.app.text_dark)
        self.text_target = Label(text='단어', font_size=40, font_name=FONT, bold=True, size_hint_y=0.2, color=self.app.text_dark)
        
        # 색상이 보일 커스텀 박스
        self.color_box = Label(text='?', font_size=28, font_name=FONT, size_hint_y=0.3, color=(1, 1, 1, 1))
        with self.color_box.canvas.before:
            self.box_color = Color(0.5, 0.5, 0.5, 1)
            self.box_rect = Rectangle(size=self.color_box.size, pos=self.color_box.pos)
        self.color_box.bind(size=self._update_box, pos=self._update_box)
        
        btn_layout = BoxLayout(spacing=20, size_hint_y=0.15)
        btn_match = Button(text='⭕ 일치', font_size=20, font_name=FONT, bold=True, background_color=self.app.primary_color, background_normal='')
        btn_match.bind(on_press=lambda x: self.check_answer(True))
        btn_miss = Button(text='❌ 불일치', font_size=20, font_name=FONT, bold=True, background_color=self.app.accent_color, background_normal='')
        btn_miss.bind(on_press=lambda x: self.check_answer(False))
        btn_layout.add_widget(btn_match)
        btn_layout.add_widget(btn_miss)
        
        self.back_btn = Button(text='메뉴로', font_size=16, font_name=FONT, size_hint_y=0.1, background_color=(0.5, 0.5, 0.5, 1), background_normal='')
        self.back_btn.bind(on_press=self.go_back)
        
        layout.add_widget(self.info_label)
        layout.add_widget(self.text_target)
        layout.add_widget(self.color_box)
        layout.add_widget(btn_layout)
        layout.add_widget(self.back_btn)
        self.add_widget(layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def _update_box(self, instance, value):
        self.box_rect.pos = instance.pos
        self.box_rect.size = instance.size

    def on_enter(self):
        self.score = 0
        self.info_label.text = '현재 점수: 0점'
        self.info_label.color = self.app.text_dark
        self.next_round()

    def next_round(self):
        self.word_idx = random.randint(0, 3)
        self.visual_idx = random.randint(0, 3)
        
        self.text_target.text = f"제시 단어: [ {self.color_names[self.word_idx]} ]"
        self.box_color.rgba = self.color_hexes[self.visual_idx]
        self.color_box.text = "이 색상은?!"

    def check_answer(self, user_said_match):
        is_match = (self.word_idx == self.visual_idx)
        if user_said_match == is_match:
            self.score += 1
            self.app.play_sound('success')
            self.info_label.text = f'정답! 🎉 현재 점수: {self.score}점'
            self.info_label.color = self.app.primary_color
            self.next_round()
        else:
            self.app.play_sound('fail')
            self.app.add_ranking("color_match", self.app.player_name, self.score)
            self.info_label.text = f'❌ 오답! 게임 종료. 최종 점수: {self.score}점'
            self.info_label.color = self.app.accent_color
            self.text_target.text = '게임 오버'

    def go_back(self, *a):
        self.app.play_sound('click')
        self.manager.current = 'menu'