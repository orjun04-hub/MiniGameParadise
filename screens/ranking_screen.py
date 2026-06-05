# screens/ranking_screen.py 전체 코드
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.app import App

FONT = 'NanumGothic'

class RankingScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.app = App.get_running_app()
        
        with self.canvas.before:
            Color(*self.app.bg_color)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        self.layout = BoxLayout(orientation='vertical', padding=15, spacing=3)
        self.add_widget(self.layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def on_enter(self):
        self.layout.clear_widgets()
        
        self.layout.add_widget(Label(
            text='🏆 명예의 전당 (종합 실시간 랭킹) 🏆', font_size=20, font_name=FONT, bold=True,
            size_hint_y=0.08, color=self.app.text_dark
        ))
        
        rankings = self.app.load_rankings()
        
        games = [
            ('숫자 기억', 'number_memory', '레벨'),
            ('반응속도', 'reaction_speed', 'ms'),
            ('가위바위보', 'rps', '승'),
            ('색상 맞추기', 'color_match', '점'),
            ('빠른 연산', 'quick_math', '점'),
            ('클래식 퐁', 'pong', '점'),
            ('운석 피하기', 'space_dodger', '점')
        ]
        medals = ['🥇', '🥈', '🥉']
        
        for title, key, unit in games:
            data = rankings.get(key, [])
            score_str = "기록 없음"
            if data and len(data) > 0:
                score_str = f"{medals[0]} {data[0]['name']}: {data[0]['score']}{unit}"
                
            self.layout.add_widget(Label(
                text=f'• {title} ➡️ {score_str}', font_size=14, font_name=FONT, 
                size_hint_y=0.05, color=self.app.text_dark, halign='left'
            ))
                
        self.layout.add_widget(BoxLayout(size_hint_y=0.03))
        back = Button(
            text='메뉴로 돌아가기', font_size=16, font_name=FONT, bold=True,
            size_hint_y=0.08, background_color=(0.5, 0.5, 0.5, 1), background_normal=''
        )
        back.bind(on_press=lambda x: self.go_back())
        self.layout.add_widget(back)

    def go_back(self):
        self.app.play_sound('click')
        self.manager.current = 'menu'