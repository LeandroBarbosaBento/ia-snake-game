import numpy as np
import random
import pygame

class SnakeGameQLearning:
    def __init__(self, width=400, height=400, block_size=20):
        pygame.init()
        self.width = width
        self.height = height
        self.block_size = block_size
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Q-Learning Snake")
        self.clock = pygame.time.Clock()

        # Cores
        self.black = (0, 0, 0)
        self.green = (0, 255, 0)
        self.red = (255, 0, 0)

        # Movimentos possíveis: [cima, baixo, esquerda, direita]
        self.actions = ["UP", "DOWN", "LEFT", "RIGHT"]
        self.reset()

    def reset(self):
        """Reinicia o jogo para um novo episódio"""
        self.snake = [[self.width // 2, self.height // 2]]
        self.food = self.generate_food()
        self.direction = "RIGHT"
        self.score = 0
        return self.get_state()

    def generate_food(self):
        """Gera comida em uma posição aleatória"""
        x = random.randint(0, (self.width // self.block_size) - 1) * self.block_size
        y = random.randint(0, (self.height // self.block_size) - 1) * self.block_size
        return [x, y]

    def get_state(self):
        """Retorna o estado atual como um vetor de informações"""
        head_x, head_y = self.snake[0]
        food_x, food_y = self.food
        
        # Direção da comida em relação à cobra
        food_dir = [
            food_x < head_x,  # Comida à esquerda
            food_x > head_x,  # Comida à direita
            food_y < head_y,  # Comida acima
            food_y > head_y,  # Comida abaixo
        ]

        # Perigo iminente (colisão se mover para frente, esquerda ou direita)
        danger = [
            self.check_collision(self.snake[0], self.direction),  # Frente
            self.check_collision(self.snake[0], self.get_left()),  # Esquerda
            self.check_collision(self.snake[0], self.get_right())   # Direita
        ]

        return tuple(food_dir + danger)

    def check_collision(self, head, direction):
        """Verifica se haverá colisão ao se mover em uma direção"""
        x, y = head
        if direction == "UP":
            y -= self.block_size
        elif direction == "DOWN":
            y += self.block_size
        elif direction == "LEFT":
            x -= self.block_size
        elif direction == "RIGHT":
            x += self.block_size

        return x < 0 or x >= self.width or y < 0 or y >= self.height or [x, y] in self.snake

    def get_left(self):
        """Retorna a direção à esquerda da atual"""
        return {"UP": "LEFT", "LEFT": "DOWN", "DOWN": "RIGHT", "RIGHT": "UP"}[self.direction]

    def get_right(self):
        """Retorna a direção à direita da atual"""
        return {"UP": "RIGHT", "RIGHT": "DOWN", "DOWN": "LEFT", "LEFT": "UP"}[self.direction]

    def step(self, action):
        """Executa uma ação e retorna o novo estado, a recompensa e se o jogo terminou"""
        self.direction = self.actions[action]
        head = self.snake[0][:]
        
        if self.direction == "UP":
            head[1] -= self.block_size
        elif self.direction == "DOWN":
            head[1] += self.block_size
        elif self.direction == "LEFT":
            head[0] -= self.block_size
        elif self.direction == "RIGHT":
            head[0] += self.block_size
        
        if head in self.snake or head[0] < 0 or head[1] < 0 or head[0] >= self.width or head[1] >= self.height:
            return self.get_state(), -10, True  # Penalidade por morrer

        self.snake.insert(0, head)

        if head == self.food:
            self.food = self.generate_food()
            self.score += 1
            reward = 10  # Recompensa por comer
        else:
            self.snake.pop()
            reward = 0  # Nenhuma recompensa por um movimento normal

        return self.get_state(), reward, False

    def render(self):
        """Desenha o jogo na tela"""
        self.screen.fill(self.black)

        # Desenha a cobra
        for segment in self.snake:
            pygame.draw.rect(self.screen, self.green, pygame.Rect(segment[0], segment[1], self.block_size, self.block_size))

        # Desenha a comida
        pygame.draw.rect(self.screen, self.red, pygame.Rect(self.food[0], self.food[1], self.block_size, self.block_size))

        pygame.display.flip()
        self.clock.tick(10)  # Ajusta a velocidade do jogo

