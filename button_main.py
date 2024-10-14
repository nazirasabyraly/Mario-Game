import pygame
import button1
import main

#create display window
SCREEN_HEIGHT = 500
SCREEN_WIDTH = 800

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Button Demo')

#load button images
start_img = pygame.image.load('/Users/user/Desktop/graphics/start_btn.png').convert_alpha()
exit_img = pygame.image.load('/Users/user/Desktop/graphics/exit_btn.png').convert_alpha()

#create button instances
start_button = button1.Button(100, 200, start_img, 0.8)
exit_button = button1.Button(450, 200, exit_img, 0.8)

#game loop
run = True
while run:

	screen.fill((202, 228, 241))

	if start_button.draw(screen):
		print('start')
	if exit_button.draw(screen):
		print('exit')

	#event handler
	for event in pygame.event.get():
		#quit game
		if event.type == pygame.QUIT:
			run = False

	pygame.display.update()

pygame.quit()