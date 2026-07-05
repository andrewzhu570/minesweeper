# Andrew Zhu kuh4de
import tkinter as tk
import minesweeper as mine
class GUI:
    def __init__(self):
        self.board = mine.Board(5, 2)
        self.window = tk.Tk()
        self.window.title("Minesweeper")

        self.buttons = []

        for r in range(self.board.size):
            row = []

            for c in range(self.board.size):
                button = tk.Button(self.window,
                                   text=".",
                                   width=3,
                                   height=1,
                                   command=lambda r=r, c=c: self.click(r, c))
                button.bind("<Button-2>", lambda event, r=r, c=c: self.flag(r, c))
                button.grid(row=r, column=c)

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
        elif self.board.check_win():
            print("You win!")

    def flag(self, row, col):
        cell = self.board.grid[row][col]
        if cell.revealed:
            return
        cell.flagged = not cell.flagged
        self.update_display()

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
                    text = str(cell.neighbor_mines)

                self.buttons[r][c].config(text=text)

gui = GUI()
gui.window.mainloop()