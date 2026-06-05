# screens/quick_math.py 전체 코드
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.app import App
import random

FONT = 'NanumGothic'

class QuickMathScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.score = 0
        self.app = App.get_running_app()
        
        with self.canvas.before:
            Color(*self.app.bg_color)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        layout = BoxLayout(orientation='vertical', padding=30, spacing=15)
        
        self.info_label = Label(text='수식이 올바르면 ⭕, 틀리면 ❌!', font_size=18, font_name=FONT, size_hint_y=0.15, color=self.app.text_dark)
        self.math_label = Label(text='1 + 1 = 2', font_size=46, font_name=FONT, bold=True, size_hint_y=0.4, color=self.app.secondary_color)
        
        btn_layout = BoxLayout(spacing=20, size_hint_y=0.2)
        btn_o = Button(text='⭕ 맞음', font_size=22, font_name=FONT, bold=True, background_color=self.app.primary_color, background_normal='')
        btn_o.bind(on_press=lambda x: self.check_answer(True))
        btn_x = Button(text='❌ 틀림', font_size=22, font_name=FONT, bold=True, background_color=self.app.accent_color, background_normal='')
        btn_x.bind(on_press=lambda x: self.check_answer(False))
        btn_layout.add_widget(btn_o)
        btn_layout.add_widget(btn_x)
        
        self.back_btn = Button(text='메뉴로', font_size=16, font_name=FONT, size_hint_y=0.15, background_color=(0.5, 0.5, 0.5, 1), background_normal='')
        self.back_btn.bind(on_press=self.go_back)
        
        layout.add_widget(self.info_label)
        layout.add_widget(self.math_label)
        layout.add_widget(btn_layout)
        layout.add_widget(self.back_btn)
        self.add_widget(layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def on_enter(self):
        self.score = 0
        self.info_label.text = '현재 콤보: 0점'
        self.info_label.color = self.app.text_dark
        self.next_problem()

    def next_problem(self):
        a = random.randint(5, 30)
        b = random.randint(5, 30)
        self.is_correct = random.choice([True, False])
        
        if self.is_correct:
            ans = a + b
        else:
            ans = a + b + random.choice([-3, -1, 1, 2, 5])
            if ans == a + b: 
                ans += 1
                
        self.math_label.text = f"{a} + {b} = {ans}"

    def check_answer(self, user_ans):
        if user_ans == self.is_correct:
            self.score += 1
            self.app.play_sound('success')
            self.info_label.text = f'연속 정답! 🔥 현재 콤보: {self.score}점'
            self.info_label.color = self.app.primary_color
            self.next_problem()
        else:
            self.app.play_sound('fail')
            self.app.add_ranking("quick_math", self.app.player_name, self.score)
            self.info_label.text = f'❌ 틀렸습니다! 최종 점수: {self.score}점'
            self.info_label.color = self.app.accent_color
            self.math_label.text = '게임 오버'

    def go_back(self, *a):
        self.app.play_sound('click')
        self.manager.current = 'menu'