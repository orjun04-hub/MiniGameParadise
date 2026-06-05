# screens/menu_screen.py 전체 코드
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.app import App

FONT = 'NanumGothic'

class MenuScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.app = App.get_running_app()
        
        with self.canvas.before:
            Color(*self.app.bg_color)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        layout = BoxLayout(orientation='vertical', padding=15, spacing=8)
        
        layout.add_widget(Label(
            text='🎮 오락실 미니게임 패키지 7-in-1 🎮', font_size=24, font_name=FONT, bold=True,
            color=self.app.text_dark, size_hint_y=0.12
        ))
        
        games = [
            ('숫자 기억 게임', 'number_memory', self.app.primary_color),
            ('반응속도 테스트', 'reaction_speed', self.app.secondary_color),
            ('가위바위보 테스트', 'rps', (0.6, 0.4, 0.8, 1)),
            ('🎨 색상 타이밍 맞추기', 'color_match', (0.9, 0.5, 0.2, 1)),
            ('🧮 빠른 연산 스피드왕', 'quick_math', (0.1, 0.7, 0.7, 1)),
            ('🏓 오락실 클래식 퐁(Pong)', 'pong', (0.9, 0.4, 0.4, 1)),
            ('🚀 스페이스 운석 피하기', 'space_dodger', (0.7, 0.5, 0.3, 1)),
            ('🏆 실시간 통합 랭킹판', 'ranking', (0.7, 0.7, 0.2, 1))
        ]
        
        for text, screen_name, btn_color in games:
            btn = Button(
                text=text, font_size=16, font_name=FONT, bold=True,
                background_color=btn_color, background_normal='',
                color=(1, 1, 1, 1)
            )
            btn.bind(on_press=lambda x, sn=screen_name: self.change_screen(sn))
            layout.add_widget(btn)
            
        self.add_widget(layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def change_screen(self, screen_name):
        self.app.play_sound('click')
        self.manager.current = screen_name