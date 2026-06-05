# main.py 전체 코드
import os
import json
import threading

os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'
os.environ['KIVY_IMAGE'] = 'sdl2'

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.text import LabelBase
from kivy.utils import get_color_from_hex

LabelBase.register(name='NanumGothic', fn_regular='fonts/NanumGothic-Bold.ttf')

from screens.login_screen import LoginScreen
from screens.menu_screen import MenuScreen
from screens.number_memory import NumberMemoryScreen
from screens.reaction_speed import ReactionSpeedScreen
from screens.rps_screen import RPSScreen
from screens.ranking_screen import RankingScreen
from screens.color_match import ColorMatchScreen
from screens.quick_math import QuickMathScreen
from screens.pong_game import PongScreen
from screens.space_dodger import SpaceDodgerScreen

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
os.makedirs(DATA_DIR, exist_ok=True)

class MiniGameApp(App):
    player_name = 'Player'
    data_dir = DATA_DIR

    bg_color = get_color_from_hex('#F4F6F9')
    primary_color = get_color_from_hex('#2ECC71')
    secondary_color = get_color_from_hex('#3498DB')
    accent_color = get_color_from_hex('#E74C3C')
    text_dark = get_color_from_hex('#2C3E50')

    def build(self):
        self.title = '미니게임 파라다이스 종합 7-in-1'
        self.account_info = self.load_account()
        if self.account_info:
            self.player_name = self.account_info.get('username', 'Player')

        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(NumberMemoryScreen(name='number_memory'))
        sm.add_widget(ReactionSpeedScreen(name='reaction_speed'))
        sm.add_widget(RPSScreen(name='rps'))
        sm.add_widget(RankingScreen(name='ranking'))
        sm.add_widget(ColorMatchScreen(name='color_match'))
        sm.add_widget(QuickMathScreen(name='quick_math'))
        sm.add_widget(PongScreen(name='pong'))
        sm.add_widget(SpaceDodgerScreen(name='space_dodger'))
        
        # 자동 진입을 막고 무조건 login 화면이 먼저 뜨도록 강제 지정!
        sm.current = 'login' 
        return sm

    def play_sound(self, sound_type):
        pass

    def get_account_file(self): return os.path.join(self.data_dir, 'account.json')
    def load_account(self):
        f = self.get_account_file()
        if os.path.exists(f):
            try:
                with open(f, 'r', encoding='utf-8') as fp: return json.load(fp)
            except Exception: pass
        return None
    def save_account(self, username, password):
        with open(self.get_account_file(), 'w', encoding='utf-8') as fp:
            json.dump({"username": username, "password": password}, fp, ensure_ascii=False, indent=2)

    def get_ranking_file(self): return os.path.join(self.data_dir, 'ranking.json')
    def load_rankings(self):
        f = self.get_ranking_file()
        if os.path.exists(f):
            try:
                with open(f, 'r', encoding='utf-8') as fp: return json.load(fp)
            except Exception: pass
        return {"number_memory": [], "reaction_speed": [], "rps": [], "color_match": [], "quick_math": [], "pong": [], "space_dodger": []}

    def save_rankings(self, data):
        with open(self.get_ranking_file(), 'w', encoding='utf-8') as fp:
            json.dump(data, fp, ensure_ascii=False, indent=2)

    def add_ranking(self, game, name, score):
        r = self.load_rankings()
        if game not in r: r[game] = []
        r[game].append({"name": name, "score": score})
        if game == "reaction_speed": r[game].sort(key=lambda x: x["score"])
        else: r[game].sort(key=lambda x: x["score"], reverse=True)
        r[game] = r[game][:3]
        self.save_rankings(r)

if __name__ == '__main__':
    MiniGameApp().run()