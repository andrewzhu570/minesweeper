class Solver:
    directions = [(-1, -1), (-1, 0), (-1, 1),
     (0, -1), (0, 1),
     (1, -1), (1, 0), (1, 1)]
    def __init__(self, board):
        self.board = board
        self.size = board.size


    def get_hidden_neighbors(self, r, c):
        hidden_list = []
        for dr, dc in self.directions:
            nr, nc = r + dr, c + dc

            if 0 <= nr < self.size and 0 <= nc < self.size:
                if not self.board.grid[nr][nc].revealed and not self.board.grid[nr][nc].flagged:
                    hidden_list.append((nr, nc))

        return hidden_list

    def get_flagged_neighbors(self, r, c):
        flagged_list = []
        for dr, dc in self.directions:
            nr, nc = r + dr, c + dc

            if 0 <= nr < self.size and 0 <= nc < self.size:
                if self.board.grid[nr][nc].flagged:
                    flagged_list.append((nr, nc))

        return flagged_list

    def get_cell_info(self, r, c):

        hidden = set(self.get_hidden_neighbors(r, c))
        flags = len(self.get_flagged_neighbors(r, c))
        remaining_mines = self.board.grid[r][c].neighbor_mines - flags

        return hidden, remaining_mines

    def find_safe_moves(self):
        safe_moves = set()
        for r in range(self.size):
            for c in range(self.size):
                if not self.board.grid[r][c].revealed:
                    continue
                if self.board.grid[r][c].neighbor_mines == 0:
                    continue

                flag_count = len(self.get_flagged_neighbors(r, c))
                if self.board.grid[r][c].neighbor_mines == flag_count:
                    for dr, dc in self.directions:
                        nr, nc = r + dr, c + dc

                        if 0 <= nr < self.size and 0 <= nc < self.size:
                            if not self.board.grid[nr][nc].revealed and not self.board.grid[nr][nc].flagged:
                                safe_moves.add((nr, nc))
        return safe_moves

    def find_mines(self):
        mines = set()
        for r in range(self.size):
            for c in range(self.size):
                if not self.board.grid[r][c].revealed:
                    continue
                if self.board.grid[r][c].neighbor_mines == 0:
                    continue

                flag_count = len(self.get_flagged_neighbors(r, c))
                hidden_count = len(self.get_hidden_neighbors(r, c))
                if self.board.grid[r][c].neighbor_mines - flag_count == hidden_count:
                    for dr, dc in self.directions:
                        nr, nc = r + dr, c + dc

                        if 0 <= nr < self.size and 0 <= nc < self.size:
                            if not self.board.grid[nr][nc].revealed and not self.board.grid[nr][nc].flagged:
                                mines.add((nr, nc))
        return mines

    def find_subset_moves(self):
        safe_moves = set()
        mine_moves = set()

        for r in range(self.size):
            for c in range(self.size):
                if not self.board.grid[r][c].revealed:
                    continue

                hidden1, mines1 = self.get_cell_info(r, c)
                if not hidden1:
                    continue

                for dr, dc in self.directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.size and 0 <= nc < self.size:
                        if not self.board.grid[nr][nc].revealed:
                            continue

                        hidden2, mines2 = self.get_cell_info(nr, nc)
                        if not hidden2:
                            continue

                        if hidden1.issubset(hidden2) and hidden1 != hidden2:
                            diff_cells = hidden2 - hidden1
                            diff_mines = mines2 - mines1

                            if diff_mines == 0:
                                for each in diff_cells:
                                    safe_moves.add(each)

                            elif diff_mines == len(diff_cells):
                                for each in diff_cells:
                                    mine_moves.add(each)

        return safe_moves, mine_moves

    def auto_flag(self):
        flags_added = 0
        mine_moves = self.find_mines()
        for r, c in mine_moves:
            if not self.board.grid[r][c].flagged:
                self.board.grid[r][c].flagged = True
                flags_added += 1

        return flags_added > 0

    def auto_reveal(self):
        cells_revealed = 0
        safe_moves = self.find_safe_moves()
        for r, c in safe_moves:
            self.board.reveal(r, c)
            cells_revealed += 1

        return cells_revealed > 0

    def auto_subset_solve(self):
        changed = False

        safe_moves, mine_moves = self.find_subset_moves()

        for r, c in mine_moves:
            if not self.board.grid[r][c].flagged:
                self.board.grid[r][c].flagged = True
                changed = True

        for r, c in safe_moves:
            if not self.board.grid[r][c].revealed:
                self.board.reveal(r, c)
                changed = True

        return changed

    """Solve step function for web version, tkinter version is located in gui.py"""
    def solve_step(self):
        changed = False

        if self.auto_flag():
            changed = True

        if self.auto_reveal():
            changed = True

        if not changed:
            if self.auto_subset_solve():
                changed = True

        return changed



