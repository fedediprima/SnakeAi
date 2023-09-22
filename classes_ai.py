import random
import pygame
import torch
import numpy as np
from model import Qnet, Qtrainer
import math

class Game():##
    def __init__(self, dimension, block, screen):
        self.score = 0
        self.block = block
        self.dimension = dimension
        self.food = (random.choice(range(20,self.dimension[0]-self.block+1, self.block)), random.choice(range(20,self.dimension[1]-self.block+1, self.block)))
        #print(self.food)
        self.snake = [(dimension[0]//2, dimension[1]//2)]
        self.head = self.snake[0]
        self.tail = self.snake[-1]
        self.len = len(self.snake)
        self.speed = 50
        self.status = True
        self.screen = screen
        self.direction = (0,0)
        self.previous_position = self.head

    def reset(self):
        self.food = (random.choice(range(20,self.dimension[0]-self.block+1, self.block)), random.choice(range(20,self.dimension[1]-self.block+1, self.block)))
        self.score = 0
        self.snake = [(self.dimension[0]//2, self.dimension[1]//2)]
        self.head = self.snake[0]
        self.tail = self.snake[-1]
        self.len = len(self.snake)
        self.status = True
        self.direction = (0,0)

    def is_collision(self, point):
        if point in self.snake[1:-1] or point[0] > self.dimension[0] or point[0] < self.block or point[1] > self.dimension[1] or point[1] < self.block:
            return True
        else:
            return False
        
    def move_snake(self, change):
        reward = 0
        # penalizzo se continua a cambiare mossa
        if change == self.direction:
            reward += 2

        self.direction = change
        self.head = tuple(a + b for a, b in zip(self.snake[0], self.direction))
        for i in range(self.len-1, 0, -1):
            self.snake[i] = self.snake[i-1]
        self.snake[0] = self.head
        self.tail = self.snake[-1]
        # small reward if getting closer to the food
        previous_distance = math.sqrt((self.food[0] - self.previous_position[0])**2 + (self.food[1] - self.previous_position[1])**2)
        current_distance = math.sqrt((self.food[0] - self.head[0])**2 + (self.food[1] - self.head[1])**2)
        self.previous_position = self.head
        if current_distance < previous_distance:
            reward += 10
        #if self.direction != (0,0):
            #self.score += 1
        if self.head == self.food:
            self.score += 100
            self.snake.append(tuple(a - b for a, b in zip(self.tail, self.direction)))
            self.len = len(self.snake)
            self.move_food()
            reward += 20
        # si schianta
        elif self.is_collision(self.head):
            self.status = False
            reward -= 100

        return reward
        # self.next_direction = predict(stato)

    def move_food(self):
        self.food = (random.choice(range(20,self.dimension[0]-self.block+1, self.block)), random.choice(range(20,self.dimension[1]-self.block+1, self.block)))
        while self.food in self.snake:
            self.food = (random.choice(range(20,self.dimension[0]-self.block+1, self.block)), random.choice(range(20,self.dimension[1]-self.block+1, self.block)))

    def draw_snake(self):
        for square in self.snake:
            pygame.draw.rect(self.screen, (0,255,0), (square[0], square[1], self.block, self.block))
            pygame.draw.rect(self.screen, (0,150,0), (square[0]+2, square[1]+2, self.block-4, self.block-4))
    
    def draw_food(self):
        pygame.draw.rect(self.screen, (255,0,0), (self.food[0], self.food[1], self.block, self.block))
        pygame.draw.rect(self.screen, (150,0,0), (self.food[0]+2, self.food[1]+2, self.block-4, self.block-4))

    def print_score(self):
        font = pygame.font.Font(None, 30)
        text_surface = font.render(f"Score: {self.score}", True, (128,128,128))
        self.screen.blit(text_surface, (35, self.screen.get_height() - 45))

    def game_interface(self):
        pygame.draw.rect(self.screen, (25,25,25), (20, 20, self.dimension[0], self.dimension[1]))
        pygame.draw.rect(self.screen, (255,255,255), (19, 19, self.dimension[0]+1, self.dimension[1]+1), 1)


class Agent():
    def __init__(self):
        self.cont = 0 
        self.epsilon = 0 # for random moves
        self.batch_size = 1000
        self.memory = []
        self.gamma = 0.9 # discount rate
        self.n_games = 0
        self.model = Qnet(12, 256, 3)
        self.trainer = Qtrainer(model = self.model, lr = 0.001, gamma = self.gamma)
    
    def get_state(self, game):
        self.cont +=1
        if self.cont % 1000==0:
            print(self.cont)
        head = game.head
        food = game.food
        point_left = (head[0]-game.block, game.head[1])
        point_right = (head[0]+game.block, game.head[1])
        point_up = (head[0], game.head[1]-game.block)
        point_down = (head[0], game.head[1]+game.block)
        direction_left = game.direction == (-game.block, 0)
        direction_right = game.direction == (game.block, 0)
        direction_up = game.direction == (0, -game.block)
        direction_down = game.direction == (0, game.block)
        food_left = head[0] > food[0]
        food_right = head[0] < food[0]
        food_up = head[1] > food[1]
        food_down = head[1] < food[1]
        state = [
            direction_left,
            direction_right,
            direction_up,
            direction_down,
            # danger left
            game.is_collision(point_left),
            # danger right
            game.is_collision(point_right),
            # danger down
            game.is_collision(point_down),
            # danger up
            game.is_collision(point_up),

            # food
            food_left, 
            food_right,
            food_up,
            food_down
        ]

        return state
    
    def update_memory(self, state, action, reward, next, game_over):
        self.memory.append((state, action, reward, next, game_over))
        
    
    def get_action(self, state):
        # trade off / exploration exploitation
        self.epsilon = 50 - self.n_games
        final_move = [0,0,0]
        # random moves
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move

    def train_short_memory(self, state, action, reward, next, game_over):
        self.trainer.train_step(state, action, reward, next, game_over)

    def train_long_memory(self):
        if len(self.memory) > self.batch_size:
            sample = random.sample(self.memory, self.batch_size)
            states, actions, rewards, next_states, game_overs = zip(*sample)
        else:
            states, actions, rewards, next_states, game_overs = zip(*self.memory)

        self.trainer.train_step(states, actions, rewards, next_states, game_overs)
        






        
            




