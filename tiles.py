import pygame 
import random

class Tile(pygame.sprite.Sprite):
	def __init__(self,pos,size):
		super().__init__()
		self.image = pygame.Surface((size,size))
		fill_color = pygame.Color(0, 255, 0)
		self.image.fill(fill_color)
		self.rect = self.image.get_rect(topleft = pos)
	def update(self,x_shift):
		self.rect.x	+= x_shift
class Circle(pygame.sprite.Sprite):
    def __init__(self, x,y):
        super().__init__()
        self.radius = 20
        self.color = (255, 0, 0)  # Red color for circles
        self.image = pygame.Surface((2 * self.radius, 2 * self.radius), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))  # Transparent fill
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center=(x, y))

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)