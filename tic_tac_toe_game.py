# from kivy.app import App
# from kivy.uix.gridlayout import GridLayout
# from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.button import Button
# from kivy.uix.label import Label
# from kivy.uix.screenmanager import ScreenManager, Screen
# from kivy.clock import Clock
# from kivy.graphics import Color, RoundedRectangle
#
# import random, math, os
#
# # ---------- COLORS ----------
# BG = (0.08, 0.08, 0.1, 1)
# CARD = (0.12, 0.12, 0.15, 1)
# ACCENT = (0, 0.8, 0.8, 1)
# WIN = (0, 1, 0.5, 1)
#
# # ---------- GLOBALS ----------
# player = "X"
# ai = "O"
# board = [" "] * 9
#
# player_score = 0
# ai_score = 0
# draws = 0
#
# difficulty = "Hard"
# starting_player = "player"
#
# SCORE_FILE = "here/scores.txt"
#
# # ---------- SCORE ----------
# def load_scores():
#     global player_score, ai_score, draws
#     if os.path.exists(SCORE_FILE):
#         with open(SCORE_FILE, "r") as f:
#             data = f.read().split(",")
#             if len(data) == 3:
#                 player_score, ai_score, draws = map(int, data)
#
# def save_scores():
#     with open(SCORE_FILE, "w") as f:
#         f.write(f"{player_score},{ai_score},{draws}")
#
# # ---------- LOGIC ----------
# def check_winner(b, p):
#     combos = [
#         [0,1,2],[3,4,5],[6,7,8],
#         [0,3,6],[1,4,7],[2,5,8],
#         [0,4,8],[2,4,6]
#     ]
#     for c in combos:
#         if all(b[i] == p for i in c):
#             return c
#     return None
#
# def is_draw(b):
#     return " " not in b
#
# def minimax(b, is_max):
#     if check_winner(b, ai): return 1
#     if check_winner(b, player): return -1
#     if is_draw(b): return 0
#
#     if is_max:
#         best = -math.inf
#         for i in range(9):
#             if b[i] == " ":
#                 b[i] = ai
#                 best = max(best, minimax(b, False))
#                 b[i] = " "
#         return best
#     else:
#         best = math.inf
#         for i in range(9):
#             if b[i] == " ":
#                 b[i] = player
#                 best = min(best, minimax(b, True))
#                 b[i] = " "
#         return best
#
# def ai_move():
#     empty = [i for i in range(9) if board[i] == " "]
#
#     if difficulty == "Easy":
#         move = random.choice(empty)
#     elif difficulty == "Medium" and random.random() < 0.5:
#         move = random.choice(empty)
#     else:
#         best, move = -math.inf, None
#         for i in empty:
#             board[i] = ai
#             score = minimax(board, False)
#             board[i] = " "
#             if score > best:
#                 best, move = score, i
#
#     board[move] = ai
#     return move
#
# # ---------- UI ----------
# def card(widget, color=CARD):
#     with widget.canvas.before:
#         Color(*color)
#         widget.rect = RoundedRectangle(radius=[20], pos=widget.pos, size=widget.size)
#     widget.bind(pos=lambda w, v: setattr(w.rect, "pos", v))
#     widget.bind(size=lambda w, v: setattr(w.rect, "size", v))
#
# # ---------- HOME ----------
# class Home(Screen):
#     def __init__(self, **kw):
#         super().__init__(**kw)
#
#         layout = BoxLayout(orientation="vertical", padding=25, spacing=20)
#         card(layout, BG)
#
#         self.score = Label(text="", font_size=16)
#         layout.add_widget(Label(text="TIC-TAC-TOE", font_size=32, color=ACCENT))
#         layout.add_widget(self.score)
#
#         layout.add_widget(Button(text="Start Game", size_hint_y=None, height=50,
#                                  on_press=lambda x: setattr(self.manager, "current", "level")))
#         layout.add_widget(Button(text="Reset Scores", size_hint_y=None, height=50,
#                                  on_press=self.reset))
#         layout.add_widget(Button(text="Exit", size_hint_y=None, height=50,
#                                  on_press=lambda x: App.get_running_app().stop()))
#
#         self.add_widget(layout)
#
#     def on_enter(self):
#         self.score.text = f"You: {player_score}  AI: {ai_score}  Draws: {draws}"
#
#     def reset(self, x):
#         global player_score, ai_score, draws
#         player_score = ai_score = draws = 0
#         save_scores()
#         self.on_enter()
#
# # ---------- LEVEL ----------
# class Level(Screen):
#     def __init__(self, **kw):
#         super().__init__(**kw)
#
#         layout = BoxLayout(orientation="vertical", padding=25, spacing=15)
#         card(layout, BG)
#
#         layout.add_widget(Label(text="Select Difficulty", font_size=20, color=ACCENT))
#
#         for lvl in ["Easy", "Medium", "Hard"]:
#             layout.add_widget(Button(text=lvl, size_hint_y=None, height=50,
#                                      on_press=lambda x, l=lvl: self.set(l)))
#
#         layout.add_widget(Button(text="Back", size_hint_y=None, height=50,
#                                  on_press=lambda x: setattr(self.manager, "current", "home")))
#
#         self.add_widget(layout)
#
#     def set(self, lvl):
#         global difficulty, starting_player
#         difficulty = lvl
#         starting_player = "player"
#         self.manager.get_screen("game").reset_board()
#         self.manager.current = "game"
#
# # ---------- GAME ----------
# class Game(Screen):
#     def __init__(self, **kw):
#         super().__init__(**kw)
#
#         main = BoxLayout(orientation="vertical", padding=15, spacing=10)
#         card(main, BG)
#
#         # TOP PANEL
#         self.result_text = Label(text="", font_size=18, color=ACCENT)
#         self.score_text = Label(text="", font_size=14)
#
#         self.next_btn = Button(text="Next Round", size_hint_y=None, height=40)
#         self.home_btn = Button(text="Home", size_hint_y=None, height=40)
#
#         self.next_btn.bind(on_press=lambda x: self.next_round())
#         self.home_btn.bind(on_press=lambda x: self.go_home())
#
#         # Hide initially
#         self.next_btn.opacity = 0
#         self.next_btn.disabled = True
#         self.home_btn.opacity = 0
#         self.home_btn.disabled = True
#
#         top_panel = BoxLayout(orientation="vertical", size_hint_y=0.5, height=80, spacing=5)
#         top_panel.add_widget(self.result_text)
#         top_panel.add_widget(self.score_text)
#
#         btn_row = BoxLayout(size_hint_y=None, height=40, spacing=10)
#         btn_row.add_widget(self.next_btn)
#         btn_row.add_widget(self.home_btn)
#
#         top_panel.add_widget(btn_row)
#         main.add_widget(top_panel)
#
#         # STATUS
#         self.status = Label(text="Your Turn", font_size=18)
#         main.add_widget(self.status)
#
#         # GRID
#         self.grid = GridLayout(cols=3, spacing=10, size_hint=(1, 1.5))
#         self.buttons = []
#
#         for i in range(9):
#             btn = Button(font_size=36,
#                          background_normal="",
#                          background_color=CARD)
#             btn.bind(on_press=lambda x, i=i: self.move(i))
#             self.buttons.append(btn)
#             self.grid.add_widget(btn)
#
#         main.add_widget(self.grid)
#
#         self.add_widget(main)
#
#     def reset_board(self):
#         global board
#         board = [" "] * 9
#
#         for b in self.buttons:
#             b.text = ""
#             b.background_color = CARD
#             b.disabled = False
#
#         self.status.text = "Your Turn"
#         self.result_text.text = ""
#         self.score_text.text = ""
#
#         # Hide buttons again
#         self.next_btn.opacity = 0
#         self.next_btn.disabled = True
#         self.home_btn.opacity = 0
#         self.home_btn.disabled = True
#
#     def move(self, i):
#         if board[i] != " ":
#             return
#
#         board[i] = player
#         self.buttons[i].text = player
#
#         combo = check_winner(board, player)
#         if combo:
#             self.highlight(combo)
#             self.end("You Won 😏", "player")
#             return
#
#         if is_draw(board):
#             self.end("Draw 🤝", "draw")
#             return
#
#         self.disable()
#         self.status.text = "AI thinking..."
#         Clock.schedule_once(self.ai_turn, 0.5)
#
#     def ai_turn(self, dt):
#         move = ai_move()
#         self.buttons[move].text = ai
#
#         combo = check_winner(board, ai)
#         if combo:
#             self.highlight(combo)
#             self.end("AI Won 🤖", "ai")
#             return
#
#         if is_draw(board):
#             self.end("Draw 🤝", "draw")
#             return
#
#         self.status.text = "Your Turn"
#         self.enable()
#
#     def end(self, text, result):
#         global player_score, ai_score, draws
#
#         self.disable()
#
#         if result == "player":
#             player_score += 1
#         elif result == "ai":
#             ai_score += 1
#         else:
#             draws += 1
#
#         save_scores()
#
#         self.result_text.text = text
#         self.score_text.text = f"You: {player_score}  AI: {ai_score}  Draws: {draws}"
#
#         # Show buttons
#         self.next_btn.opacity = 1
#         self.next_btn.disabled = False
#         self.home_btn.opacity = 1
#         self.home_btn.disabled = False
#
#     def next_round(self):
#         global starting_player
#
#         starting_player = "ai" if starting_player == "player" else "player"
#         self.reset_board()
#
#         if starting_player == "ai":
#             self.disable()
#             self.status.text = "AI thinking..."
#             Clock.schedule_once(self.ai_turn, 0.5)
#
#     def go_home(self):
#         self.manager.current = "home"
#
#     def highlight(self, combo):
#         for i in combo:
#             self.buttons[i].background_color = WIN
#
#     def disable(self):
#         for b in self.buttons:
#             b.disabled = True
#
#     def enable(self):
#         for i, b in enumerate(self.buttons):
#             if board[i] == " ":
#                 b.disabled = False
#
# # ---------- APP ----------
# class TicTacToeApp(App):
#     def build(self):
#         load_scores()
#
#         sm = ScreenManager()
#         sm.add_widget(Home(name="home"))
#         sm.add_widget(Level(name="level"))
#         sm.add_widget(Game(name="game"))
#
#         return sm
#
# TicTacToeApp().run()

import streamlit as st
import random
import math
import os
import time

# ---------- PAGE ----------
st.set_page_config(
    page_title="Tic-Tac-Toe",
    layout="centered"
)

# ---------- COLORS ----------
BG = "#141416"
CARD = "#1f1f26"
ACCENT = "#00cccc"
WIN = "#00ff88"

# ---------- CSS ----------
st.markdown(f"""
<style>

html, body, [class*="css"] {{
    background-color: {BG};
    color: white;
}}

.block-container {{
    padding-top: 2rem;
    max-width: 550px;
}}

.title {{
    text-align: center;
    font-size: 40px;
    font-weight: bold;
    color: {ACCENT};
    margin-bottom: 10px;
}}

.score {{
    text-align: center;
    font-size: 18px;
    margin-bottom: 20px;
}}

.status {{
    text-align: center;
    font-size: 22px;
    margin-top: 10px;
    margin-bottom: 20px;
}}

.stButton > button {{
    width: 100%;
    height: 140px;
    font-size: 48px;
    border-radius: 20px;
    border: none;
    background-color: #1f1f26;
    color: white;
}}

.menu-btn > button {{
    height: 50px !important;
    font-size: 16px !important;
}}

</style>
""", unsafe_allow_html=True)

# ---------- GLOBALS ----------
player = "X"
ai = "O"

SCORE_FILE = "scores.txt"

# ---------- SESSION ----------
if "board" not in st.session_state:
    st.session_state.board = [" "] * 9

if "difficulty" not in st.session_state:
    st.session_state.difficulty = "Hard"

if "player_score" not in st.session_state:
    st.session_state.player_score = 0

if "ai_score" not in st.session_state:
    st.session_state.ai_score = 0

if "draws" not in st.session_state:
    st.session_state.draws = 0

if "status" not in st.session_state:
    st.session_state.status = "Your Turn"

if "game_over" not in st.session_state:
    st.session_state.game_over = False

if "winner_combo" not in st.session_state:
    st.session_state.winner_combo = []

if "result" not in st.session_state:
    st.session_state.result = ""

if "page" not in st.session_state:
    st.session_state.page = "home"

if "starting_player" not in st.session_state:
    st.session_state.starting_player = "player"

# ---------- SCORE ----------
def load_scores():

    if os.path.exists(SCORE_FILE):

        with open(SCORE_FILE, "r") as f:

            data = f.read().split(",")

            if len(data) == 3:

                st.session_state.player_score = int(data[0])
                st.session_state.ai_score = int(data[1])
                st.session_state.draws = int(data[2])

def save_scores():

    with open(SCORE_FILE, "w") as f:

        f.write(
            f"{st.session_state.player_score},"
            f"{st.session_state.ai_score},"
            f"{st.session_state.draws}"
        )

load_scores()

# ---------- LOGIC ----------
def check_winner(board, p):

    combos = [
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8],
        [0,4,8],[2,4,6]
    ]

    for c in combos:

        if all(board[i] == p for i in c):
            return c

    return None

def is_draw(board):
    return " " not in board

def minimax(board, is_max):

    if check_winner(board, ai):
        return 1

    if check_winner(board, player):
        return -1

    if is_draw(board):
        return 0

    if is_max:

        best = -math.inf

        for i in range(9):

            if board[i] == " ":

                board[i] = ai

                best = max(best, minimax(board, False))

                board[i] = " "

        return best

    else:

        best = math.inf

        for i in range(9):

            if board[i] == " ":

                board[i] = player

                best = min(best, minimax(board, True))

                board[i] = " "

        return best

# ---------- AI ----------
def ai_move():

    board = st.session_state.board

    empty = [i for i in range(9) if board[i] == " "]

    if st.session_state.difficulty == "Easy":

        move = random.choice(empty)

    elif (
        st.session_state.difficulty == "Medium"
        and random.random() < 0.5
    ):

        move = random.choice(empty)

    else:

        best = -math.inf
        move = None

        for i in empty:

            board[i] = ai

            score = minimax(board, False)

            board[i] = " "

            if score > best:

                best = score
                move = i

    board[move] = ai

    return move

# ---------- RESET ----------
def reset_board():

    st.session_state.board = [" "] * 9
    st.session_state.status = "Your Turn"
    st.session_state.game_over = False
    st.session_state.result = ""
    st.session_state.winner_combo = []

# ---------- END ----------
def end_game(text, result):

    st.session_state.game_over = True
    st.session_state.result = text

    if result == "player":
        st.session_state.player_score += 1

    elif result == "ai":
        st.session_state.ai_score += 1

    else:
        st.session_state.draws += 1

    save_scores()

# ---------- PLAYER MOVE ----------
def move(i):

    if st.session_state.game_over:
        return

    if st.session_state.board[i] != " ":
        return

    st.session_state.board[i] = player

    combo = check_winner(st.session_state.board, player)

    if combo:

        st.session_state.winner_combo = combo

        end_game("You Won 😏", "player")

        return

    if is_draw(st.session_state.board):

        end_game("Draw 🤝", "draw")

        return

    st.session_state.status = "AI thinking..."

    time.sleep(0.5)

    ai_index = ai_move()

    combo = check_winner(st.session_state.board, ai)

    if combo:

        st.session_state.winner_combo = combo

        end_game("AI Won 🤖", "ai")

        return

    if is_draw(st.session_state.board):

        end_game("Draw 🤝", "draw")

        return

    st.session_state.status = "Your Turn"

# ---------- HOME ----------
if st.session_state.page == "home":

    st.markdown(
        '<div class="title">TIC-TAC-TOE</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="score">
        You: {st.session_state.player_score}
        &nbsp;&nbsp;&nbsp;
        AI: {st.session_state.ai_score}
        &nbsp;&nbsp;&nbsp;
        Draws: {st.session_state.draws}
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("Start Game", use_container_width=True):

        st.session_state.page = "level"

        st.rerun()

    if st.button("Reset Scores", use_container_width=True):

        st.session_state.player_score = 0
        st.session_state.ai_score = 0
        st.session_state.draws = 0

        save_scores()

        st.rerun()

    if st.button("Exit", use_container_width=True):

        st.stop()

# ---------- LEVEL ----------
elif st.session_state.page == "level":

    st.markdown(
        '<div class="title">Select Difficulty</div>',
        unsafe_allow_html=True
    )

    for lvl in ["Easy", "Medium", "Hard"]:

        if st.button(lvl, use_container_width=True):

            st.session_state.difficulty = lvl

            reset_board()

            st.session_state.page = "game"

            st.rerun()

    if st.button("Back", use_container_width=True):

        st.session_state.page = "home"

        st.rerun()

# ---------- GAME ----------
elif st.session_state.page == "game":

    st.markdown(
        f"""
        <div class="status">
        {st.session_state.status}
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.session_state.result:

        st.markdown(
            f"""
            <div class="status" style="color:{ACCENT};">
            {st.session_state.result}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="score">
            You: {st.session_state.player_score}
            &nbsp;&nbsp;&nbsp;
            AI: {st.session_state.ai_score}
            &nbsp;&nbsp;&nbsp;
            Draws: {st.session_state.draws}
            </div>
            """,
            unsafe_allow_html=True
        )

    # GRID
    for row in range(3):

        cols = st.columns(3)

        for col in range(3):

            i = row * 3 + col

            text = st.session_state.board[i]

            if i in st.session_state.winner_combo:

                st.markdown(f"""
                <style>
                div[data-testid="stButton"] button[kind="secondary"] {{
                    background-color: {WIN};
                }}
                </style>
                """, unsafe_allow_html=True)

            with cols[col]:

                st.button(
                    text,
                    key=i,
                    on_click=move,
                    args=(i,)
                )

    # BUTTONS
    if st.session_state.game_over:

        col1, col2 = st.columns(2)

        with col1:

            if st.button("Next Round", use_container_width=True):

                st.session_state.starting_player = (
                    "ai"
                    if st.session_state.starting_player == "player"
                    else "player"
                )

                reset_board()

                if st.session_state.starting_player == "ai":

                    st.session_state.status = "AI thinking..."

                    time.sleep(0.5)

                    ai_move()

                    st.session_state.status = "Your Turn"

                st.rerun()

        with col2:

            if st.button("Home", use_container_width=True):

                st.session_state.page = "home"

                st.rerun()