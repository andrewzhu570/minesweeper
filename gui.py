# Andrew Zhu kuh4de
import tkinter as tk
from tkinter import messagebox
import minesweeper as mine
class GUI:
    def __init__(self):
        self.BOARD_SIZE = 8
        self.NUM_MINES = 5
        self.board = mine.Board(self.BOARD_SIZE, self.NUM_MINES)
        self.window = tk.Tk()
        self.window.title("Minesweeper")

        self.buttons = []
        self.restart_button = tk.Button(
            self.window,
            text="Restart",
            command=self.restart
        )
        self.restart_button.grid(row=0, column=0, columnspan=self.board.size)
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
        self.update_display()

    def click(self, row, col):
        if self.board.first_click:
            if self.board.grid[row][col].has_mine:
                self.board.move_mine(row, col)
                self.board.compute_numbers()
            self.board.first_click = False
        self.board.reveal(row, col)
        self.update_display()

        if self.board.game_over:
            self.reveal_all()
            messagebox.showinfo("Game over.", "Better luck next time.")
            for row in self.buttons:
                for button in row:
                    button.config(state="disabled")
        elif self.board.check_win():
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
        self.board = mine.Board(self.BOARD_SIZE, self.NUM_MINES)
        self.update_display()

        for row in self.buttons:
            for button in row:
                button.config(state="normal")

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

gui = GUI()
gui.window.mainloop()