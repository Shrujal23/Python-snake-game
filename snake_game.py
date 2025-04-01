import pygame
import time
import random

# Initialize the game
pygame.init()

# Define colors
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 204, 0)  # Updated to a more vibrant green
blue = (0, 102, 204)  # Updated to a more vibrant blue
dark_blue = (0, 51, 102)

# Set display dimensions
width = 600
height = 400
display = pygame.display.set_mode((width, height))
pygame.display.set_caption('Modern Snake Game')

# Set game clock
clock = pygame.time.Clock()

# Snake properties
snake_block = 10
snake_speed = 15

# Enhanced font styles with custom fonts
try:
    font_style = pygame.font.Font("arial.ttf", 25)
    score_font = pygame.font.Font("arial.ttf", 35)
except:
    font_style = pygame.font.SysFont("arial", 25)
    score_font = pygame.font.SysFont("arial", 35)

def draw_gradient_background():
    """Draw a gradient background from dark blue to blue."""
    for i in range(height):
        color = (
            dark_blue[0] + (blue[0] - dark_blue[0]) * i // height,
            dark_blue[1] + (blue[1] - dark_blue[1]) * i // height,
            dark_blue[2] + (blue[2] - dark_blue[2]) * i // height
        )
        pygame.draw.line(display, color, (0, i), (width, i))

def our_snake(snake_block, snake_list):
    """Draw the snake on the display with gradient coloring."""
    for i, x in enumerate(snake_list):
        # Create a gradient effect from dark green to light green
        gradient_color = (
            0,
            max(100, min(255, 150 + (i * 2))),
            0
        )
        pygame.draw.rect(display, gradient_color, [x[0], x[1], snake_block, snake_block])
        # Add a small white highlight for 3D effect
        pygame.draw.rect(display, (255, 255, 255), 
                        [x[0], x[1], snake_block/3, snake_block/3])

def message(msg, color):
    """Display a message on the screen with shadow effect."""
    # Add shadow effect
    shadow = font_style.render(msg, True, (0, 0, 0))
    mesg = font_style.render(msg, True, color)
    display.blit(shadow, [width/6 + 2, height/3 + 2])  # Shadow offset
    display.blit(mesg, [width/6, height/3])

def gameLoop():  # Main game loop
    """Main game loop."""
    game_over = False
    game_close = False

    x1 = width / 2
    y1 = height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0

    # Define hurdles
    hurdle_width = 10
    hurdle_height = 10
    hurdles = [(200, 150), (300, 250), (400, 100)]  # Example hurdle positions

    while not game_over:

        while game_close:
            draw_gradient_background()
            message("You Lost! Press C-Play Again or Q-Quit", red)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        draw_gradient_background()

        pygame.draw.rect(display, green, [foodx, foody, snake_block, snake_block])  # Draw food
        # Draw hurdles
        for hurdle in hurdles:
            pygame.draw.rect(display, black, [hurdle[0], hurdle[1], hurdle_width, hurdle_height])  # Draw hurdles

        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List)  # Draw the snake

        # Check for collisions with hurdles and display message
        for hurdle in hurdles:
            if snake_Head[0] == list(hurdle):
                message("You hit an obstacle! Start again by pressing C or Q to quit.", red)

                game_close = True  # End game if snake hits a hurdle

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()

gameLoop()
