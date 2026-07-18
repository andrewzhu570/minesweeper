import tkinter as tk
from tkinter import messagebox
import minesweeper as mine
import time
import solver

class GUI:
    def __init__(self):
        self.BOARD_SIZE = 8
        self.NUM_MINES = 7
        self.board = mine.Board(self.BOARD_SIZE, self.NUM_MINES)
        self.solver = solver.Solver(self.board)
        self.window = tk.Tk()
        self.window.title("Minesweeper")
        self.buttons = []

        self.start_time = None
        self.time_running = False

        self.top_frame = tk.Frame(self.window)
        self.top_frame.grid(row=0, column=0, columnspan=self.BOARD_SIZE, sticky="ew")

        self.mine_counter = tk.Label(
            self.top_frame,
            text=f"Mines: {self.NUM_MINES}\n"
                 f"Flags: {0}",
            font=("Arial", 12)
        )

        self.difficulty_label = tk.Label(
            self.top_frame,
            text=f"Easy",
            font=("Arial", 12)
        )

        self.time_label = tk.Label(
            self.top_frame,
            text=f"Time: {0}",
            font=("Arial", 12)
        )

        self.solve_step_button = tk.Button(
            self.top_frame,
            text="Solve Step",
            command=self.solve_step
        )

        self.solve_all_button = tk.Button(
            self.top_frame,
            text="Solve All",
            command=self.solve_all
        )

        self.menu_bar = tk.Menu(self.window)
        self.game_menu = tk.Menu(self.menu_bar)
        self.game_menu.add_command(
            label="New Game",
            command=self.restart
        )
        self.game_menu.add_command(
            label="Easy",
            command=lambda: self.set_difficulty(8, 7)
        )
        self.game_menu.add_command(
            label="Intermediate",
            command=lambda: self.set_difficulty(14, 25)
        )
        self.game_menu.add_command(
            label="Advanced",
            command=lambda: self.set_difficulty(20, 60)
        )
        self.menu_bar.add_cascade(
            label="Game",
            menu=self.game_menu
        )

        self.window.config(menu=self.menu_bar)



        self.mine_counter.grid(in_=self.top_frame, row=0, column=0, padx=5)
        self.difficulty_label.grid(in_=self.top_frame, row=0, column=1, padx=5)
        self.time_label.grid(in_=self.top_frame, row=0, column=2, padx=5)
        self.solve_step_button.grid(in_=self.top_frame, row=0, column=3, padx=5)
        self.solve_all_button.grid(row=0, column=4, padx=5)

        self.create_board_widgets()
        self.update_display()

    def click(self, row, col):
        cell = self.board.grid[row][col]
        if cell.flagged:
            return

        if self.board.first_click:
            if cell.has_mine:
                self.board.move_mine(row, col)
                self.board.compute_numbers()
            self.start_time = time.time()
            self.time_running = True
            self.board.first_click = False
            self.update_timer()

        if cell.revealed:
            if self.get_adjacent_flags(row, col) == cell.neighbor_mines:
                self.chord(row, col)
        else:
            self.board.reveal(row, col)

        self.update_display()

        if self.board.game_over:
            self.time_running = False
            self.reveal_all()
            self.window.after(
                500,
                lambda: messagebox.showinfo("Game over.", "Better luck next time.")
            )

            for row in self.buttons:
                for button in row:
                    button.config(state="disabled")

        elif self.board.check_win():
            self.game_won()

    def game_won(self):
        self.time_running = False
        for row in self.buttons:
            for button in row:
                button.config(state="disabled")
        self.window.after(
            500,
            lambda: messagebox.showinfo("You win!", "Congratulations!")
        )

    def flag(self, row, col):
        cell = self.board.grid[row][col]

        if cell.revealed:
            return

        flag_count = sum(
            cell.flagged
            for row in self.board.grid
            for cell in row
        )

        if not cell.flagged and flag_count >= self.NUM_MINES:
            return

        cell.flagged = not cell.flagged
        self.update_display()

    def restart(self):
        self.destroy_board_widgets()
        self.board = mine.Board(self.BOARD_SIZE, self.NUM_MINES)
        self.solver = solver.Solver(self.board)
        self.create_board_widgets()
        self.update_display()

        for row in self.buttons:
            for button in row:
                button.config(state="normal")

        self.start_time = None
        self.time_running = False
        self.time_label.config(text="Time: 0")

    def update_timer(self):
        if not self.time_running:
            return
        elapsed = int(time.time() - self.start_time)
        self.time_label.config(text=f"Time: {elapsed}")
        self.window.after(1000, self.update_timer)

    def reveal_all(self):
        for r in range(self.board.size):
            for c in range(self.board.size):
                cell = self.board.grid[r][c]

                if cell.flagged:
                    text = "🚩"
                elif cell.has_mine:
                    text = "💥"
                elif cell.neighbor_mines == 0:
                    text = ""
                else:
                    text = str(cell.neighbor_mines)
                self.buttons[r][c].config(text=text)

    def update_mine_counter(self):
        flag_count = 0
        for row in self.board.grid:
            for cell in row:
                if cell.flagged:
                    flag_count += 1
        self.mine_counter.config(text=f"Mines: {self.NUM_MINES}\n"
                                      f"Flags: {flag_count}")

    def update_display(self):
        for r in range(self.board.size):
            for c in range(self.board.size):
                text = self.get_cell_text(r, c)
                self.buttons[r][c].config(text=text)

        self.update_mine_counter()

    def set_difficulty(self, size, mines):
        self.BOARD_SIZE = size
        self.NUM_MINES = mines
        self.restart()
        if mines == 7:
            self.difficulty_label.config(text="Easy")
        elif mines == 25:
            self.difficulty_label.config(text="Intermediate")
        else:
            self.difficulty_label.config(text="Advanced")

    def create_board_widgets(self):
        for r in range(self.board.size):
            row = []

            for c in range(self.board.size):
                button = tk.Button(self.window,
                                   text=".",
                                   width=1,
                                   height=1,
                                   command=lambda r=r, c=c: self.click(r, c))
                button.bind("<Button-2>", lambda event, r=r, c=c: self.flag(r, c))
                button.bind("<Button-3>", lambda event, r=r, c=c: self.flag(r, c))
                button.grid(row=r+1, column=c)

                row.append(button)

            self.buttons.append(row)

    def destroy_board_widgets(self):
        for row in self.buttons:
            for button in row:
                button.destroy()

        self.buttons = []

    def get_cell_text(self, r, c):
        cell = self.board.grid[r][c]
        if cell.flagged:
            text = "🚩"
        elif not cell.revealed:
            text = ""
        elif cell.has_mine:
            text = "💥"
        elif cell.neighbor_mines == 0:
            text = ""
            self.buttons[r][c].config(
                state="disabled"
            )
        else:
            colors = {
                1: "blue",
                2: "green",
                3: "red",
                4: "#000080",
                5: "brown",
                6: "#008080",
                7: "black",
                8: "gray"
            }
            text = cell.neighbor_mines
            if cell.neighbor_mines > 0:
                self.buttons[r][c].config(
                    fg=colors[cell.neighbor_mines]
                )
        return text

    def get_adjacent_flags(self, r, c):
        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1), (0, 1),
                      (1, -1), (1, 0), (1, 1)]
        count = 0
        for dr, dc in directions:
            nr, nc = r + dr, c + dc

            if 0 <= nr < self.board.size and 0 <= nc < self.board.size:
                if self.board.grid[nr][nc].flagged:
                    count += 1

        return count

    def chord(self, r, c):
        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1), (0, 1),
                      (1, -1), (1, 0), (1, 1)]
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.board.size and 0 <= nc < self.board.size:
                new_cell = self.board.grid[nr][nc]
                if not new_cell.revealed and not new_cell.flagged:
                    self.board.reveal(nr, nc)
                    if self.board.game_over:
                        return

    def auto_flag(self):
        flags_added = 0
        mine_moves = self.solver.find_mines()
        for r, c in mine_moves:
            self.board.grid[r][c].flagged = True
            flags_added += 1

        return flags_added > 0

    def auto_reveal(self):
        cells_revealed = 0
        safe_moves = self.solver.find_safe_moves()
        for r, c in safe_moves:
            self.board.grid[r][c].revealed = True
            cells_revealed += 1

        return cells_revealed > 0

    def auto_subset_solve(self):
        changed = False

        safe_moves, mine_moves = self.solver.find_subset_moves()

        for r, c in mine_moves:
            if not self.board.grid[r][c].flagged:
                self.board.grid[r][c].flagged = True
                changed = True

        for r, c in safe_moves:
            if not self.board.grid[r][c].revealed:
                self.board.grid[r][c].revealed = True
                changed = True

        return changed


    def solve_step(self):
        changed = False

        if self.auto_flag():
            changed = True

        if self.auto_reveal():
            changed = True

        if not changed:
            if self.auto_subset_solve():
                changed = True

        self.update_display()
        if self.board.check_win():
            self.game_won()
        return changed

    def solve_all(self):
        if self.board.check_win():
            self.game_won()
            return
        progress = self.solve_step()
        if not progress:
            return
        else:
            self.window.after(500, self.solve_all)



gui = GUI()
gui.window.mainloop()