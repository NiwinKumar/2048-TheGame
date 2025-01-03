import tkinter as tk
import random
import numpy as np

class Game2048:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("2048")
        self.window.configure(bg='#faf8ef')
        self.score = 0
        self.high_score = 0
        self.grid_cells = []
        self.matrix = np.zeros((4, 4), dtype=int)
        
        # Create score display
        self.score_frame = tk.Frame(self.window, bg='#faf8ef')
        self.score_frame.pack(pady=10)
        
        # Score labels
        self.score_label = tk.Label(
            self.score_frame,
            text=f"Score: {self.score}",
            font=('Arial', 20, 'bold'),
            bg='#bbada0',
            fg='white',
            padx=10,
            pady=5
        )
        self.score_label.pack(side=tk.LEFT, padx=5)
        
        self.high_score_label = tk.Label(
            self.score_frame,
            text=f"Best: {self.high_score}",
            font=('Arial', 20, 'bold'),
            bg='#bbada0',
            fg='white',
            padx=10,
            pady=5
        )
        self.high_score_label.pack(side=tk.LEFT, padx=5)
        
        # New Game button
        self.new_game_btn = tk.Button(
            self.window,
            text="New Game",
            font=('Arial', 12, 'bold'),
            bg='#8f7a66',
            fg='white',
            command=self.reset_game
        )
        self.new_game_btn.pack(pady=10)
        
        self.init_grid()
        self.add_new_tile()
        self.add_new_tile()
        
        # Instructions label
        instructions = "Use arrow keys to move tiles.\nCombine same numbers to reach 2048!"
        self.instructions_label = tk.Label(
            self.window,
            text=instructions,
            font=('Arial', 11),
            bg='#faf8ef',
            fg='#776e65'
        )
        self.instructions_label.pack(pady=10)
        
        # Bind arrow keys and WASD
        self.window.bind("<Left>", lambda event: self.move("left"))
        self.window.bind("<Right>", lambda event: self.move("right"))
        self.window.bind("<Up>", lambda event: self.move("up"))
        self.window.bind("<Down>", lambda event: self.move("down"))
        self.window.bind("a", lambda event: self.move("left"))
        self.window.bind("d", lambda event: self.move("right"))
        self.window.bind("w", lambda event: self.move("up"))
        self.window.bind("s", lambda event: self.move("down"))

    def init_grid(self):
        background = tk.Frame(
            self.window,
            bg='#bbada0',
            width=400,
            height=400
        )
        background.pack(padx=10, pady=10)

        for i in range(4):
            grid_row = []
            for j in range(4):
                cell = tk.Frame(
                    background,
                    bg='#cdc1b4',
                    width=100,
                    height=100
                )
                cell.grid(row=i, column=j, padx=5, pady=5)
                cell.grid_propagate(False)
                cell_number = tk.Label(
                    cell,
                    bg='#cdc1b4',
                    justify=tk.CENTER,
                    font=('Arial', 30, 'bold'),
                    width=4,
                    height=2
                )
                cell_number.place(relx=0.5, rely=0.5, anchor="center")
                grid_row.append(cell_number)
            self.grid_cells.append(grid_row)

    def reset_game(self):
        self.score = 0
        self.score_label.config(text=f"Score: {self.score}")
        self.matrix = np.zeros((4, 4), dtype=int)
        self.add_new_tile()
        self.add_new_tile()
        self.update_grid_cells()

    def add_new_tile(self):
        empty_cells = [(i, j) for i in range(4) for j in range(4) if self.matrix[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.matrix[i][j] = 2 if random.random() < 0.9 else 4
            self.update_grid_cells()

    def update_grid_cells(self):
        for i in range(4):
            for j in range(4):
                new_number = self.matrix[i][j]
                if new_number == 0:
                    self.grid_cells[i][j].configure(
                        text="",
                        bg='#cdc1b4'
                    )
                else:
                    self.grid_cells[i][j].configure(
                        text=str(new_number),
                        bg=self.get_cell_color(new_number),
                        fg=self.get_text_color(new_number)
                    )
        self.window.update_idletasks()

    def get_cell_color(self, number):
        colors = {
            2: '#eee4da',
            4: '#ede0c8',
            8: '#f2b179',
            16: '#f59563',
            32: '#f67c5f',
            64: '#f65e3b',
            128: '#edcf72',
            256: '#edcc61',
            512: '#edc850',
            1024: '#edc53f',
            2048: '#edc22e'
        }
        return colors.get(number, '#3c3a32')

    def get_text_color(self, number):
        return '#f9f6f2' if number >= 8 else '#776e65'

    def stack(self):
        new_matrix = np.zeros((4, 4), dtype=int)
        for i in range(4):
            fill_position = 0
            for j in range(4):
                if self.matrix[i][j] != 0:
                    new_matrix[i][fill_position] = self.matrix[i][j]
                    fill_position += 1
        self.matrix = new_matrix

    def combine(self):
        for i in range(4):
            for j in range(3):
                if self.matrix[i][j] != 0 and self.matrix[i][j] == self.matrix[i][j + 1]:
                    self.matrix[i][j] *= 2
                    self.score += self.matrix[i][j]
                    if self.score > self.high_score:
                        self.high_score = self.score
                        self.high_score_label.config(text=f"Best: {self.high_score}")
                    self.score_label.config(text=f"Score: {self.score}")
                    self.matrix[i][j + 1] = 0

    def reverse(self):
        self.matrix = np.flip(self.matrix, axis=1)

    def transpose(self):
        self.matrix = self.matrix.T

    def move(self, direction):
        original_matrix = self.matrix.copy()
        
        if direction == "left":
            self.stack()
            self.combine()
            self.stack()
        elif direction == "right":
            self.reverse()
            self.stack()
            self.combine()
            self.stack()
            self.reverse()
        elif direction == "up":
            self.transpose()
            self.stack()
            self.combine()
            self.stack()
            self.transpose()
        elif direction == "down":
            self.transpose()
            self.reverse()
            self.stack()
            self.combine()
            self.stack()
            self.reverse()
            self.transpose()

        if not np.array_equal(original_matrix, self.matrix):
            self.add_new_tile()
            
        if self.game_over():
            game_over_window = tk.Toplevel(self.window)
            game_over_window.title("Game Over")
            game_over_window.configure(bg='#faf8ef')
            
            message = f"Game Over!\nFinal Score: {self.score}"
            if self.score == self.high_score:
                message += "\nNew High Score!"
                
            tk.Label(
                game_over_window,
                text=message,
                font=('Arial', 16, 'bold'),
                bg='#faf8ef',
                fg='#776e65',
                pady=20,
                padx=20
            ).pack()
            
            tk.Button(
                game_over_window,
                text="Play Again",
                command=lambda: [game_over_window.destroy(), self.reset_game()],
                font=('Arial', 12, 'bold'),
                bg='#8f7a66',
                fg='white'
            ).pack(pady=(0, 20))

    def game_over(self):
        if 0 in self.matrix:
            return False

        for i in range(4):
            for j in range(3):
                if self.matrix[i][j] == self.matrix[i][j + 1]:
                    return False
        
        for i in range(3):
            for j in range(4):
                if self.matrix[i][j] == self.matrix[i + 1][j]:
                    return False

        return True

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    game = Game2048()
    game.run()

