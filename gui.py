import tkinter as tk
from game_logic import SnakeGame, EASY_SPEED, MEDIUM_SPEED, HARD_SPEED
from constants import *


class SnakeGUI:
    def __init__(self):
        self.game = SnakeGame()
        self.setup_buttons()

    def setup_buttons(self):
        easy_button = tk.Button(self.game.button_frame, text="Easy", command=self.start_easy_game, font=BUTTON_FONT,
                                bg=BUTTON_COLORS["start"], fg="white", relief=tk.FLAT, bd=0)
        easy_button.pack(side=tk.RIGHT, padx=10)

        medium_button = tk.Button(self.game.button_frame, text="Medium", command=self.start_medium_game, font=BUTTON_FONT,
                                  bg=BUTTON_COLORS["start"], fg="white", relief=tk.FLAT, bd=0)
        medium_button.pack(side=tk.RIGHT, padx=10)

        hard_button = tk.Button(self.game.button_frame, text="Hard", command=self.start_hard_game, font=BUTTON_FONT,
                                bg=BUTTON_COLORS["start"], fg="white", relief=tk.FLAT, bd=0)
        hard_button.pack(side=tk.RIGHT, padx=10)

    def start_easy_game(self):
        self.game.start_game(EASY_SPEED)

    def start_medium_game(self):
        self.game.start_game(MEDIUM_SPEED)

    def start_hard_game(self):
        self.game.start_game(HARD_SPEED)

    def run(self):
        self.game.mainloop()
