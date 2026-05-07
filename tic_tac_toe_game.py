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

div[data-testid="stButton"] button {{
    width: 100%;
    height: 140px;
    font-size: 48px;
    border-radius: 20px;
    border: none;
    background-color: {CARD};
    color: white;
    transition: 0.2s;
}}

div[data-testid="stButton"] button:hover {{
    transform: scale(1.03);
}}

</style>
""", unsafe_allow_html=True)

# ---------- CONSTANTS ----------
player = "X"
ai = "O"

SCORE_FILE = "scores.txt"

# ---------- SESSION ----------
defaults = {
    "board": [" "] * 9,
    "difficulty": "Hard",
    "player_score": 0,
    "ai_score": 0,
    "draws": 0,
    "status": "Your Turn",
    "game_over": False,
    "winner_combo": [],
    "result": "",
    "page": "home",
    "starting_player": "player"
}

for key, value in defaults.items():

    if key not in st.session_state:
        st.session_state[key] = value

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

# ---------- GAME LOGIC ----------
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

    ai_move()

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

    # ---------- GRID ----------
    button_index = 0

    for row in range(3):

        cols = st.columns(3)

        for col in range(3):
            i = row * 3 + col

            text = st.session_state.board[i]

            # only winning cells become green
            bg_color = WIN if i in st.session_state.winner_combo else CARD

            # Streamlit button position selector
            st.markdown(
                f"""
                <style>

                div[data-testid="stButton"]:nth-of-type({button_index + 1}) button {{
                    background-color: {bg_color} !important;
                    color: white !important;
                    height: 140px !important;
                    width: 100% !important;
                    border-radius: 20px !important;
                    border: none !important;
                    font-size: 48px !important;
                    font-weight: bold !important;
                }}

                </style>
                """,
                unsafe_allow_html=True
            )

            with cols[col]:
                st.button(
                    text if text != " " else " ",
                    key=f"cell_{i}",
                    on_click=move,
                    args=(i,),
                    disabled=(
                            st.session_state.game_over
                            or st.session_state.board[i] != " "
                    ),
                    use_container_width=True
                )

            button_index += 1

    # ---------- BUTTONS ----------
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