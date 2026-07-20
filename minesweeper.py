import random

class Cell:
    def __init__(self):
        self.has_mine = False
        self.revealed = False
        self.flagged = False
        self.neighbor_mines = 0


class Board:
    def __init__(self, size=10, num_mines=10):
        self.size = size
        self.num_mines = num_mines
        self.game_over = False
        self.first_click = True

        self.grid = [[Cell() for _ in range(size)] for _ in range(size)]

        self.place_mines()
        self.compute_numbers()


    def place_mines(self):
        """Randomly chooses cells to place mines until the amount of mines needed is reached"""
        placed = 0
        while placed < self.num_mines:
            r = random.randint(0, self.size - 1)
            c = random.randint(0, self.size - 1)

            cell = self.grid[r][c]

            if not cell.has_mine:
                cell.has_mine = True
                placed += 1

    def count_neighbors(self, r, c):
        """Counts how many neighboring cells have mines"""
        directions = [(-1,-1), (-1,0), (-1,1),
                      (0,-1),         (0,1),
                      (1,-1),  (1,0), (1,1)]
        count = 0
        for dr, dc in directions:
            nr, nc = r + dr, c + dc

            if 0 <= nr < self.size and 0 <= nc < self.size:
                if self.grid[nr][nc].has_mine:
                    count += 1

        return count

    def compute_numbers(self):
        """Assigns the neighbor_mines field of each cell to an integer using count_neighbors()"""
        for r in range(self.size):
            for c in range(self.size):
                if not self.grid[r][c].has_mine:
                    self.grid[r][c].neighbor_mines = self.count_neighbors(r, c)
                else: self.grid[r][c].neighbor_mines = 0

    def reveal(self, r, c):
        """Reveals each cell that is clicked along with neighboring cells touching 0 mines"""
        if not (0 <= r < self.size and 0 <= c < self.size):
            return
        cell = self.grid[r][c]
        if cell.revealed or cell.flagged:
            return
        cell.revealed = True
        if cell.has_mine:
            self.game_over = True
            return
        if cell.neighbor_mines > 0:
            return
        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1), (0, 1),
                      (1, -1), (1, 0), (1, 1)]
        for dr, dc in directions:
            nr, nc = r + dr, c + dc

            if 0 <= nr < self.size and 0 <= nc < self.size:
                self.reveal(nr, nc)

    def display_board(self):
        """Generates the visual of the entire board ONLY FOR TERMINAL VERSION"""
        for row in self.grid:
            display_row = []
            for cell in row:
                if cell.flagged:
                    value = "F"
                elif not cell.revealed:
                    value = "."
                elif cell.has_mine:
                    value = "*"
                elif cell.neighbor_mines == 0:
                    value = " "
                else:
                    value = str(cell.neighbor_mines)
                display_row.append(value)
            print("  ".join(display_row))

    def reveal_all(self):
        """Reveals every cell ONLY FOR TERMINAL VERSION"""
        for row in self.grid:
            display_row = []
            for cell in row:
                if cell.flagged:
                    value = "F"
                elif cell.has_mine:
                    value = "*"
                elif cell.neighbor_mines == 0:
                    value = " "
                else:
                    value = str(cell.neighbor_mines)
                display_row.append(value)
            print("  ".join(display_row))

    def check_win(self):
        for row in self.grid:
            for cell in row:
                if not cell.has_mine and not cell.revealed:
                    return False
        return True

    def move_mine(self, r, c):
        """Ensures first click safety by moving the mine a user clicks on the first move"""
        self.grid[r][c].has_mine = False
        found_space = False
        while not found_space:
            rr = random.randint(0, self.size - 1)
            rc = random.randint(0, self.size - 1)
            if rr == r and rc == c:
                continue
            cell = self.grid[rr][rc]

            if not cell.has_mine:
                cell.has_mine = True
                found_space = True

    def play_game(self):
        """Used only for functionality of the terminal version"""
        while not self.game_over:
            self.display_board()
            command = input("Enter move: (r row col or f row col): ")
            parts = command.split()
            action = parts[0]
            try:
                row = int(parts[1])
                col = int(parts[2])
            except ValueError:
                print("Invalid input!")
                continue
            if not (0 <= row < self.size and 0 <= col < self.size):
                print("Out of range")
                continue

            if action == "r":
                if self.first_click:
                    if self.grid[row][col].has_mine:
                        self.move_mine(row, col)
                        self.compute_numbers()
                    self.first_click = False
                self.reveal(row, col)
            elif action == "f":
                if self.grid[row][col].revealed:
                    continue
                self.grid[row][col].flagged = not self.grid[row][col].flagged
            else:
                print("Unknown command")
            if self.check_win():
                print("You win!")
                self.display_board()
                return
        self.reveal_all()
        print("Game Over!")

if __name__ == "__main__":
    board = Board(5, 5)
    board.play_game()