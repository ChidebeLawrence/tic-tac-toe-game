from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.graphics import Color, RoundedRectangle

import random, math, os

# ---------- COLORS ----------
BG = (0.08, 0.08, 0.1, 1)
CARD = (0.12, 0.12, 0.15, 1)
ACCENT = (0, 0.8, 0.8, 1)
WIN = (0, 1, 0.5, 1)

# ---------- GLOBALS ----------
player = "X"
ai = "O"
board = [" "] * 9

player_score = 0
ai_score = 0
draws = 0

difficulty = "Hard"
starting_player = "player"

SCORE_FILE = "scores.txt"

# ---------- SCORE ----------
def load_scores():
    global player_score, ai_score, draws
    if os.path.exists(SCORE_FILE):
        with open(SCORE_FILE, "r") as f:
            data = f.read().split(",")
            if len(data) == 3:
                player_score, ai_score, draws = map(int, data)

def save_scores():
    with open(SCORE_FILE, "w") as f:
        f.write(f"{player_score},{ai_score},{draws}")

# ---------- LOGIC ----------
def check_winner(b, p):
    combos = [
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8],
        [0,4,8],[2,4,6]
    ]
    for c in combos:
        if all(b[i] == p for i in c):
            return c
    return None

def is_draw(b):
    return " " not in b

def minimax(b, is_max):
    if check_winner(b, ai): return 1
    if check_winner(b, player): return -1
    if is_draw(b): return 0

    if is_max:
        best = -math.inf
        for i in range(9):
            if b[i] == " ":
                b[i] = ai
                best = max(best, minimax(b, False))
                b[i] = " "
        return best
    else:
        best = math.inf
        for i in range(9):
            if b[i] == " ":
                b[i] = player
                best = min(best, minimax(b, True))
                b[i] = " "
        return best

def ai_move():
    empty = [i for i in range(9) if board[i] == " "]

    if difficulty == "Easy":
        move = random.choice(empty)
    elif difficulty == "Medium" and random.random() < 0.5:
        move = random.choice(empty)
    else:
        best, move = -math.inf, None
        for i in empty:
            board[i] = ai
            score = minimax(board, False)
            board[i] = " "
            if score > best:
                best, move = score, i

    board[move] = ai
    return move

# ---------- UI ----------
def card(widget, color=CARD):
    with widget.canvas.before:
        Color(*color)
        widget.rect = RoundedRectangle(radius=[20], pos=widget.pos, size=widget.size)
    widget.bind(pos=lambda w, v: setattr(w.rect, "pos", v))
    widget.bind(size=lambda w, v: setattr(w.rect, "size", v))

# ---------- HOME ----------
class Home(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

        layout = BoxLayout(orientation="vertical", padding=25, spacing=20)
        card(layout, BG)

        self.score = Label(text="", font_size=16)
        layout.add_widget(Label(text="TIC-TAC-TOE", font_size=32, color=ACCENT))
        layout.add_widget(self.score)

        layout.add_widget(Button(text="Start Game", size_hint_y=None, height=50,
                                 on_press=lambda x: setattr(self.manager, "current", "level")))
        layout.add_widget(Button(text="Reset Scores", size_hint_y=None, height=50,
                                 on_press=self.reset))
        layout.add_widget(Button(text="Exit", size_hint_y=None, height=50,
                                 on_press=lambda x: App.get_running_app().stop()))

        self.add_widget(layout)

    def on_enter(self):
        self.score.text = f"You: {player_score}  AI: {ai_score}  Draws: {draws}"

    def reset(self, x):
        global player_score, ai_score, draws
        player_score = ai_score = draws = 0
        save_scores()
        self.on_enter()

# ---------- LEVEL ----------
class Level(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

        layout = BoxLayout(orientation="vertical", padding=25, spacing=15)
        card(layout, BG)

        layout.add_widget(Label(text="Select Difficulty", font_size=20, color=ACCENT))

        for lvl in ["Easy", "Medium", "Hard"]:
            layout.add_widget(Button(text=lvl, size_hint_y=None, height=50,
                                     on_press=lambda x, l=lvl: self.set(l)))

        layout.add_widget(Button(text="Back", size_hint_y=None, height=50,
                                 on_press=lambda x: setattr(self.manager, "current", "home")))

        self.add_widget(layout)

    def set(self, lvl):
        global difficulty, starting_player
        difficulty = lvl
        starting_player = "player"
        self.manager.get_screen("game").reset_board()
        self.manager.current = "game"

# ---------- GAME ----------
class Game(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

        main = BoxLayout(orientation="vertical", padding=15, spacing=10)
        card(main, BG)

        # TOP PANEL
        self.result_text = Label(text="", font_size=18, color=ACCENT)
        self.score_text = Label(text="", font_size=14)

        self.next_btn = Button(text="Next Round", size_hint_y=None, height=40)
        self.home_btn = Button(text="Home", size_hint_y=None, height=40)

        self.next_btn.bind(on_press=lambda x: self.next_round())
        self.home_btn.bind(on_press=lambda x: self.go_home())

        # Hide initially
        self.next_btn.opacity = 0
        self.next_btn.disabled = True
        self.home_btn.opacity = 0
        self.home_btn.disabled = True

        top_panel = BoxLayout(orientation="vertical", size_hint_y=0.5, height=80, spacing=5)
        top_panel.add_widget(self.result_text)
        top_panel.add_widget(self.score_text)

        btn_row = BoxLayout(size_hint_y=None, height=40, spacing=10)
        btn_row.add_widget(self.next_btn)
        btn_row.add_widget(self.home_btn)

        top_panel.add_widget(btn_row)
        main.add_widget(top_panel)

        # STATUS
        self.status = Label(text="Your Turn", font_size=18)
        main.add_widget(self.status)

        # GRID
        self.grid = GridLayout(cols=3, spacing=10, size_hint=(1, 1.5))
        self.buttons = []

        for i in range(9):
            btn = Button(font_size=36,
                         background_normal="",
                         background_color=CARD)
            btn.bind(on_press=lambda x, i=i: self.move(i))
            self.buttons.append(btn)
            self.grid.add_widget(btn)

        main.add_widget(self.grid)

        self.add_widget(main)

    def reset_board(self):
        global board
        board = [" "] * 9

        for b in self.buttons:
            b.text = ""
            b.background_color = CARD
            b.disabled = False

        self.status.text = "Your Turn"
        self.result_text.text = ""
        self.score_text.text = ""

        # Hide buttons again
        self.next_btn.opacity = 0
        self.next_btn.disabled = True
        self.home_btn.opacity = 0
        self.home_btn.disabled = True

    def move(self, i):
        if board[i] != " ":
            return

        board[i] = player
        self.buttons[i].text = player

        combo = check_winner(board, player)
        if combo:
            self.highlight(combo)
            self.end("You Won 😏", "player")
            return

        if is_draw(board):
            self.end("Draw 🤝", "draw")
            return

        self.disable()
        self.status.text = "AI thinking..."
        Clock.schedule_once(self.ai_turn, 0.5)

    def ai_turn(self, dt):
        move = ai_move()
        self.buttons[move].text = ai

        combo = check_winner(board, ai)
        if combo:
            self.highlight(combo)
            self.end("AI Won 🤖", "ai")
            return

        if is_draw(board):
            self.end("Draw 🤝", "draw")
            return

        self.status.text = "Your Turn"
        self.enable()

    def end(self, text, result):
        global player_score, ai_score, draws

        self.disable()

        if result == "player":
            player_score += 1
        elif result == "ai":
            ai_score += 1
        else:
            draws += 1

        save_scores()

        self.result_text.text = text
        self.score_text.text = f"You: {player_score}  AI: {ai_score}  Draws: {draws}"

        # Show buttons
        self.next_btn.opacity = 1
        self.next_btn.disabled = False
        self.home_btn.opacity = 1
        self.home_btn.disabled = False

    def next_round(self):
        global starting_player

        starting_player = "ai" if starting_player == "player" else "player"
        self.reset_board()

        if starting_player == "ai":
            self.disable()
            self.status.text = "AI thinking..."
            Clock.schedule_once(self.ai_turn, 0.5)

    def go_home(self):
        self.manager.current = "home"

    def highlight(self, combo):
        for i in combo:
            self.buttons[i].background_color = WIN

    def disable(self):
        for b in self.buttons:
            b.disabled = True

    def enable(self):
        for i, b in enumerate(self.buttons):
            if board[i] == " ":
                b.disabled = False

# ---------- APP ----------
class TicTacToeApp(App):
    def build(self):
        load_scores()

        sm = ScreenManager()
        sm.add_widget(Home(name="home"))
        sm.add_widget(Level(name="level"))
        sm.add_widget(Game(name="game"))

        return sm

TicTacToeApp().run()