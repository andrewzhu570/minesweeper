from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import uuid

from minesweeper import Board
from solver import Solver

app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)

games = {}

@app.route('/')
def serve_index():
    return send_from_directory('static', 'index.html')


@app.route('/api/new-game', methods=["POST"])
def new_game():
    data = request.get_json() or {}
    size = data.get('size', 10)
    mines = data.get('mines', 15)
    board = Board(size=size, num_mines=mines)
    solver = Solver(board)

    game_id = str(uuid.uuid4())
    games[game_id] = {
        'board': board,
        'solver': solver
    }

    return jsonify({
            "status": "success",
            "size": board.size,
            "game_id": game_id,
            "num_mines": board.num_mines,
            "grid": board.get_board_state(),
            "game_over": board.game_over,
            "win": False
        })

@app.route('/api/click', methods=['POST'])
def click():
    data = request.get_json() or {}
    game_id = data.get('game_id')

    game_session = games.get(game_id)

    if not game_session:
        return jsonify({"error": "Game not found"}), 404

    board = game_session['board']
    solver = game_session['solver']


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

@app.route('/api/flag', methods=['POST'])
def flag():
    data = request.get_json() or {}
    game_id = data.get('game_id')
    game_session = games.get(game_id)
    if not game_session:
        return jsonify({"error": "Game not found"}), 404
    board = game_session['board']

    if board is None:
        return jsonify({"error": "No active game. Start a new game first."}), 400

    r = data.get('row')
    c = data.get('col')

    if r is None or c is None or not (0 <= r < board.size and 0 <= c < board.size):
        return jsonify({"error": "Invalid coordinates"}), 400

    cell = board.grid[r][c]

    if not cell.revealed and not board.game_over:
        cell.flagged = not cell.flagged

    return jsonify({
        "grid": board.get_board_state(),
        "game_over": board.game_over,
        "win": board.check_win()
    })

@app.route('/api/solve-step', methods=['POST'])
def solve_step():
    data = request.get_json() or {}
    game_id = data.get('game_id')
    game_session = games.get(game_id)
    if not game_session:
        return jsonify({"error": "Game not found"}), 404
    board = game_session['board']
    solver = game_session['solver']

    if board is None or solver is None:
        return jsonify({"error": "No active game. Start a new game first."}), 400

    if board.game_over or board.check_win():
        return jsonify({
            "status": "game_ended",
            "grid": board.get_board_state(),
            "game_over": board.game_over,
            "win": board.check_win()
        })

    changed = solver.solve_step()

    return jsonify({
        "status": "moved" if changed else "stuck",
        "grid": board.get_board_state(),
        "game_over": board.game_over,
        "win": board.check_win()
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)