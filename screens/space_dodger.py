# screens/space_dodger.py 전체 코드
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Ellipse
from kivy.clock import Clock
from kivy.app import App
import random

FONT = 'NanumGothic'

class SpaceDodgerScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.score = 0
        self.ship_x = 200
        self.asteroids = [] # 각 운석은 [x, y, size, speed] 배열 구조
        self.app = App.get_running_app()
        self.game_event = None
        
        with self.canvas.before:
            Color(*self.app.bg_color)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        self.info_label = Label(text='버튼을 눌러 운석을 피하세요! 생존 점수: 0점', font_size=18, font_name=FONT, size_hint_y=0.1, color=self.app.text_dark)
        layout.add_widget(self.info_label)
        
        # 게임 캔버스 보드 영역
        self.canvas_widget = Widget(size_hint_y=0.7)
        with self.canvas_widget.canvas.before:
            Color(0.05, 0.05, 0.1, 1) # 깊은 우주 공간 밤하늘 테마
            self.canvas_rect = Rectangle(size=self.canvas_widget.size, pos=self.canvas_widget.pos)
        self.canvas_widget.bind(size=self._update_canvas_rect, pos=self._update_canvas_rect)
        layout.add_widget(self.canvas_widget)
        
        # 좌우 이동 컨트롤러 패널
        ctrl_layout = BoxLayout(spacing=20, size_hint_y=0.12)
        btn_left = Button(text='◀ 좌측 이동', font_size=18, font_name=FONT, bold=True, background_color=self.app.secondary_color, background_normal='')
        btn_left.bind(on_press=lambda x: self.move_ship(-35))
        
        btn_right = Button(text='우측 이동 ▶', font_size=18, font_name=FONT, bold=True, background_color=self.app.secondary_color, background_normal='')
        btn_right.bind(on_press=lambda x: self.move_ship(35))
        
        ctrl_layout.add_widget(btn_left)
        ctrl_layout.add_widget(btn_right)
        layout.add_widget(ctrl_layout)
        
        self.back_btn = Button(text='메뉴로', font_size=16, font_name=FONT, size_hint_y=0.08, background_color=(0.5, 0.5, 0.5, 1), background_normal='')
        self.back_btn.bind(on_press=self.go_back)
        layout.add_widget(self.back_btn)
        
        self.add_widget(layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def _update_canvas_rect(self, instance, value):
        self.canvas_rect.pos = instance.pos
        self.canvas_rect.size = instance.size

    def on_enter(self):
        self.score = 0
        self.ship_x = self.canvas_widget.center_x
        self.asteroids = []
        # 초기 기본 운석 4개 생성
        for _ in range(4):
            self.asteroids.append([random.randint(int(self.canvas_widget.x), int(self.canvas_widget.right - 30)), random.randint(400, 600), random.randint(25, 45), random.randint(3, 7)])
        
        self.info_label.text = '생존 점수: 0점'
        self.info_label.color = self.app.text_dark
        self.game_event = Clock.schedule_interval(self.update_game, 1.0 / 40.0)

    def move_ship(self, offset):
        self.app.play_sound('click')
        self.ship_x += offset
        # 화면 탈출 방지 경계 제한
        if self.ship_x < self.canvas_widget.x: self.ship_x = self.canvas_widget.x
        if self.ship_x > self.canvas_widget.right - 30: self.ship_x = self.canvas_widget.right - 30

    def update_game(self, dt):
        self.score += 1
        self.info_label.text = f'🚀 요리조리 회피 중! 생존 스코어: {self.score}점'
        
        # 캔버스 갱신 드로잉
        self.canvas_widget.canvas.clear()
        with self.canvas_widget.canvas:
            # 내 우주선 그리기 (초록 형광색 타원 사각형 조합)
            Color(0, 1, 0.5, 1)
            Rectangle(pos=(self.ship_x, self.canvas_widget.y + 10), size=(30, 40))
            
            # 떨어지는 운석들 루프 처리
            Color(1, 0.4, 0.1, 1)
            for ast in self.asteroids:
                ast[1] -= ast[3] # Y값 감소시켜 하강
                Ellipse(pos=(ast[0], ast[1]), size=(ast[2], ast[2]))
                
                # 화면 아래로 떨어지면 위에서 재생성하며 점수 추가 보너스
                if ast[1] < self.canvas_widget.y:
                    ast[0] = random.randint(int(self.canvas_widget.x), int(self.canvas_widget.right - 30))
                    ast[1] = self.canvas_widget.top - 40
                    ast[3] = random.randint(4, 9)
                    self.score += 10
                    
                # 💥 충돌 감지 박스 처리 (우주선 크기 30x40 감안)
                if (ast[0] < self.ship_x + 30 and ast[0] + ast[2] > self.ship_x) and \
                   (ast[1] < self.canvas_widget.y + 50 and ast[1] + ast[2] > self.canvas_widget.y + 10):
                    self.end_game()
                    return

    def end_game(self):
        if self.game_event: Clock.unschedule(self.game_event)
        self.app.play_sound('fail')
        self.app.add_ranking("space_dodger", self.app.player_name, self.score)
        self.info_label.text = f'💥 충돌 발생! 게임 종료. 최종 점수: {self.score}점'
        self.info_label.color = self.app.accent_color

    def go_back(self, *a):
        if self.game_event: Clock.unschedule(self.game_event)
        self.app.play_sound('click')
        self.manager.current = 'menu'