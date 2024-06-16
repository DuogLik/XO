import streamlit as st
import random
import numpy as np

# Maximum depth of the search tree
MAX_DEPTH = 3

# Styles
def get_styles():
    return """
    <style>
    body {
        background-color: #23006F;
    }
    .square {
        display: inline-block;
        width: 60px;
        height: 60px;
        line-height: 60px;
        border: 5px solid #00C9C9;
        text-align: center;
        font-size: 24px;
        cursor: pointer;
        background-color: #1E006B;
        color: #FFF;
        margin: 5px;
        border-radius: 10px;
    }
    .header {
        text-align: center;
        margin-bottom: 30px;
        color: #FFF;
    }
    .title {
        text-align: center;
        font-size: 48px;
        font-weight: bold;
        color: #FFF;
        background: linear-gradient(to right, #FFEB3B, #FF4081, #3F51B5, #00BCD4);
        -webkit-background-clip: text;
        color: transparent;
    }
    .game-mode, .game-board {
        margin-bottom: 20px;
    }
    .game-board {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .board-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
    }
    .stats {
        text-align: center;
        margin-top: 20px;
        color: #FFF;
    }
    </style>
    """

# Minimax with Alpha-Beta Pruning
def alpha_beta_minimax(board, depth, alpha, beta, maximizing_player, player, opponent):
    winner = check_win(board)
    if winner == player:
        return 1, None
    elif winner == opponent:
        return -1, None
    elif winner == "Tie":
        return 0, None

    if depth == MAX_DEPTH:
        return 0, None

    if maximizing_player:
        max_eval = -np.inf
        best_move = None
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == " ":
                    board[i][j] = player
                    eval, _ = alpha_beta_minimax(board, depth + 1, alpha, beta, False, player, opponent)
                    board[i][j] = " "
                    if eval > max_eval:
                        max_eval = eval
                        best_move = (i, j)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
        return max_eval, best_move
    else:
        min_eval = np.inf
        best_move = None
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == " ":
                    board[i][j] = opponent
                    eval, _ = alpha_beta_minimax(board, depth + 1, alpha, beta, True, player, opponent)
                    board[i][j] = " "
                    if eval < min_eval:
                        min_eval = eval
                        best_move = (i, j)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
        return min_eval, best_move

# Initialize the game board
def initialize_board(size):
    return [[" " for _ in range(size)] for _ in range(size)]

# Check for a winner or a tie
def check_win(board):
    size = len(board)
    win_conditions = {
        3: 3,
        5: 4,
        7: 5
    }

    for i in range(size):
        for j in range(size):
            if board[i][j] != " ":
                player = board[i][j]

                # Check horizontally
                if j <= size - win_conditions[size]:
                    if all(board[i][j+k] == player for k in range(win_conditions[size])):
                        return player

                # Check vertically
                if i <= size - win_conditions[size]:
                    if all(board[i+k][j] == player for k in range(win_conditions[size])):
                        return player

                # Check diagonally (top-left to bottom-right)
                if i <= size - win_conditions[size] and j <= size - win_conditions[size]:
                    if all(board[i+k][j+k] == player for k in range(win_conditions[size])):
                        return player

                # Check diagonally (top-right to bottom-left)
                if i <= size - win_conditions[size] and j >= win_conditions[size] - 1:
                    if all(board[i+k][j-k] == player for k in range(win_conditions[size])):
                        return player

    if all(board[i][j] != " " for i in range(size) for j in range(size)):
        return "Tie"

    return ""

# Player makes a move
def player_move(board, row, col, icon):
    if board[row][col] == " ":
        board[row][col] = icon
        return True
    return False

# Computer makes a move
def computer_move(board, icon):
    opponent = "O" if icon == "X" else "X"
    size = len(board)
    available_moves = [(i, j) for i in range(size) for j in range(size) if board[i][j] == " "]

    move = alpha_beta_minimax(board, 0, -np.inf, np.inf, True, icon, opponent)[1]

    if move:
        board[move[0]][move[1]] = icon

# Main application
def main():
    st.markdown(get_styles(), unsafe_allow_html=True)
    st.markdown("<div class='title'>LET'S PLAY TIC TAC TOE</div>", unsafe_allow_html=True)

    st.sidebar.header("Game Mode")
    mode = st.sidebar.radio("Select Mode", ("2 Players", "Play with Computer"))

    st.sidebar.header("Game Board")
    if "board_size" not in st.session_state:
        st.session_state.board_size = 3

    board_size = st.sidebar.radio("Board Size", ["3x3", "5x5", "7x7"])

    if st.sidebar.button("Start New Game"):
        st.session_state.board_size = int(board_size[0])
        st.session_state.mode = mode
        st.session_state.board = initialize_board(st.session_state.board_size)
        st.session_state.current_player = "X"
        st.session_state.winner = ""
        st.session_state.playing = True

    if "board" not in st.session_state:
        st.session_state.board = initialize_board(st.session_state.board_size)
        st.session_state.current_player = "X"
        st.session_state.winner = ""
        st.session_state.playing = True

    # Initialize stats
    if "player_wins" not in st.session_state:
        st.session_state.player_wins = 0
    if "computer_wins" not in st.session_state:
        st.session_state.computer_wins = 0
    if "ties" not in st.session_state:
        st.session_state.ties = 0

    board = st.session_state.board
    current_player = st.session_state.current_player
    winner = st.session_state.winner
    playing = st.session_state.playing

    win_conditions = {
        3: 3,
        5: 4,
        7: 5
    }

    if winner == "":
        st.write(f"Player {current_player}'s Turn ({'X' if current_player == 'X' else 'O'})")
    else:
        if winner == "Tie":
            st.markdown("<h2 style='color: orange;'>It's a Tie!</h2>", unsafe_allow_html=True)
            st.session_state.ties += 1
        else:
            st.markdown(f"<h2 style='color: green;'>Player {winner} Wins!</h2>", unsafe_allow_html=True)
            if winner == "X":
                st.session_state.player_wins += 1
            else:
                st.session_state.computer_wins += 1

    # Display stats
    st.sidebar.header("Statistics")
    st.sidebar.markdown(f"- Player Wins: {st.session_state.player_wins}", unsafe_allow_html=True)
    st.sidebar.markdown(f"- Computer Wins: {st.session_state.computer_wins}", unsafe_allow_html=True)
    st.sidebar.markdown(f"- Ties: {st.session_state.ties}", unsafe_allow_html=True)

    # Display the board
    board_display = st.container()
    with board_display:
        for row in range(st.session_state.board_size):
            cols = st.columns(st.session_state.board_size)
            for col in range(st.session_state.board_size):
                if board[row][col] == " " and playing:
                    if cols[col].button(" ", key=f"{row}-{col}"):
                        if player_move(board, row, col, current_player):
                            st.session_state.winner = check_win(board)
                            if st.session_state.winner == "":
                                if st.session_state.mode == "Play with Computer" and current_player == "X":
                                    computer_move(board, "O")
                                    st.session_state.winner = check_win(board)
                                    if st.session_state.winner == "":
                                        st.session_state.current_player = "X"
                                    else:
                                        st.session_state.playing = False
                                else:
                                    st.session_state.current_player = "O" if current_player == "X" else "X"
                            else:
                                st.session_state.playing = False
                else:
                    content = f"<div class='square {board[row][col]}'>{board[row][col]}</div>"
                    cols[col].markdown(content, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

