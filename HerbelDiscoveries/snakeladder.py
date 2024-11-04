import tkinter as tk
import random

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game")

        self.canvas = tk.Canvas(root, width=600, height=600, bg="black")
        self.canvas.pack()

        self.snake = [(100, 100), (90, 100), (80, 100)]
        self.snake_dir = "Right"
        self.food = self.create_food()
        self.score = 0
        self.game_over = False

        self.score_label = tk.Label(root, text=f"Score: {self.score}", font=("Helvetica", 16))
        self.score_label.pack()

        self.root.bind("<KeyPress>", self.change_direction)

        self.run_game()

    def run_game(self):
        if not self.game_over:
            self.move_snake()
            self.check_collisions()
            self.update_canvas()
            if self.game_over:
                self.canvas.create_text(300, 300, text="GAME OVER", fill="red", font=("Helvetica", 32))
            else:
                self.root.after(100, self.run_game)

    def create_food(self):
        x = random.randint(0, 59) * 10
        y = random.randint(0, 59) * 10
        while (x, y) in self.snake:
            x = random.randint(0, 59) * 10
            y = random.randint(0, 59) * 10
        return (x, y)

    def move_snake(self):
        head_x, head_y = self.snake[0]
        if self.snake_dir == "Right":
            head_x += 10
        elif self.snake_dir == "Left":
            head_x -= 10
        elif self.snake_dir == "Up":
            head_y -= 10
        elif self.snake_dir == "Down":
            head_y += 10

        new_head = (head_x, head_y)
        self.snake = [new_head] + self.snake[:-1]

        if self.snake[0] == self.food:
            self.snake.append(self.snake[-1])
            self.food = self.create_food()
            self.score += 1
            self.score_label.config(text=f"Score: {self.score}")

    def check_collisions(self):
        head_x, head_y = self.snake[0]
        # Check if the snake hits the border
        if head_x < 0 or head_x >= 600 or head_y < 0 or head_y >= 600:
            self.game_over = True
        # Check if the snake collides with itself
        if len(self.snake) != len(set(self.snake)):
            self.game_over = False

    def change_direction(self, event):
        new_dir = event.keysym
        all_dirs = {"Right", "Left", "Up", "Down"}
        opposites = {("Right", "Left"), ("Left", "Right"), ("Up", "Down"), ("Down", "Up")}
        if new_dir in all_dirs and (self.snake_dir, new_dir) not in opposites:
            self.snake_dir = new_dir

    def update_canvas(self):
        self.canvas.delete(tk.ALL)
        self.canvas.create_rectangle(self.food[0], self.food[1], self.food[0] + 10, self.food[1] + 10, fill="red")
        for x, y in self.snake:
            self.canvas.create_rectangle(x, y, x + 10, y + 10, fill="green")


if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
