import pygame
import sys
import button1
from settings import *
from level import Level

# Function to start the game
def start_game():
    pygame.quit()
    game_loop()

# Function to exit the program
def exit_game():
    pygame.quit()
    sys.exit()

# Function to run the game loop
def game_loop():
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    level = Level(level_map, screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        background_color = pygame.Color(0,0,255)
        screen.fill(background_color)
        level.run()

        pygame.display.update()
        clock.tick(60)

def main_menu():
    # Create display window
    screen = pygame.display.set_mode((800, 500))
    pygame.display.set_caption('Menu')

    # Load button images
    start_img = pygame.image.load('/Users/user/Desktop/graphics/start_btn.png').convert_alpha()
    exit_img = pygame.image.load('/Users/user/Desktop/graphics/exit_btn.png').convert_alpha()

    # Create button instances
    start_button = button1.Button(100, 200, start_img, 0.8)
    exit_button = button1.Button(450, 200, exit_img, 0.8)

    # Set up font
    pygame.font.init()
    font = pygame.font.Font(None, 36)
    text = font.render("Nazira's Mario Game", True, (255, 0, 127))
    text_rect = text.get_rect(center=(800 // 2, 100))

    # Game loop for main menu
    run = True
    while run:
        screen.fill((202, 228, 241))

        # Draw title text
        screen.blit(text, text_rect)

        # Draw buttons
        if start_button.draw(screen):
            start_game()  # Start the game if "start" button is pressed
        if exit_button.draw(screen):
            exit_game()   # Exit the program if "exit" button is pressed

        # Event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
        pygame.display.update()
    pygame.quit()

# Run the main menu
main_menu()
