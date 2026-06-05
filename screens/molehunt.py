# screens/molehunt.py 전체 코드
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.app import App
import random

FONT = 'NanumGothic'

class MoleHuntScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.score = 0
        self.time_left = 20
        self.mole_index = -1
        self.app = App.get_running_app()
        self.game_event = None
        self.time_event = None
        
        with self.canvas.before:
            Color(*self.app.bg_color)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # 상단 정보창
        self.info_label = Label(
            text='제한시간: 20초 | 점수: 0점', font_size=20, font_name=FONT, 
            size_hint_y=0.15, color=self.app.text_dark
        )
        layout.add_widget(self.info_label)
        
        # 3x3 격자판
        self.grid = GridLayout(cols=3, spacing=10, size_hint_y=0.65)
        self.buttons = []
        for i in range(9):
            btn = Button(
                text='흙', font_size=24, font_name=FONT,
                background_color=(0.6, 0.4, 0.2, 1), background_normal=''
            )
            btn.bind(on_press=lambda x, idx=i: self.whack(idx))
            self.grid.add_widget(btn)
            self.buttons.append(btn)
        layout.add_widget(self.grid)
        
        # 하단 제어 버튼
        self.back_btn = Button(
            text='메뉴로', font_size=16, font_name=FONT, size_hint_y=0.2,
            background_color=(0.5, 0.5, 0.5, 1), background_normal=''
        )
        self.back_btn.bind(on_press=self.go_back)
        layout.add_widget(self.back_btn)
        
        self.add_widget(layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def on_enter(self):
        self.score = 0
        self.time_left = 20
        self.mole_index = -1
        self.info_label.text = f'제한시간: {self.time_left}초 | 점수: {self.score}점'
        self.info_label.color = self.app.text_dark
        
        for btn in self.buttons:
            btn.text = '흙'
            btn.background_color = (0.6, 0.4, 0.2, 1)
            btn.disabled = False
            
        self.game_event = Clock.schedule_interval(self.spawn_mole, 0.8)
        self.time_event = Clock.schedule_interval(self.update_timer, 1.0)

    def spawn_mole(self, dt):
        for btn in self.buttons:
            btn.text = '흙'
            btn.background_color = (0.6, 0.4, 0.2, 1)
            
        self.mole_index = random.randint(0, 8)
        self.buttons[self.mole_index].text = '🐹 두더지'
        self.buttons[self.mole_index].background_color = self.app.primary_color

    def whack(self, idx):
        if idx == self.mole_index:
            self.score += 1
            self.app.play_sound('success')
            self.buttons[idx].text = '💥 히트!'
            self.buttons[idx].background_color = self.app.accent_color
            self.mole_index = -1
            self.info_label.text = f'제한시간: {self.time_left}초 | 점수: {self.score}점'

    def update_timer(self, dt):
        self.time_left -= 1
        if self.time_left <= 0:
            self.end_game()
        else:
            self.info_label.text = f'제한시간: {self.time_left}초 | 점수: {self.score}점'

    def end_game(self):
        if self.game_event: self.game_event.cancel()
        if self.time_event: self.time_event.cancel()
        
        self.app.play_sound('success')
        self.app.add_ranking("molehunt", self.app.player_name, self.score)
        self.info_label.text = f'🎉 게임 완료! 최종 점수: {self.score}점 (랭킹 등록)'
        self.info_label.color = self.app.primary_color
        
        for btn in self.buttons:
            btn.disabled = True

    def go_back(self, *a):
        if self.game_event: self.game_event.cancel()
        if self.time_event: self.time_event.cancel()
        self.app.play_sound('click')
        self.manager.current = 'menu'