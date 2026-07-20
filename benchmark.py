import minesweeper as mine
import solver

def benchmark(size, mines, total_games=100):
    print(f"Starting benchmark for a board of size {size} and {mines} mines over {total_games} games.")
    wins = 0

    for game in range(1, total_games + 1):
        board = mine.Board(size, mines)
        solve = solver.Solver(board)

        """Starts the game by revealing a 0 so the algorithms do not get stuck on a single revealed cell."""
        for r in range(board.size):
            for c in range(board.size):
                if board.grid[r][c].neighbor_mines == 0 and not board.grid[r][c].has_mine:
                    board.reveal(r, c)
                    break
            else:
                continue
            break
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
                break

    win_rate = (wins / total_games) * 100
    print(win_rate)

benchmark(8, 7, 100)