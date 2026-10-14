import json
import random
import os

# ==========================================
# AI-BASED TIC-TAC-TOE GAME
# Using Minimax Algorithm
# ==========================================

HISTORY_FILE = "game_history.json"
SCOREBOARD_FILE = "scoreboard.json"

board = [" "] * 9

player_wins = 0
ai_wins = 0
draws = 0


# ==========================================
# CHECK WINNER
# ==========================================

def check_winner():
    winning_combinations = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6]
    ]

    for combination in winning_combinations:
        a, b, c = combination

        if (
            board[a] == board[b] == board[c]
            and board[a] != " "
        ):
            return board[a]

    return None


# ==========================================
# DISPLAY BOARD
# ==========================================

def display_board():
    print()
    print(f" {board[0]} | {board[1]} | {board[2]}")
    print("---+---+---")
    print(f" {board[3]} | {board[4]} | {board[5]}")
    print("---+---+---")
    print(f" {board[6]} | {board[7]} | {board[8]}")
    print()


def display_position_guide():
    print("\nPosition Guide:")
    print(" 1 | 2 | 3")
    print("---+---+---")
    print(" 4 | 5 | 6")
    print("---+---+---")
    print(" 7 | 8 | 9")


# ==========================================
# MINIMAX ALGORITHM
# ==========================================

def minimax(is_maximizing):
    winner = check_winner()

    if winner == "O":
        return 1

    if winner == "X":
        return -1

    if " " not in board:
        return 0

    if is_maximizing:
        best_score = -float("inf")

        for i in range(9):
            if board[i] == " ":
                board[i] = "O"
                score = minimax(False)
                board[i] = " "

                best_score = max(best_score, score)

        return best_score

    else:
        best_score = float("inf")

        for i in range(9):
            if board[i] == " ":
                board[i] = "X"
                score = minimax(True)
                board[i] = " "

                best_score = min(best_score, score)

        return best_score


# ==========================================
# FIND BEST AI MOVE
# ==========================================

def find_best_move():
    best_score = -float("inf")
    best_moves = []

    for i in range(9):
        if board[i] == " ":
            board[i] = "O"

            score = minimax(False)

            board[i] = " "

            if score > best_score:
                best_score = score
                best_moves = [i]

            elif score == best_score:
                best_moves.append(i)

    return random.choice(best_moves) if best_moves else None


# ==========================================
# AI DIFFICULTY LEVELS
# ==========================================

def get_ai_move(difficulty):

    available_moves = [
        i for i in range(9)
        if board[i] == " "
    ]

    # Easy mode: Win, block, or choose randomly
    if difficulty == "easy":

        # Take a winning move if possible
        for move in available_moves:
            board[move] = "O"
            won = check_winner() == "O"
            board[move] = " "

            if won:
                return move

        # Block the player's immediate winning move
        for move in available_moves:
            board[move] = "X"
            player_wins_next = check_winner() == "X"
            board[move] = " "

            if player_wins_next:
                return move

        return random.choice(available_moves)

    # Medium mode: Win, block, or use Minimax sometimes
    elif difficulty == "medium":

        # Always take a winning move
        for move in available_moves:
            board[move] = "O"
            won = check_winner() == "O"
            board[move] = " "

            if won:
                return move

        # Always block an immediate player win
        for move in available_moves:
            board[move] = "X"
            player_wins_next = check_winner() == "X"
            board[move] = " "

            if player_wins_next:
                return move

        # Use Minimax for most other decisions
        if random.random() < 0.8:
            return find_best_move()

        return random.choice(available_moves)

    # Hard mode: Always use Minimax
    else:
        return find_best_move()


# ==========================================
# GAME HISTORY
# ==========================================

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []

    try:
        with open(HISTORY_FILE, "r") as file:
            history = json.load(file)

            if isinstance(history, list):
                return history

            return []

    except (json.JSONDecodeError, OSError):
        return []


def save_game_result(result, difficulty):
    history = load_history()

    game_record = {
        "game_number": len(history) + 1,
        "result": result,
        "difficulty": difficulty
    }

    history.append(game_record)

    try:
        with open(HISTORY_FILE, "w") as file:
            json.dump(history, file, indent=4)

    except OSError:
        print("Warning: Game history could not be saved.")

    # Save the updated scoreboard permanently
    save_scoreboard()


def show_game_history():
    history = load_history()

    print("\n" + "=" * 42)
    print("              GAME HISTORY")
    print("=" * 42)

    if not history:
        print("No previous games found.")

    else:
        for game in history[-10:]:
            print(
                f"Game {game.get('game_number', '?')}: "
                f"{game.get('result', 'Unknown')} "
                f"| Difficulty: "
                f"{game.get('difficulty', 'Unknown').title()}"
            )

    print("=" * 42)


# ==========================================
# PERMANENT SCOREBOARD STORAGE
# ==========================================

def load_scoreboard():
    global player_wins, ai_wins, draws

    if not os.path.exists(SCOREBOARD_FILE):
        return

    try:
        with open(SCOREBOARD_FILE, "r") as file:
            scores = json.load(file)

        player_wins = scores.get("player_wins", 0)
        ai_wins = scores.get("ai_wins", 0)
        draws = scores.get("draws", 0)

    except (json.JSONDecodeError, OSError):
        print("Warning: Could not load the saved scoreboard.")


def save_scoreboard():
    scores = {
        "player_wins": player_wins,
        "ai_wins": ai_wins,
        "draws": draws
    }

    try:
        with open(SCOREBOARD_FILE, "w") as file:
            json.dump(scores, file, indent=4)

    except OSError:
        print("Warning: Scoreboard could not be saved.")


# ==========================================
# DISPLAY SCOREBOARD
# ==========================================

def display_scoreboard():
    total_games = player_wins + ai_wins + draws

    print("\n" + "=" * 42)
    print("           TIC-TAC-TOE SCOREBOARD")
    print("=" * 42)

    print(f"Total Games Played : {total_games}")
    print(f"Player Wins        : {player_wins}")
    print(f"AI Wins            : {ai_wins}")
    print(f"Draws              : {draws}")

    if total_games > 0:
        player_percentage = player_wins / total_games * 100
        ai_percentage = ai_wins / total_games * 100
        draw_percentage = draws / total_games * 100

        print(f"Player Win Rate    : {player_percentage:.1f}%")
        print(f"AI Win Rate        : {ai_percentage:.1f}%")
        print(f"Draw Rate          : {draw_percentage:.1f}%")

    print("=" * 42)


# ==========================================
# SELECT DIFFICULTY
# ==========================================

def choose_difficulty():
    while True:
        print("\nChoose Difficulty:")
        print("1. Easy")
        print("2. Medium")
        print("3. Hard")

        choice = input("Enter your choice (1-3): ").strip()

        if choice == "1":
            return "easy"

        elif choice == "2":
            return "medium"

        elif choice == "3":
            return "hard"

        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


# ==========================================
# PLAY ONE GAME
# ==========================================

def play_game(difficulty):
    global board, player_wins, ai_wins, draws

    board = [" "] * 9

    print("\n" + "=" * 42)
    print("       AI-BASED TIC-TAC-TOE")
    print("=" * 42)
    print("You are X | AI is O")
    print("Difficulty:", difficulty.title())

    display_position_guide()

    while True:

        # PLAYER TURN
        try:
            position = int(
                input("\nChoose a position (1-9): ")
            )

        except ValueError:
            print("Invalid input! Enter a number from 1 to 9.")
            continue

        if position < 1 or position > 9:
            print("Please choose a number between 1 and 9.")
            continue

        if board[position - 1] != " ":
            print("That position is occupied. Choose another.")
            continue

        board[position - 1] = "X"

        print("\nYour move:")
        display_board()

        if check_winner() == "X":
            print("Congratulations! You win!")
            player_wins += 1
            save_game_result("Player Won", difficulty)
            break

        if " " not in board:
            print("It's a draw!")
            draws += 1
            save_game_result("Draw", difficulty)
            break

        # AI TURN
        ai_move = get_ai_move(difficulty)

        board[ai_move] = "O"

        display_board()

        if check_winner() == "O":
            print("AI wins! Better luck next time.")
            ai_wins += 1
            save_game_result("AI Won", difficulty)
            break

        if " " not in board:
            print("It's a draw!")
            draws += 1
            save_game_result("Draw", difficulty)
            break

    # SHOW SCOREBOARD AFTER GAME ENDS
    display_scoreboard()


# ==========================================
# MAIN PROGRAM
# ==========================================

def main():
    while True:

        print("\n" + "=" * 42)
        print("       WELCOME TO TIC-TAC-TOE")
        print("=" * 42)
        print("1. Play Game")
        print("2. View Game History")
        print("3. Exit")

        choice = input("Choose an option (1-3): ").strip()

        if choice == "1":
            difficulty = choose_difficulty()
            play_game(difficulty)

            replay = input(
                "\nDo you want to play again? (yes/no): "
            ).strip().lower()

            if replay not in ("yes", "y"):
                print("\nThanks for playing!")
                break

        elif choice == "2":
            show_game_history()

        elif choice == "3":
            print("\nThanks for playing!")
            break

        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


# ==========================================
# START PROGRAM
# ==========================================

if __name__ == "__main__":
    load_scoreboard()
    main()