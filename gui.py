# gui.py

import tkinter as tk
from game_logic import SnakeGame

class SnakeGUI:
    def __init__(self):
        self.game = SnakeGame()
    
    def run(self):
        self.game.mainloop()
