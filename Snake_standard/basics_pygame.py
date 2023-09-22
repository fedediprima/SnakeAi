import pygame

# Initialize pygame
pygame.init()

# constants
DIMENSION = (800,600)
BLACK = (0,0,0)
GRAY = (128,128,128)
RED = (255,0,0)

# Create the window
screen = pygame.display.set_mode(DIMENSION)

# Title and Icon
pygame.display.set_caption("NOME DEL GIOCO")
icon = pygame.image.load("images/anaconda.png")
pygame.display.set_icon(icon)

# to insert image of snake in the window
position_x = 10
position_y = 10
image = pygame.image.load("images/anaconda.png")
def snake(x,y):
    screen.blit(image, (x, y))

# position change at zero at beginning
position_x_change = 0
position_y_change = 0

# Game loop
running = True
while running:
    # color the screen (before everything)
    screen.fill(GRAY)

    for event in pygame.event.get():  # pygame.event.get() all the event happening inside the game
        if event.type == pygame.QUIT:
            running = False

        # a key is pressed
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_LEFT:
                position_x_change = -0.5
                position_y_change = 0
            if event.key == pygame.K_RIGHT:
                position_x_change = +0.5
                position_y_change = 0
            if event.key == pygame.K_DOWN:
                position_x_change = 0
                position_y_change = +0.5
            if event.key == pygame.K_UP:
                position_x_change = 0
                position_y_change = -0.5

        # a key is released
        #if event.type == pygame.KEYUP:
            #if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            #    position_x_change = 0
    
    # update position of the head
    position_x += position_x_change
    position_y += position_y_change
    
    # insert image in the window every iteration  the loop 
    snake(position_x, position_y)


    # update every iteration of the game loop
    pygame.display.update()