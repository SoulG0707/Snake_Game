import random
import os
import tkinter as tk
from constants import *


class SnakeGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Snake Game")
        self.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        self.configure(bg=BACKGROUND_COLOR)

        self.canvas = tk.Canvas(self, bg="#E0E0E0", highlightthickness=0)
        self.canvas.place(x=10, y=10, width=SCREEN_WIDTH -
                          20, height=SCREEN_HEIGHT-100)
        self.canvas.create_rectangle(
            0, 0, SCREEN_WIDTH - 20, SCREEN_HEIGHT - 100, outline=BORDER_COLOR, width=2)

        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.direction = "Right"
        self.food = None
        self.score = 0
        self.high_score = self.load_high_score()
        self.game_running = False
        self.paused = False
        self.speed = MEDIUM_SPEED  # Default speed

        self.score_label = tk.Label(
            self, text="", font=SCORE_FONT, bg=BACKGROUND_COLOR, fg="black")
        self.score_label.place(x=10, y=SCREEN_HEIGHT-85)

        self.high_score_label = tk.Label(self, text=f"High Score: {
                                         self.high_score}", font=HIGH_SCORE_FONT, bg=BACKGROUND_COLOR, fg="black")
        self.high_score_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.button_frame = tk.Frame(self, bg=BACKGROUND_COLOR)
        self.button_frame.place(x=10, y=SCREEN_HEIGHT -
                                50, width=SCREEN_WIDTH-20)

        self.start_button = tk.Button(self.button_frame, text="Start", font=BUTTON_FONT, command=self.start_game,
                                      bg=BUTTON_COLORS["start"], fg="white", relief=tk.FLAT, bd=0)
        self.start_button.pack(side=tk.LEFT, padx=10)

        self.stop_button = tk.Button(self.button_frame, text="Stop", font=BUTTON_FONT, command=self.stop_game,
                                     bg=BUTTON_COLORS["stop"], fg="white", relief=tk.FLAT, state=tk.DISABLED, bd=0)
        self.stop_button.pack(side=tk.LEFT, padx=10)

        self.reset_button = tk.Button(self.button_frame, text="Reset", font=BUTTON_FONT, command=self.reset_game,
                                      bg=BUTTON_COLORS["start"], fg="white", relief=tk.FLAT, state=tk.DISABLED, bd=0)
        self.reset_button.pack(side=tk.LEFT, padx=10)

        self.quit_button = tk.Button(self.button_frame, text="Quit", font=BUTTON_FONT, command=self.quit_game,
                                     bg=BUTTON_COLORS["quit"], fg="white", relief=tk.FLAT, bd=0)
        self.quit_button.pack(side=tk.LEFT, padx=10)

        self.bind("<KeyPress>", self.change_direction)

    def start_game(self, speed=MEDIUM_SPEED):
        if not self.game_running:
            self.speed = speed  # Set the speed
            self.game_running = True
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.quit_button.config(state=tk.DISABLED)
            self.reset_button.config(state=tk.NORMAL)
            self.high_score_label.place_forget()
            self.reset_game()
            self.move_snake()

    def stop_game(self):
        self.paused = not self.paused
        if self.paused:
            self.stop_button.config(text="Resume", bg=BUTTON_COLORS["start"])
            self.quit_button.config(state=tk.NORMAL)
        else:
            self.stop_button.config(text="Stop", bg=BUTTON_COLORS["stop"])
            self.quit_button.config(state=tk.DISABLED)
            self.move_snake()

    def quit_game(self):
        self.save_high_score()
        self.destroy()

    def reset_game(self):
        self.score = 0
        self.direction = "Right"
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.canvas.delete(tk.ALL)
        self.create_food()
        self.update_score()
        self.update_high_score()
        self.move_snake()  # Restart the snake movement after resetting

    def create_food(self):
        while True:
            x = random.randint(
                1, (SCREEN_WIDTH - CELL_SIZE - 20) // CELL_SIZE) * CELL_SIZE
            y = random.randint(
                1, (SCREEN_HEIGHT - CELL_SIZE - 100) // CELL_SIZE) * CELL_SIZE
            if (x, y) not in self.snake:
                self.food = self.canvas.create_oval(
                    x, y, x + CELL_SIZE, y + CELL_SIZE, fill=FOOD_COLOR, tags="food")
                break

    def change_direction(self, event):
        key = event.keysym
        if key in ["Up", "Down", "Left", "Right"]:
            if (key == "Up" and self.direction != "Down" or
                key == "Down" and self.direction != "Up" or
                key == "Left" and self.direction != "Right" or
                    key == "Right" and self.direction != "Left"):
                self.direction = key

    def move_snake(self):
        if self.game_running and not self.paused:
            head_x, head_y = self.snake[0]
            if self.direction == "Up":
                new_head = (head_x, head_y - CELL_SIZE)
            elif self.direction == "Down":
                new_head = (head_x, head_y + CELL_SIZE)
            elif self.direction == "Left":
                new_head = (head_x - CELL_SIZE, head_y)
            elif self.direction == "Right":
                new_head = (head_x + CELL_SIZE, head_y)

            self.snake.insert(0, new_head)
            if (self.canvas.coords(self.food)[0], self.canvas.coords(self.food)[1]) == new_head:
                self.canvas.delete("food")
                self.create_food()
                self.score += 1
                self.update_score()
                self.update_high_score()
            else:
                self.canvas.delete(self.snake.pop())

            if (new_head[0] < 0 or new_head[0] >= SCREEN_WIDTH - 20 or
                new_head[1] < 0 or new_head[1] >= SCREEN_HEIGHT - 100 or
                    new_head in self.snake[1:]):
                self.game_over()
                return

            self.update_snake()
            self.after(self.speed, self.move_snake)

    def update_snake(self):
        self.canvas.delete("snake")
        for i, (x, y) in enumerate(self.snake):
            color = SNAKE_HEAD_COLOR if i == 0 else SNAKE_BODY_COLOR
            self.canvas.create_rectangle(
                x, y, x + CELL_SIZE, y + CELL_SIZE, fill=color, tags="snake")

    def update_score(self):
        self.score_label.config(text=f"Score: {self.score}")

    def update_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()
        if not self.game_running:
            self.high_score_label.config(text=f"High Score: {self.high_score}")

    def load_high_score(self):
        if os.path.exists("high_score.txt"):
            with open("high_score.txt", "r") as file:
                return int(file.read())
        return 0

    def save_high_score(self):
        with open("high_score.txt", "w") as file:
            file.write(str(self.high_score))

    def game_over(self):
        self.game_running = False
        self.canvas.delete(tk.ALL)
        self.canvas.create_text(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                text=f"Game Over! Score: {self.score}", fill="black", font=GAME_OVER_FONT)
        self.start_button.config(state=tk.NORMAL)
        self.quit_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.reset_button.config(state=tk.DISABLED)
        self.high_score_label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
