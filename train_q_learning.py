from q_learning_snake import SnakeGameQLearning
import numpy as np
import random
import pickle

# Hiperparâmetros
alpha = 0.1   # Taxa de aprendizado
gamma = 0.9   # Fator de desconto
epsilon = 1.0 # Exploração inicial
epsilon_decay = 0.995
min_epsilon = 0.01
num_episodes = 500000

# Inicializa Q-Table
q_table = {}

game = SnakeGameQLearning()

for episode in range(num_episodes):
    state = game.reset()
    done = False
    total_reward = 0

    while not done:
        if state not in q_table:
            q_table[state] = np.zeros(len(game.actions))

        if random.uniform(0, 1) < epsilon:
            action = random.randint(0, len(game.actions) - 1)
        else:
            action = np.argmax(q_table[state])

        next_state, reward, done = game.step(action)

        if next_state not in q_table:
            q_table[next_state] = np.zeros(len(game.actions))

        q_table[state][action] = q_table[state][action] + alpha * (
            reward + gamma * np.max(q_table[next_state]) - q_table[state][action]
        )

        state = next_state
        total_reward += reward

    epsilon = max(min_epsilon, epsilon * epsilon_decay)

    if episode % 500 == 0:
        print(f"Episode {episode}, Score: {game.score}, Epsilon: {epsilon:.4f}")

print("Treinamento concluído!")

# Salvar a tabela Q em um arquivo
with open("q_table.pkl", "wb") as f:
    pickle.dump(q_table, f)

print("Tabela Q salva!")
