# screens/reaction_speed.py 전체 코드
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.app import App
import random, time

FONT = 'NanumGothic'

class ReactionSpeedScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.state = 'ready'
        self.scheduled_event = None
        self.app = App.get_running_app()
        
        self.trials = []  # 3회 측정 기록 저장 리스트
        
        with self.canvas.before:
            Color(*self.app.bg_color)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        layout = BoxLayout(orientation='vertical', padding=30, spacing=15)
        self.info_label = Label(
            text='[총 3회 측정]\n버튼이 초록색으로 변할 때 광속 클릭!', font_size=22, font_name=FONT,
            size_hint_y=0.25, halign='center', color=self.app.text_dark
        )
        self.action_btn = Button(
            text='시작하기', font_size=28, font_name=FONT,
            size_hint_y=0.6, background_color=self.app.secondary_color, background_normal=''
        )
        self.action_btn.bind(on_press=self.handle_press)
        
        self.back_btn = Button(
            text='메뉴로', font_size=18, font_name=FONT,
            size_hint_y=0.15, background_color=(0.5, 0.5, 0.5, 1), background_normal=''
        )
        self.back_btn.bind(on_press=self.go_back)
        
        layout.add_widget(self.info_label)
        layout.add_widget(self.action_btn)
        layout.add_widget(self.back_btn)
        self.add_widget(layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def on_enter(self):
        self.state = 'ready'
        self.trials = []
        self.action_btn.text = '시작하기'
        self.action_btn.background_color = self.app.secondary_color
        self.info_label.text = '[총 3회 측정]\n버튼이 초록색으로 변할 때 광속 클릭!'

    def handle_press(self, *a):
        if self.state == 'ready':
            self.app.play_sound('click')
            self.state = 'waiting'
            self.action_btn.text = '기다리세요...'
            self.action_btn.background_color = self.app.accent_color
            delay = random.uniform(2.0, 4.5)
            self.scheduled_event = Clock.schedule_once(self.turn_green, delay)
            
        elif self.state == 'waiting':
            # 부정행위 (초록 불 켜지기 전에 성급하게 연타한 경우)
            if self.scheduled_event:
                self.scheduled_event.cancel()
            self.app.play_sound('fail')
            self.info_label.text = '⚠️ 너무 빨랐습니다! 파울! 다시 조준하세요.'
            self.state = 'ready'
            self.action_btn.text = '재도전'
            self.action_btn.background_color = self.app.secondary_color
            
        elif self.state == 'green':
            reaction_time = int((time.time() - self.green_time) * 1000)
            self.trials.append(reaction_time)
            self.app.play_sound('success')
            
            current_count = len(self.trials)
            self.info_label.text = f'{current_count}회차 반응속도: {reaction_time}ms!'
            
            if current_count < 3:
                self.state = 'ready'
                self.action_btn.text = f'다음 라운드 ({current_count}/3)'
                self.action_btn.background_color = self.app.secondary_color
            else:
                # 3회 측정 완료 -> 평균 계산 및 랭킹 저장
                avg_score = int(sum(self.trials) / 3)
                self.app.add_ranking("reaction_speed", self.app.player_name, avg_score)
                self.info_label.text = f'🎉 완료! 3회 평균 반응속도: {avg_score}ms!'
                self.state = 'done'
                self.action_btn.text = '모든 도전 완료 (기록 등록)'
                self.action_btn.background_color = self.app.primary_color
                self.action_btn.disabled = True

    def turn_green(self, *a):
        self.state = 'green'
        self.green_time = time.time()
        self.action_btn.text = '⚡ 지금 누르세요!!'
        self.action_btn.background_color = self.app.primary_color

    def go_back(self, *a):
        if self.scheduled_event:
            self.scheduled_event.cancel()
        self.app.play_sound('click')
        self.action_btn.disabled = False
        self.manager.current = 'menu'