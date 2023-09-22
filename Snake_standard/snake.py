import pygame
from game_class import Game

# Initialize pygame
pygame.init()

# constants
DISPLAY_DIMENSION = (800,600)
GAME_DIMENSION = (760,520)
BLACK = (0,0,0)
GRAY = (128,128,128)
RED = (255,0,0)
DARK_GREY = (25,25,25)
BLOCK = 20

# Create the window
screen = pygame.display.set_mode(DISPLAY_DIMENSION)

# Title and Icon
pygame.display.set_caption("SNAKE")
icon = pygame.image.load("images/anaconda.png")
pygame.display.set_icon(icon)

# Clock to control the time
clock = pygame.time.Clock()

# Game loop
running = True
start_game = False
while running:
    # color the screen (before everything)
    screen.fill(BLACK)

    # initial page if start_game
    if start_game == False:
        # initialize class game, all the information about the game in one class
        game = Game(GAME_DIMENSION, BLOCK, screen)

        # change tuple
        change= (0,0)
        game.initial_page()

        for event in pygame.event.get():  # pygame.event.get() all the event happening inside the game
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_RETURN:
                    start_game = True
    
    # game interface if !startgame
    else:
        game.game_interface()
        for event in pygame.event.get():  # pygame.event.get() all the event happening inside the game
            if event.type == pygame.QUIT:
                running = False
            
            # a key is pressed
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_LEFT and previous_change != (BLOCK, 0):
                    change = (- BLOCK, 0)
                if event.key == pygame.K_RIGHT and previous_change != (-BLOCK, 0):
                    change = (BLOCK, 0)
                if event.key == pygame.K_DOWN and previous_change != (0, - BLOCK):
                    change = (0, BLOCK)
                if event.key == pygame.K_UP and previous_change != (0,  BLOCK):
                    change = (0, - BLOCK)

        
        previous_change = change
        if change == (0,0):
            game.start()

        game.move_snake(change)

        # Game over
        if game.status == False:
            game.game_over()
            pygame.display.update()
            event = pygame.event.wait()
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_r:
                    start_game = False
        else:
            game.draw_food()
            game.draw_snake()
            game.print_score()

        # delay based on the game speed
        clock.tick(game.speed)

    # update every iteration of the game loop
    pygame.display.update()