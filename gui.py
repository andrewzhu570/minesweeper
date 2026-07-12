# Andrew Zhu kuh4de
import tkinter as tk
from tkinter import messagebox
import minesweeper as mine
import time

class GUI:
    def __init__(self):
        self.BOARD_SIZE = 8
        self.NUM_MINES = 5
        self.board = mine.Board(self.BOARD_SIZE, self.NUM_MINES)
        self.window = tk.Tk()
        self.window.title("Minesweeper")
        self.buttons = []

        self.start_time = None
        self.time_running = False

        self.mine_counter = tk.Label(
            self.window,
            text=f"Mines: {self.NUM_MINES}\n"
                 f"Flags: {0}",
            font=("Arial", 12)
        )

        self.time_label = tk.Label(
            self.window,
            text=f"Time: {0}",
            font=("Arial", 12)
        )

        self.restart_button = tk.Button(
            self.window,
            text="Restart",
            command=self.restart
        )

        self.menu_bar = tk.Menu(self.window)
        self.game_menu = tk.Menu(self.menu_bar)
        self.game_menu.add_command(
            label="New Game",
            command=self.restart
        )
        self.game_menu.add_command(
            label="Easy",
            command=lambda: self.set_difficulty(8, 10)
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

        self.time_label.grid(row=0, column=0, columnspan=10)
        self.mine_counter.grid(row=0, column=0, columnspan=2)
        self.restart_button.grid(row=0, column=0, columnspan=5)
        self.create_board_widgets()
        self.update_display()

    def click(self, row, col):
        if self.board.first_click:
            if self.board.grid[row][col].has_mine:
                self.board.move_mine(row, col)
                self.board.compute_numbers()
            self.start_time = time.time()
            self.time_running = True
            self.board.first_click = False
            self.update_timer()
        self.board.reveal(row, col)
        self.update_display()

        if self.board.game_over:
            self.time_running = False
            self.reveal_all()
            messagebox.showinfo("Game over.", "Better luck next time.")
            for row in self.buttons:
                for button in row:
                    button.config(state="disabled")
        elif self.board.check_win():
            self.time_running = False
            for row in self.buttons:
                for button in row:
                    button.config(state="disabled")
            messagebox.showinfo("You win!", "Congratulations!")

    def flag(self, row, col):
        cell = self.board.grid[row][col]
        if cell.revealed:
            return
        cell.flagged = not cell.flagged
        self.update_display()

    def restart(self):
        self.destroy_board_widgets()
        self.board = mine.Board(self.BOARD_SIZE, self.NUM_MINES)
        self.create_board_widgets()
        self.update_display()

        for row in self.buttons:
            for button in row:
                button.config(state="normal")

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
                    text = "F"
                elif cell.has_mine:
                    text = "*"
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
                cell = self.board.grid[r][c]

                if cell.flagged:
                    text = "F"
                elif not cell.revealed:
                    text = "."
                elif cell.has_mine:
                    text = "*"
                elif cell.neighbor_mines == 0:
                    text = ""
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
                self.buttons[r][c].config(text=text)

                self.update_mine_counter()

    def set_difficulty(self, size, mines):
        self.BOARD_SIZE = size
        self.NUM_MINES = mines
        self.restart()

    def create_board_widgets(self):
        for r in range(self.board.size):
            row = []

            for c in range(self.board.size):
                button = tk.Button(self.window,
                                   text=".",
                                   width=3,
                                   height=1,
                                   command=lambda r=r, c=c: self.click(r, c))
                button.bind("<Button-2>", lambda event, r=r, c=c: self.flag(r, c))
                button.grid(row=r+1, column=c)

                row.append(button)

            self.buttons.append(row)

    def destroy_board_widgets(self):
        for row in self.buttons:
            for button in row:
                button.destroy()

        self.buttons = []
gui = GUI()
gui.window.mainloop()