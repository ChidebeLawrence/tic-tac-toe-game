import tkinter as tk
from tkinter import ttk, messagebox
import random
import math
import os

# ---------- GLOBALS ----------
player = "X"
ai = "O"

board = [" " for _ in range(9)]
buttons = []

player_score = 0
ai_score = 0
draws = 0

difficulty = "Medium"
game_result = ""

starting_player = "player"
thinking_job = None
dots = 0

SCORE_FILE = "scores.txt"

# ---------- SCORE SAVE / LOAD ----------
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

# ✅ RESET SCORES FUNCTION
def reset_scores():
    global player_score, ai_score, draws

    confirm = messagebox.askyesno("Reset Scores", "Are you sure you want to reset all scores?")
    if confirm:
        player_score = 0
        ai_score = 0
        draws = 0

        save_scores()
        update_home_score()

# ---------- BUTTON CONTROL ----------
def disable_buttons():
    for btn in buttons:
        btn.config(state="disabled")

def enable_buttons():
    for i, btn in enumerate(buttons):
        if board[i] == " ":
            btn.config(state="normal")

# ---------- GAME LOGIC ----------
def check_winner(b, p):
    combos = [
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8],
        [0,4,8],[2,4,6]
    ]
    for combo in combos:
        if all(b[i] == p for i in combo):
            return combo
    return None

def is_draw(b):
    return " " not in b

def minimax(b, is_max):
    if check_winner(b, ai):
        return 1
    if check_winner(b, player):
        return -1
    if is_draw(b):
        return 0

    if is_max:
        best = -math.inf
        for i in range(9):
            if b[i] == " ":
                b[i] = ai
                score = minimax(b, False)
                b[i] = " "
                best = max(best, score)
        return best
    else:
        best = math.inf
        for i in range(9):
            if b[i] == " ":
                b[i] = player
                score = minimax(b, True)
                b[i] = " "
                best = min(best, score)
        return best

def ai_move():
    empty = [i for i in range(9) if board[i] == " "]

    if difficulty == "Easy":
        move = random.choice(empty)
    elif difficulty == "Medium" and random.random() < 0.5:
        move = random.choice(empty)
    else:
        best_score = -math.inf
        move = None
        for i in empty:
            board[i] = ai
            score = minimax(board, False)
            board[i] = " "
            if score > best_score:
                best_score = score
                move = i

    board[move] = ai
    buttons[move].config(text=ai)

# ---------- THINKING ANIMATION ----------
def animate_thinking():
    global dots, thinking_job

    dots = (dots + 1) % 4
    status_label.config(text="AI thinking" + "." * dots)

    thinking_job = root.after(300, animate_thinking)

def stop_thinking():
    global thinking_job
    if thinking_job:
        root.after_cancel(thinking_job)
        thinking_job = None

# ---------- WIN HIGHLIGHT ----------
def highlight_winner(combo):
    for i in combo:
        buttons[i].config(bg="#00ff88")

# ---------- SCREEN SWITCH ----------
def show_frame(frame):
    frame.tkraise()

# ---------- UPDATE HOME SCORE ----------
def update_home_score():
    home_score_label.config(
        text=f"You: {player_score}  AI: {ai_score}  Draws: {draws}"
    )

# ---------- HOME SCREEN ----------
def create_home():
    frame = tk.Frame(root, bg="#1e1e1e")

    tk.Label(frame, text="TIC-TAC-TOE",
             font=("Segoe UI", 24, "bold"),
             fg="#00adb5", bg="#1e1e1e").pack(pady=30)

    global home_score_label
    home_score_label = tk.Label(frame,
        text="",
        font=("Segoe UI", 12),
        fg="white", bg="#1e1e1e")
    home_score_label.pack(pady=10)

    tk.Button(frame, text="Start Game", width=15,
              command=lambda: show_frame(level_frame)).pack(pady=2)

    # ✅ RESET BUTTON ADDED HERE
    tk.Button(frame, text="Reset Scores", width=15,
              command=reset_scores).pack(pady=10)

    tk.Button(frame, text="Exit", width=15,
              command=root.quit).pack()

    return frame

# ---------- LEVEL SCREEN ----------
def create_level():
    frame = tk.Frame(root, bg="#1e1e1e")

    tk.Label(frame, text="Select Difficulty",
             font=("Segoe UI", 18),
             fg="white", bg="#1e1e1e").pack(pady=20)

    box = ttk.Combobox(frame,
                       values=["Easy", "Medium", "Hard"],
                       state="readonly")
    box.set("Hard")
    box.pack(pady=10)

    def start():
        global difficulty, starting_player

        difficulty = box.get()
        starting_player = "player"

        reset_board()
        show_frame(game_frame)

        status_label.config(text="Your Turn")
        enable_buttons()

    tk.Button(frame, text="Start",
              command=start).pack(pady=10)

    tk.Button(frame, text="Back",
              command=lambda: show_frame(home_frame)).pack()

    return frame

# ---------- GAME SCREEN ----------
def create_game():
    frame = tk.Frame(root, bg="#1e1e1e")

    global status_label
    status_label = tk.Label(frame, text="Your Turn",
                            fg="white", bg="#1e1e1e")
    status_label.pack(pady=5)

    tk.Button(frame, text="Restart",
              command=reset_board).pack(pady=5)

    board_frame = tk.Frame(frame, bg="#1e1e1e")
    board_frame.pack()

    for i in range(9):
        btn = tk.Button(board_frame, text="", width=5, height=2,
                        font=("Segoe UI", 18),
                        command=lambda i=i: player_move(i))
        btn.grid(row=i//3, column=i%3, padx=5, pady=5)
        buttons.append(btn)

    return frame

def player_move(i):
    global game_result

    if board[i] != " ":
        return

    board[i] = player
    buttons[i].config(text=player)

    combo = check_winner(board, player)
    if combo:
        highlight_winner(combo)
        game_result = "You Won! 😏"
        end_round("player")
        return

    if is_draw(board):
        game_result = "It's a Draw 🤝"
        end_round("draw")
        return

    disable_buttons()
    animate_thinking()
    root.after(500, ai_turn)

def ai_turn():
    global game_result

    stop_thinking()
    ai_move()

    combo = check_winner(board, ai)
    if combo:
        highlight_winner(combo)
        game_result = "AI Won 🤖"
        end_round("ai")
        return

    if is_draw(board):
        game_result = "It's a Draw 🤝"
        end_round("draw")
        return

    status_label.config(text="Your Turn")
    enable_buttons()

# ---------- POP-UP RESULT ----------
def show_end_popup():
    popup = tk.Toplevel(root)
    popup.title("Round Result")
    popup.geometry("280x230")
    popup.configure(bg="#1e1e1e")
    popup.grab_set()

    tk.Label(popup, text=game_result,
             font=("Segoe UI", 16, "bold"),
             fg="#00adb5", bg="#1e1e1e").pack(pady=15)

    tk.Label(popup,
             text=f"You: {player_score}  AI: {ai_score}  Draws: {draws}",
             fg="white", bg="#1e1e1e").pack(pady=5)

    def next_round_popup():
        popup.destroy()
        next_round()

    def go_home_popup():
        popup.destroy()
        update_home_score()
        show_frame(home_frame)

    tk.Button(popup, text="Next Round",
              command=next_round_popup, width=15).pack(pady=5)

    tk.Button(popup, text="Home",
              command=go_home_popup, width=15).pack(pady=5)

# ---------- ROUND HANDLING ----------
def end_round(result):
    global player_score, ai_score, draws

    if result == "player":
        player_score += 1
    elif result == "ai":
        ai_score += 1
    else:
        draws += 1

    save_scores()
    update_home_score()
    show_end_popup()

def next_round():
    global starting_player

    starting_player = "ai" if starting_player == "player" else "player"

    reset_board()
    show_frame(game_frame)

    if starting_player == "ai":
        disable_buttons()
        animate_thinking()
        root.after(500, ai_turn)
    else:
        status_label.config(text="Your Turn")
        enable_buttons()

# ---------- RESET BOARD ----------
def reset_board():
    global board
    board = [" " for _ in range(9)]
    for btn in buttons:
        btn.config(text="", state="normal", bg="#f0f0f0")
    status_label.config(text="Your Turn")

# ---------- MAIN ----------
root = tk.Tk()
root.title("Tic-Tac-Toe Pro")
root.geometry("300x400")
root.configure(bg="#1e1e1e")

load_scores()

home_frame = create_home()
level_frame = create_level()
game_frame = create_game()

for frame in (home_frame, level_frame, game_frame):
    frame.place(relwidth=1, relheight=1)

update_home_score()
show_frame(home_frame)

root.mainloop()