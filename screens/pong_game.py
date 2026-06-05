# screens/pong_game.py 전체 코드
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.app import App
import random

FONT = 'NanumGothic'

class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

class PongPaddle(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            ball.velocity = vel.x, vel.y + offset
            return True
        return False

class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)

    def __init__(self, screen, **kwargs):
        super().__init__(**kwargs)
        self.screen = screen
        self.app = App.get_running_app()
        
    def serve_ball(self, vel=(4, 0)):
        self.ball.center = self.center
        self.ball.velocity = vel

    def update(self, dt):
        self.ball.move()

        # 패들 바운스 판정
        if self.player1.bounce_ball(self.ball) or self.player2.bounce_ball(self.ball):
            self.app.play_sound('click')

        # 벽 튕기기 판정 (상하)
        if (self.ball.y < self.y) or (self.ball.top > self.top):
            self.ball.velocity_y *= -1
            self.app.play_sound('click')

        # AI 패들 자동 조작
        if self.ball.center_y > self.player2.center_y:
            self.player2.y += 3
        else:
            self.player2.y -= 3

        # 득점 판정
        if self.ball.x < self.x:
            self.player2.score += 1
            self.app.play_sound('fail')
            self.screen.end_game_session(self.player1.score)
        if self.ball.x > self.width:
            self.player1.score += 1
            self.app.play_sound('success')
            self.serve_ball(vel=(-4, random.randint(-2, 2)))
            self.screen.update_score_label(self.player1.score)

    def on_touch_move(self, touch):
        if touch.x < self.width / 3:
            self.player1.center_y = touch.y

class PongScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.app = App.get_running_app()
        self.game_event = None
        
        with self.canvas.before:
            Color(*self.app.bg_color)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        self.main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        self.score_label = Label(text='내 점수: 0점 (화면 왼쪽을 위아래로 드래그하세요!)', font_size=18, font_name=FONT, size_hint_y=0.1, color=self.app.text_dark)
        self.main_layout.add_widget(self.score_label)
        
        # 게임 컨테이너 및 게임판 객체 생성
        self.game_container = BoxLayout(size_hint_y=0.8)
        self.game = PongGame(self)
        
        with self.game.canvas.before:
            Color(0.1, 0.1, 0.15, 1) # 미니 오락실 브라운관 느낌의 딥 블랙 세팅
            self.bg_rect = Rectangle(size=self.game.size, pos=self.game.pos)
        self.game.bind(size=self._update_game_bg, pos=self._update_game_bg)
        
        # [수정 핵심 포인트] 오류가 나던 동적 바인딩 람다식을 지우고, 
        # Kivy Graphic Instructions 객체를 인스턴스 변수로 직접 잡아 속성을 제어합니다.
        self.game.ball = PongBall(size=(20, 20))
        with self.game.ball.canvas:
            Color(1, 0.8, 0, 1) # 노란색 공
            self.ball_rect = Rectangle(size=self.game.ball.size, pos=self.game.ball.pos)
        self.game.ball.bind(pos=self._sync_ball)
        
        self.game.player1 = PongPaddle(size=(20, 100))
        with self.game.player1.canvas:
            Color(0.2, 0.6, 1, 1) # 파란색 플레이어
            self.p1_rect = Rectangle(size=self.game.player1.size, pos=self.game.player1.pos)
        self.game.player1.bind(pos=self._sync_p1)
        
        self.game.player2 = PongPaddle(size=(20, 100))
        with self.game.player2.canvas:
            Color(1, 0.3, 0.3, 1) # 빨간색 AI 컴퓨터
            self.p2_rect = Rectangle(size=self.game.player2.size, pos=self.game.player2.pos)
        self.game.player2.bind(pos=self._sync_p2)
        
        self.game.add_widget(self.game.ball)
        self.game.add_widget(self.game.player1)
        self.game.add_widget(self.game.player2)
        
        self.game_container.add_widget(self.game)
        self.main_layout.add_widget(self.game_container)
        
        self.back_btn = Button(text='메뉴로 탈출', font_size=16, font_name=FONT, size_hint_y=0.1, background_color=(0.5, 0.5, 0.5, 1), background_normal='')
        self.back_btn.bind(on_press=self.go_back)
        self.main_layout.add_widget(self.back_btn)
        
        self.add_widget(self.main_layout)

    # 위치 동기화 안전 패치 함수들
    def _sync_ball(self, instance, value):
        self.ball_rect.pos = value

    def _sync_p1(self, instance, value):
        self.p1_rect.pos = value

    def _sync_p2(self, instance, value):
        self.p2_rect.pos = value

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def _update_game_bg(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size
        # 사이즈 동기화 시 초기 위치 리셋
        self.game.player1.x = instance.x + 10
        self.game.player1.center_y = instance.center_y
        self.game.player2.x = instance.right - 30
        self.game.player2.center_y = instance.center_y
        self.game.ball.center = instance.center

    def on_enter(self):
        self.game.player1.score = 0
        self.game.player2.score = 0
        self.score_label.text = '내 점수: 0점 (화면 왼쪽을 위아래로 드래그하세요!)'
        self.game.serve_ball()
        self.game_event = Clock.schedule_interval(self.game.update, 1.0 / 60.0)

    def update_score_label(self, score):
        self.score_label.text = f'🔥 대박 연속 득점 중! 현재: {score}점'

    def end_game_session(self, final_score):
        if self.game_event: Clock.unschedule(self.game_event)
        self.app.add_ranking("pong", self.app.player_name, final_score)
        self.score_label.text = f'❌ 패배! 최종 스코어: {final_score}점 (랭킹 저장 완료)'

    def go_back(self, *a):
        if self.game_event: Clock.unschedule(self.game_event)
        self.app.play_sound('click')
        self.manager.current = 'menu'