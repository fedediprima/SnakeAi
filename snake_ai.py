import pygame
from classes_ai import Game, Agent
from plot import plot

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

Direction = {
    "RIGHT" : (BLOCK, 0),
    "LEFT" : (- BLOCK, 0),
    "UP" : (0, -BLOCK),
    "DOWN" : (0, BLOCK)
}


# Create the window
screen = pygame.display.set_mode(DISPLAY_DIMENSION)

# Title and Icon
pygame.display.set_caption("SNAKE")
icon = pygame.image.load("images/anaconda.png")
pygame.display.set_icon(icon)

# Clock to control the time
clock = pygame.time.Clock()

game = Game(GAME_DIMENSION, BLOCK, screen)
agent = Agent()

# change tuples
change= (0, BLOCK)
previous_change = (0, BLOCK)

# score variables
plot_scores = []
plot_mean_scores = []
total_score = 0
record = 0

# Game loop
running = True
while running:
    # color the screen (before everything)
    screen.fill(BLACK)

    if game.status==True:
        game.game_interface()
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                running = False

        # get old state
        old_state = agent.get_state(game)
        
        # get action
        final_move = agent.get_action(old_state)

        # get move
        clock_wise = [Direction["RIGHT"], Direction["DOWN"], Direction["LEFT"], Direction["UP"]]
        idx = clock_wise.index(previous_change)

        # no turn
        if final_move == [1,0,0]:
            change = clock_wise[idx]
        # right turn
        if final_move == [0,1,0]:
            new_idx = (idx + 1) % 4 
            change = clock_wise[new_idx]
        # left turn
        if final_move == [0,0,1]:
            new_idx = (idx - 1) % 4 
            change = clock_wise[new_idx]

        
        # logica per cambiare final_move e metterla in formagto (x,y) come change, and game step
        previous_change = change

        reward = game.move_snake(change) # devo ritornare reward per ogni mossa
        
        # get state after the move
        new_state = agent.get_state(game)

        # trainare l'agent considerando old state, final move, reward and new state
        # train short memory 
        agent.train_short_memory(old_state, final_move, reward, new_state, game.status)

        # add the data tu the memory
        agent.update_memory(old_state, final_move, reward, new_state, game.status)

        # Game over
        if game.status == False:

            if game.score > record:
                record = game.score
                agent.model.save()

            print('Game', agent.n_games, 'Score', game.score, 'Record:', record)

            plot_scores.append(game.score)
            total_score += game.score
            mean_score = total_score / (agent.n_games + 1)
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)

            game.reset()
            change = (0, BLOCK)
            agent.n_games += 1
            agent.train_long_memory()

        else:
            game.draw_food()
            game.draw_snake()
            game.print_score()

        # delay based on the game speed
        clock.tick(game.speed)

    # update every iteration of the game loop
    pygame.display.update()