# screens/login_screen.py 전체 코드
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.app import App

FONT = 'NanumGothic'

class LoginScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.app = App.get_running_app()
        
        with self.canvas.before:
            Color(*self.app.bg_color)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        layout = BoxLayout(orientation='vertical', padding=40, spacing=15)
        
        layout.add_widget(Label(
            text='미니게임 파라다이스', font_size=34, font_name=FONT,
            bold=True, color=self.app.primary_color, size_hint_y=0.2
        ))
        
        # 아이디 입력창
        layout.add_widget(Label(text='아이디 (ID)', font_size=16, font_name=FONT, color=self.app.text_dark, size_hint_y=0.08))
        self.id_input = TextInput(
            text='', font_size=18, font_name=FONT, multiline=False, size_hint_y=0.1,
            halign='center', background_color=(1, 1, 1, 1), foreground_color=self.app.text_dark
        )
        layout.add_widget(self.id_input)
        
        # 비밀번호 입력창
        layout.add_widget(Label(text='비밀번호 (PASSWORD)', font_size=16, font_name=FONT, color=self.app.text_dark, size_hint_y=0.08))
        self.pw_input = TextInput(
            text='', font_size=18, font_name=FONT, multiline=False, size_hint_y=0.1,
            password=True, halign='center', background_color=(1, 1, 1, 1), foreground_color=self.app.text_dark
        )
        layout.add_widget(self.pw_input)
        
        layout.add_widget(BoxLayout(size_hint_y=0.05)) # 여백
        
        # 로그인 버튼
        login_btn = Button(
            text='로그인 및 정보 저장', font_size=20, font_name=FONT, bold=True,
            size_hint_y=0.15, background_color=self.app.secondary_color,
            background_normal='', color=(1, 1, 1, 1)
        )
        login_btn.bind(on_press=self.perform_login)
        layout.add_widget(login_btn)
        
        self.add_widget(layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def perform_login(self, instance):
        username = self.id_input.text.strip()
        password = self.pw_input.text.strip()
        
        if not username or not password:
            self.app.play_sound('fail')
            return
            
        # 로그인 정보 파일로 로컬 저장 가동
        self.app.player_name = username
        self.app.save_account(username, password)
        
        self.app.play_sound('success')
        self.manager.current = 'menu'