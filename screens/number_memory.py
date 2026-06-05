# screens/number_memory.py 전체 코드
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.app import App
import random

FONT = 'NanumGothic'

class NumberMemoryScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.level = 1
        self.current_number = ''
        self.app = App.get_running_app()
        
        with self.canvas.before:
            Color(*self.app.bg_color)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        self.layout = BoxLayout(orientation='vertical', padding=30, spacing=15)
        
        self.info_label = Label(text='숫자 기억 게임', font_size=24, font_name=FONT, size_hint_y=0.15, color=self.app.text_dark)
        self.number_label = Label(text='준비', font_size=48, font_name=FONT, bold=True, size_hint_y=0.4, color=self.app.primary_color)
        
        self.input_field = TextInput(font_size=24, font_name=FONT, multiline=False, size_hint_y=0.15, hint_text='기억한 숫자를 입력하세요', halign='center', disabled=True)
        
        self.action_btn = Button(text='시작하기', font_size=20, font_name=FONT, size_hint_y=0.15, background_color=self.app.secondary_color, background_normal='')
        self.action_btn.bind(on_press=self.handle_action)
        
        self.back_btn = Button(text='메뉴로', font_size=16, font_name=FONT, size_hint_y=0.1, background_color=(0.5, 0.5, 0.5, 1), background_normal='')
        self.back_btn.bind(on_press=self.go_back)
        
        self.layout.add_widget(self.info_label)
        self.layout.add_widget(self.number_label)
        self.layout.add_widget(self.input_field)
        self.layout.add_widget(self.action_btn)
        self.layout.add_widget(self.back_btn)
        self.add_widget(self.layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def on_enter(self):
        self.level = 1
        self.number_label.text = '준비'
        self.number_label.color = self.app.primary_color
        self.info_label.text = '숫자 기억 게임'
        self.input_field.text = ''
        self.input_field.disabled = True
        self.action_btn.text = '시작하기'
        self.action_btn.disabled = False

    def handle_action(self, instance):
        self.app.play_sound('click')
        if self.action_btn.text in ['시작하기', '다음 레벨']:
            self.input_field.text = ''
            self.input_field.disabled = True
            self.current_number = ''.join([str(random.randint(0, 9)) for _ in range(self.level)])
            self.number_label.text = self.current_number
            self.action_btn.disabled = True
            Clock.schedule_once(self.hide_number, max(1.5, self.level * 0.8))
        elif self.action_btn.text == '정답 제출':
            user_input = self.input_field.text.strip()
            if user_input == self.current_number:
                self.app.play_sound('success')
                self.number_label.text = '정답입니다! ⭕'
                self.number_label.color = self.app.primary_color
                self.level += 1
                self.action_btn.text = '다음 레벨'
            else:
                self.app.play_sound('fail')
                self.number_label.text = f'오답입니다! ❌\n정답: {self.current_number}'
                self.number_label.color = self.app.accent_color
                self.app.add_ranking("number_memory", self.app.player_name, self.level - 1)
                self.action_btn.text = '게임 종료'
                self.action_btn.disabled = True

    def hide_number(self, dt):
        self.number_label.text = '❓'
        self.input_field.disabled = False
        self.input_field.focus = True
        self.action_btn.text = '정답 제출'
        self.action_btn.disabled = False

    def go_back(self, *a):
        self.app.play_sound('click')
        self.manager.current = 'menu'