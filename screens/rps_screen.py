# screens/rps_screen.py 전체 코드
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.app import App
import random

FONT = 'NanumGothic'

class RPSScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.wins = 0
        self.rounds = 0
        self.app = App.get_running_app()
        
        # 배경색 설정 (밝은 톤)
        with self.canvas.before:
            Color(*self.app.bg_color)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        layout = BoxLayout(orientation='vertical', padding=30, spacing=15)
        
        self.info_label = Label(
            text='가위바위보! (5판 진행)', font_size=26, font_name=FONT, 
            size_hint_y=0.15, color=self.app.text_dark
        )
        
        # 큰 이모지가 들어갈 메인 디스플레이 공간
        self.vs_label = Label(
            text='🎮\nREADY', font_size=55, font_name=FONT,
            size_hint_y=0.35, halign='center', color=self.app.secondary_color
        )
        
        self.result_label = Label(
            text='아래 버튼을 선택하세요.', font_size=22, font_name=FONT, 
            size_hint_y=0.15, color=self.app.text_dark
        )
        
        btn_layout = BoxLayout(spacing=15, size_hint_y=0.2)
        emoji_map = {'가위': '✌️ 가위', '바위': '✊ 바위', '보': '🖐️ 보'}
        for choice in ['가위', '바위', '보']:
            btn = Button(
                text=emoji_map[choice], font_size=20, font_name=FONT,
                background_color=self.app.secondary_color, background_normal=''
            )
            btn.bind(on_press=lambda x, c=choice: self.play(c))
            btn_layout.add_widget(btn)
            
        self.back_btn = Button(
            text='메뉴로 나가지', font_size=18, font_name=FONT,
            size_hint_y=0.1, background_color=(0.5, 0.5, 0.5, 1), background_normal=''
        )
        self.back_btn.bind(on_press=self.go_back)
        
        layout.add_widget(self.info_label)
        layout.add_widget(self.vs_label)
        layout.add_widget(self.result_label)
        layout.add_widget(btn_layout)
        layout.add_widget(self.back_btn)
        self.add_widget(layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def on_enter(self):
        self.wins = 0
        self.rounds = 0
        self.info_label.text = '가위바위보! (5판 진행)'
        self.vs_label.text = '🎮\nREADY'
        self.vs_label.color = self.app.secondary_color
        self.result_label.text = '아래 버튼을 선택하세요.'
        self.result_label.color = self.app.text_dark

    def play(self, player_choice):
        if self.rounds >= 5:
            return
            
        choices = ['가위', '바위', '보']
        computer = random.choice(choices)
        
        emoji_symbols = {'가위': '✌️', '바위': '✊', '보': '🖐️'}
        p_symbol = emoji_symbols[player_choice]
        c_symbol = emoji_symbols[computer]
        
        if player_choice == computer:
            result = '무승부!'
            self.vs_label.color = (0.5, 0.5, 0.5, 1)
            self.app.play_sound('click')
        elif (player_choice == '가위' and computer == '보') or \
             (player_choice == '바위' and computer == '가위') or \
             (player_choice == '보' and computer == '바위'):
            result = '승리!'
            self.wins += 1
            self.vs_label.color = self.app.primary_color
            self.app.play_sound('success')
        else:
            result = '패배!'
            self.vs_label.color = self.app.accent_color
            self.app.play_sound('fail')
            
        self.rounds += 1
        self.vs_label.text = f'{p_symbol}  VS  {c_symbol}'
        self.result_label.text = f'{player_choice} 내셨고, 컴퓨터는 {computer}! -> {result}'
        self.info_label.text = f'{self.rounds}/5판  |  현재 승리: {self.wins}회'
        
        if self.rounds >= 5:
            self.app.add_ranking("rps", self.app.player_name, self.wins)
            self.result_label.text = f'🎉 게임 완료! 최종 성적: 5판 중 {self.wins}승!'
            self.result_label.color = self.app.primary_color
            self.app.play_sound('success')

    def go_back(self, *a):
        self.app.play_sound('click')
        self.manager.current = 'menu'