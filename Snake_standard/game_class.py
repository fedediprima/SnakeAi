import random
import pygame

class Game():
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
        self.speed = 10
        self.status = True
        self.screen = screen

    def move_snake(self, change):
        self.head = tuple(a + b for a, b in zip(self.snake[0], change))
        for i in range(self.len-1, 0, -1):
            self.snake[i] = self.snake[i-1]
        self.snake[0] = self.head
        self.tail = self.snake[-1]

        if self.head == self.food:
            self.score += 100
            self.snake.append(tuple(a - b for a, b in zip(self.tail, change)))
            self.len = len(self.snake)
            self.move_food()
        elif self.head in self.snake[1:-1] or self.head[0] > self.dimension[0] or self.head[0] < self.block or self.head[1] > self.dimension[1] or self.head[1] < self.block:
            self.status = False

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

    def start(self):
        font = pygame.font.Font(None, 30)
        text_surface = font.render("Use the keyboard arrows to move the snake!", True, (128,128,128))
        self.screen.blit(text_surface, (350, self.screen.get_height() - 45))

    def game_interface(self):
        pygame.draw.rect(self.screen, (25,25,25), (20, 20, self.dimension[0], self.dimension[1]))
        pygame.draw.rect(self.screen, (255,255,255), (19, 19, self.dimension[0]+1, self.dimension[1]+1), 1)

    def initial_page(self):
        self.screen.fill((25,25,25))
        font = pygame.font.Font(None, 60)
        text_surface = font.render("SNAKE", True, (255,255,255))
        text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 200))
        self.screen.blit(text_surface, text_rect)
        
        image = pygame.image.load("images/anaconda.png")
        image = pygame.transform.scale(image, (300,300))
        logo_rect = image.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(image, logo_rect)

        font = pygame.font.Font(None, 36)
        text_surface = font.render("Press [ENTER] to start", True, (255,255,255))
        text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 200))
        self.screen.blit(text_surface, text_rect)

    def game_over(self):
        font = pygame.font.Font(None, 100)
        text_surface = font.render("GAME OVER", True, (0,255,0))
        text_rect = text_surface.get_rect(center=(self.dimension[0] // 2, self.dimension[1] // 2))
        self.screen.blit(text_surface, text_rect)
        
        font = pygame.font.Font(None, 36)
        text_surface = font.render(f"Your score: {self.score}", True, (0,255,0))
        text_rect = text_surface.get_rect(center=(self.dimension[0] // 2, self.dimension[1] // 2 + 50))
        self.screen.blit(text_surface, text_rect)

        font = pygame.font.Font(None, 36)
        text_surface = font.render(f"Press [r] to restart", True, (255,255,255))
        text_rect = text_surface.get_rect(center=(self.dimension[0] // 2, self.dimension[1] // 2 + 85))
        self.screen.blit(text_surface, text_rect)
        
            




