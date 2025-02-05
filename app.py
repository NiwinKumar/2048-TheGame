from flask import Flask, render_template, jsonify, request, session, send_from_directory
import random
import os
app = Flask(__name__)
app.secret_key = 'mysecretkey'

class Game2048:
    def __init__(self):        
        self.grid = [[0 for _ in range(4)] for _ in range(4)]
        self.score = 0
        self.high_score = 0
        self.add_new_tile()
        self.add_new_tile()

    def init_grid(self):
        self.grid = [[0 for _ in range(4)] for _ in range(4)]

    def add_new_tile(self):
        empty_cells = [(i, j) for i in range(4) for j in range(4) if self.grid[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.grid[i][j] = 2 if random.random() < 0.9 else 4

    def stack(self):
        new_grid = [[0 for _ in range(4)] for _ in range(4)]
        for i in range(4):
            fill_position = 0
            for j in range(4):
                if self.grid[i][j] != 0:
                    new_grid[i][fill_position] = self.grid[i][j]
                    fill_position += 1
        self.grid = new_grid

    def combine(self):
        for i in range(4):
            for j in range(3):
                if self.grid[i][j] != 0 and self.grid[i][j] == self.grid[i][j + 1]:
                    self.grid[i][j] *= 2
                    self.score += self.grid[i][j]
                    self.grid[i][j + 1] = 0

    def reverse(self):
        new_grid = []
        for i in range(4):
            new_grid.append([])
            for j in range(4):
                new_grid[i].append(self.grid[i][3 - j])
        self.grid = new_grid

    def transpose(self):
        new_grid = [[0 for _ in range(4)] for _ in range(4)]
        for i in range(4):
            for j in range(4):
                new_grid[i][j] = self.grid[j][i]
        self.grid = new_grid

    def move(self, direction):
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

    def game_over(self):
        for row in self.grid:
            for cell in row:
                if cell == 0:
                    return False

        for i in range(4):
            for j in range(3):
                if self.grid[i][j] == self.grid[i][j + 1]:
                    return False
                if self.grid[j][i] == self.grid[j + 1][i]:
                    return False
        return True

    def update_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score

    def new_game(self):
        self.init_grid()
        self.score = 0
        self.add_new_tile()
        self.add_new_tile()    
    def get_grid(self):
        return self.grid
    
    def get_score(self):
        return self.score

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/<path:filename>')
def serve_static(filename):
    root_dir = os.path.dirname(os.getcwd())
    return send_from_directory(os.path.join(root_dir, 'static'), filename)

@app.route('/move', methods=['POST'])
def move():
    if 'game' not in session:
        session['game'] = Game2048()
    game = session['game']    
    direction = request.json['direction']
    if direction not in ["left","right","up","down"]:
        return jsonify({"error": "Invalid move."}), 400
    
    
    
    game.move(direction)
    game.add_new_tile()
    game.update_high_score()
    return jsonify({
        'grid': game.grid,
        'score': game.score,
        'high_score':game.high_score,
        'game_over': game.game_over()
    })

@app.route('/reset', methods=['POST'])
def reset():
    if 'game' not in session:
        session['game'] = Game2048()
    game = session['game']
    game.new_game()
    return jsonify({'board': game.get_grid(), 'score': game.get_score()})




import tkinter as tk
import random
import numpy as np
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

class Game2048:
    def __init__(self):
        self.score = 0
        self.high_score = 0
        self.matrix = np.zeros((4, 4), dtype=int)
        self.add_new_tile()
        self.add_new_tile()

    def reset_game(self):
        self.score = 0
        self.matrix = np.zeros((4, 4), dtype=int)
        self.add_new_tile()
        self.add_new_tile()

    def add_new_tile(self):
        empty_cells = [(i, j) for i in range(4) for j in range(4) if self.matrix[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.matrix[i][j] = 2 if random.random() < 0.9 else 4

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

game = Game2048()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/reset', methods=['POST'])
def reset():
    game.reset_game()
    return jsonify({'board': game.matrix.tolist(), 'score': game.score, 'high_score': game.high_score, 'game_over': game.game_over()})

@app.route('/move', methods=['POST'])
def move():
    data = request.get_json()
    direction = data['direction']
    game.move(direction)
    return jsonify({'board': game.matrix.tolist(), 'score': game.score, 'high_score': game.high_score, 'game_over': game.game_over()})

if __name__ == '__main__':
    app.run(debug=True)
