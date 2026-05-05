import math
import time
import random

# Score tracking
player_score = 0
ai_score = 0
draws = 0

# Print board
def print_board(board):
    for i in range(0, 9, 3):
        print(board[i] + " | " + board[i+1] + " | " + board[i+2])
        print("-" * 9)

# Check winner
def check_winner(b, player):
    win_combinations = [
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8],
        [0,4,8],[2,4,6]
    ]
    return any(all(b[i] == player for i in combo) for combo in win_combinations)

# Check draw
def is_draw(b):
    return " " not in b

# Minimax
def minimax(b, is_maximizing):
    if check_winner(b, "O"):
        return 1
    if check_winner(b, "X"):
        return -1
    if is_draw(b):
        return 0

    if is_maximizing:
        best_score = -math.inf
        for i in range(9):
            if b[i] == " ":
                b[i] = "O"
                score = minimax(b, False)
                b[i] = " "
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for i in range(9):
            if b[i] == " ":
                b[i] = "X"
                score = minimax(b, True)
                b[i] = " "
                best_score = min(score, best_score)
        return best_score

# AI move based on difficulty
def ai_move(board, difficulty):
    empty_spots = [i for i in range(9) if board[i] == " "]

    # EASY → random move
    if difficulty == "easy":
        move = random.choice(empty_spots)
        board[move] = "O"
        return

    # MEDIUM → mix of random and smart
    if difficulty == "medium":
        if random.random() < 0.5:
            move = random.choice(empty_spots)
            board[move] = "O"
            return
        # else fall through to minimax

    # HARD → minimax
    best_score = -math.inf
    move = None
    for i in empty_spots:
        board[i] = "O"
        score = minimax(board, False)
        board[i] = " "
        if score > best_score:
            best_score = score
            move = i
    board[move] = "O"

# Play one game
def play_game(starting_player, difficulty):
    board = [" " for _ in range(9)]

    print("\n🎮 New Game Started!")
    print(f"👉 {starting_player.upper()} starts first!")
    print(f"🎯 Difficulty: {difficulty.upper()}\n")

    print("Positions:")
    print("0 | 1 | 2")
    print("---------")
    print("3 | 4 | 5")
    print("---------")
    print("6 | 7 | 8\n")

    print_board(board)

    current_turn = starting_player

    while True:
        if current_turn == "player":
            try:
                move = int(input("Enter your move (0-8): "))
            except:
                print("❌ Enter a valid number.")
                continue

            if move < 0 or move > 8 or board[move] != " ":
                print("❌ Invalid move.")
                continue

            board[move] = "X"
            print("\nYou played:")
            print_board(board)

            if check_winner(board, "X"):
                print("🎉 You won!")
                return "player"

            current_turn = "ai"

        else:
            print("🤖 AI is thinking", end="")
            for _ in range(3):
                time.sleep(0.5)
                print(".", end="", flush=True)
            print()

            ai_move(board, difficulty)

            print("🤖 AI played:")
            print_board(board)

            if check_winner(board, "O"):
                print("🤖 AI won!")
                return "ai"

            current_turn = "player"

        if is_draw(board):
            print("🤝 It's a draw!")
            return "draw"

# Main loop
def main():
    global player_score, ai_score, draws

    print("=== TIC-TAC-TOE (WITH AI) ===")

    starting_player = "player"

    while True:
        # Ask for difficulty EVERY round
        while True:
            difficulty = input("\nChoose difficulty (easy / medium / hard): ").lower()
            if difficulty in ["easy", "medium", "hard"]:
                break
            print("❌ Invalid choice.")

        result = play_game(starting_player, difficulty)

        if result == "player":
            player_score += 1
        elif result == "ai":
            ai_score += 1
        else:
            draws += 1

        print("\n📊 SCOREBOARD")
        print(f"You: {player_score} | AI: {ai_score} | Draws: {draws}")

        # Alternate starter
        starting_player = "ai" if starting_player == "player" else "player"

        choice = input("\nPlay again? (y/n): ").lower()
        if choice != "y":
            print("\n👋 Thanks for playing!")
            break

# Run game
main()