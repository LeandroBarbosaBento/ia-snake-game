import pygame
import random

class SnakeGame:
    def __init__(self, width=600, height=400, block_size=20):
        pygame.init()
        self.width = width
        self.height = height
        self.block_size = block_size
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Jogo da Cobrinha")
        self.clock = pygame.time.Clock()

        # Colors
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.red = (200, 0, 0)
        self.green = (0, 200, 0)

        # Game state
        self.snake = [[self.width // 2, self.height // 2]]
        self.food = self.generate_food()
        self.direction = "RIGHT"
        self.running = True

    def generate_food(self):
        # Generate food in a random position
        x = random.randint(0, (self.width // self.block_size) - 1) * self.block_size
        y = random.randint(0, (self.height // self.block_size) - 1) * self.block_size
        return [x, y]

    def move_snake(self):
        # Move the snake
        head = self.snake[0][:]
        if self.direction == "UP":
            head[1] -= self.block_size
        elif self.direction == "DOWN":
            head[1] += self.block_size
        elif self.direction == "LEFT":
            head[0] -= self.block_size
        elif self.direction == "RIGHT":
            head[0] += self.block_size

        # Handle colision with walls
        if head[0] < 0 or head[0] >= self.width or head[1] < 0 or head[1] >= self.height:
            self.running = False

        # Handle colision with the snake itself
        if head in self.snake:
            self.running = False

        self.snake.insert(0, head)

        # Generate food
        if head == self.food:
            self.food = self.generate_food()
        else:
            self.snake.pop()

    def render(self):
        self.screen.fill(self.black)
        for segment in self.snake:
            pygame.draw.rect(self.screen, self.green, (*segment, self.block_size, self.block_size))

        pygame.draw.rect(self.screen, self.red, (*self.food, self.block_size, self.block_size))
        pygame.display.update()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and self.direction != "DOWN":
                        self.direction = "UP"
                    elif event.key == pygame.K_DOWN and self.direction != "UP":
                        self.direction = "DOWN"
                    elif event.key == pygame.K_LEFT and self.direction != "RIGHT":
                        self.direction = "LEFT"
                    elif event.key == pygame.K_RIGHT and self.direction != "LEFT":
                        self.direction = "RIGHT"

            self.move_snake()
            self.render()
            self.clock.tick(10)  # Control speed

        pygame.quit()

