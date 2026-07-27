from flask import Flask, jsonify, request
from flask_cors import CORS

from minesweeper import Board
from solver import Solver

app = Flask(__name__)
CORS(app)

board: Board | None = None
solver = None

current_size = 8
current_mines = 7

@app.route('api/new-game', methods=["POST"])
def new_game():
    global board, solver, current_size, current_mines
    data = request.get_json() or {}
    if 'size' in data and 'mines' in data:
        current_size = data['size']
        current_mines = data['mines']

    board = Board(size=current_size, num_mines=current_mines)
    solver = Solver(board)

    return jsonify({
            "status": "success",
            "size": board.size,
            "num_mines": board.num_mines,
            "grid": board.get_board_state(),
            "game_over": board.game_over,
            "win": False
        })

@app.route('/api/click', methods=['POST'])
def click():
    global board, solver
    if not board:
        return jsonify({"error": "No active game. Start a new game first."}), 400

    data = request.get_json() or {}
    r = data.get('row')
    c = data.get('col')

    if r is None or c is None or not (0 <= r < board.size and 0 <= c < board.size):
        return jsonify({"error": "Invalid coordinates"}), 400

    cell = board.grid[r][c]

    if cell.flagged:
        return jsonify({
            "grid": board.get_board_state(),
            "game_over": board.game_over,
            "win": board.check_win()
        })

    if board.first_click:
        if cell.has_mine:
            board.move_mine(r, c)
            board.compute_numbers()
        board.first_click = False

    if cell.revealed:
        # Chording: if flagged neighbors match neighbor count, reveal hidden neighbors
        flag_count = len(solver.get_flagged_neighbors(r, c))
        if flag_count == cell.neighbor_mines:
            for dr, dc in solver.directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < board.size and 0 <= nc < board.size:
                    if not board.grid[nr][nc].revealed and not board.grid[nr][nc].flagged:
                        board.reveal(nr, nc)
    else:
        board.reveal(r, c)

    return jsonify({
        "grid": board.get_board_state(),
        "game_over": board.game_over,
        "win": board.check_win()
    })