import pickle
import pygame
import numpy as np
from q_learning_snake import SnakeGameQLearning

# Carregar a tabela Q treinada
with open("q_table.pkl", "rb") as f:
    q_table = pickle.load(f)

# Inicializar o jogo
game = SnakeGameQLearning()
state = game.reset()
running = True

while running:
    game.render()  # Renderiza o jogo
    pygame.time.delay(100)  # Ajusta a velocidade do jogo

    if state in q_table:
        action = np.argmax(q_table[state])  # Escolhe a melhor ação aprendida
    else:
        action = np.random.randint(0, len(game.actions))  # Caso falte um estado, faz um movimento aleatório

    next_state, _, done = game.step(action)
    state = next_state

    if done:
        running = False

pygame.quit()
print("Jogo finalizado!")
