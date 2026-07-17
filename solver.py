class Solver:
    def __init__(self, board):
        self.board = board
        self.size = board.size
        self.directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1), (0, 1),
                      (1, -1), (1, 0), (1, 1)]

    def get_hidden_neighbors(self, r, c):
        hidden_list = []
        for dr, dc in self.directions:
            nr, nc = r + dr, c + dc

            if 0 <= nr < self.size and 0 <= nc < self.size:
                if not self.board.grid[nr][nc].revealed:
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


