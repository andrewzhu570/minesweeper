import minesweeper as mine
import solver
import random

def benchmark(size, mines, total_games=100):
    print(f"Starting benchmark for a board of size {size} and {mines} mines over {total_games} games.")
    wins = 0
    directions = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1), (0, 1),
                  (1, -1), (1, 0), (1, 1)]

    for game in range(1, total_games + 1):
        board = mine.Board(size, mines)
        solve = solver.Solver(board)

        """Starts the game by revealing a 0 that boarders at least one other 0 so the algorithms do not get stuck on a single revealed cell."""
        found_optimal_move = False

        for r in range(board.size):
            for c in range(board.size):
                if board.grid[r][c].neighbor_mines == 0 and not board.grid[r][c].has_mine:
                    borders_zero = False
                    for dr, dc in directions:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < board.size and 0 <= nc < board.size:
                            if board.grid[nr][nc].neighbor_mines == 0:
                                borders_zero = True
                                break

                    if borders_zero:
                        board.reveal(r, c)
                        found_optimal_move = True
                        break
            if found_optimal_move:
                break

        if not found_optimal_move:
            fallback_r, fallback_c = board.size // 2, board.size // 2

            # Check to make sure the fallback click is mine-safe
            if board.grid[fallback_r][fallback_c].has_mine:
                board.move_mine(fallback_r, fallback_c)
                board.compute_numbers()

            board.reveal(fallback_r, fallback_c)

        board.first_click = False

        while not board.game_over:
            if board.check_win():
                wins += 1
                break

            changed = False

            safe_moves = solve.find_safe_moves()
            mine_moves = solve.find_mines()

            for r, c in safe_moves:
                if not board.grid[r][c].revealed and not board.grid[r][c].flagged:
                    board.reveal(r, c)
                    changed = True

            for r, c in mine_moves:
                if not board.grid[r][c].flagged:
                    board.grid[r][c].flagged = True
                    changed = True

            if not changed:
                subset_safe, subset_mine = solve.find_subset_moves()

                for r, c in subset_mine:
                    if not board.grid[r][c].flagged:
                        board.grid[r][c].flagged = True
                        changed = True

                for r, c in subset_safe:
                    if not board.grid[r][c].revealed and not board.grid[r][c].flagged:
                        board.reveal(r, c)
                        changed = True

            if not changed:
                unrevealed_cells = []
                for r in range(board.size):
                    for c in range(board.size):
                        if not board.grid[r][c].revealed and not board.grid[r][c].flagged:
                            unrevealed_cells.append([r, c])

                if unrevealed_cells:
                    gr, gc = random.choice(unrevealed_cells)
                    board.reveal(gr,gc)
                else:
                    break

    win_rate = (wins / total_games) * 100
    print(win_rate)

benchmark(20, 60, 100)

"""Easy: size = 8, mines = 7 | Intermediate: size = 14, mines = 25 | Advanced: size = 20, mines = 60"""