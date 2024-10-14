import pygame 
from tiles import Tile, Circle 
from settings import tile_size, screen_width, screen_height
from player import Player
from particles import ParticleEffect
import random

class Level:
	def __init__(self,level_data,surface):
		
		# level setup
		self.display_surface = surface 
		self.setup_level(level_data)
		self.world_shift = 0
		self.current_x = 0

		# dust
		self.dust_sprite = pygame.sprite.GroupSingle()
		self.player_on_ground = False
		
        # Create a sprite group for circles
		self.scores = 0
		
	def handle_circle_collisions(self):
		player = self.player.sprite
		collided_circles = pygame.sprite.spritecollide(player, self.circle_sprites, True)
		for circle in collided_circles:
            # Increase player's score
			self.scores += 1

	def create_jump_particles(self,pos):
		if self.player.sprite.facing_right:
			pos -= pygame.math.Vector2(10,5)
		else:
			pos += pygame.math.Vector2(10,-5)
		jump_particle_sprite = ParticleEffect(pos, '/jump')
		self.dust_sprite.add(jump_particle_sprite)
	
	def get_player_on_ground(self):
		if self.player.sprite.on_ground:
			self.player_on_ground = True
		else:
			self.player_on_ground = False
	
	def create_landing_dust(self):
		if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
			if self.player.sprite.facing_right:
				offset = pygame.math.Vector2(10,15)
			else:
				offset = pygame.math.Vector2(-10,15)
			fall_dust_particle = ParticleEffect(self.player.sprite.rect.midbottom - offset,'/land')
			self.dust_sprite.add(fall_dust_particle)
	
	def scroll_x(self):
		player = self.player.sprite
		player_x = player.rect.centerx
		direction_x = player.direction.x

		if player_x <  screen_width / 4 and direction_x < 0:
			self.world_shift = 8
			player.speed = 0
			
		elif player_x >  screen_width - (screen_width / 4) and direction_x > 0:
			self.world_shift = -8
			player.speed = 0
		else:
			self.world_shift = 0
			player.speed = 8
	    
	def setup_level(self,layout):
		self.tiles = pygame.sprite.Group()
		self.player = pygame.sprite.GroupSingle()
		self.circle_sprites = pygame.sprite.Group()
		for row_index,row in enumerate(layout):
			for col_index,cell in enumerate(row):
				x = col_index * tile_size
				y = row_index * tile_size
				if cell == 'X' :
					tile = Tile((x,y), tile_size)
					self.tiles.add(tile)
				if cell == 'P':
					player_sprite = Player((x,y), self.display_surface, self.create_jump_particles)
					self.player.add(player_sprite)
				if cell == 'C':
					circle = Circle(x + tile_size // 2, y + tile_size // 2)  # Place circle in the center of the tile
					self.circle_sprites.add(circle)
		
	def vertical_movement_collision(self):
		player = self.player.sprite
		player.apply_gravity()

		for sprite in self.tiles.sprites():
			if sprite.rect.colliderect(player.rect):
				if player.direction.y > 0:
					player.rect.bottom = sprite.rect.top
					player.direction.y = 0
					player.on_ground = True
				elif player.direction.y < 0:
					player.rect.top = sprite.rect.bottom
					player.direction.y = 0
					player.on_ceiling = True

		if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
			player.on_ground = False
		if player.on_ceiling and player.direction.y > 0.1:
			player.on_ceiling = False
	
	def horizontal_movement_collision(self):
		player = self.player.sprite
		player.rect.x += player.direction.x * player.speed

		for sprite in self.tiles.sprites():
			if sprite.rect.colliderect(player.rect):
				if player.direction.x < 0:
					player.rect.left = sprite.rect.right
					player.on_left = True
					self.current_x = player.rect.left
				elif player.direction.x > 0:
					player.rect.right = sprite.rect.left
					player.on_right = True
					self.current_x = player.rect.right

		if player.on_left and (player.rect.left < self.current_x or player.direction.x <= 0):
			player.on_left = False
		if player.on_right and (player.rect.right > self.current_x or player.direction.x >= 0):
			player.on_right = False

	def levels(self):
		if self.scores <= 5:
			font = pygame.font.Font(None, 36)
			text_surface = font.render(f"Level: 1", True, (255, 255, 255))
			text_rect = text_surface.get_rect(topleft=(200, 10))
			self.display_surface.blit(text_surface, text_rect)
		elif self.scores >= 5:
			font = pygame.font.Font(None, 36)
			text_surface = font.render(f"Level: 2", True, (255, 255, 255))
			text_rect = text_surface.get_rect(topleft=(200, 10))
			self.display_surface.blit(text_surface, text_rect)
			self.speed = 16
		elif self.scores >= 10:
			font = pygame.font.Font(None, 36)
			text_surface = font.render(f"Level: 3", True, (255, 255, 255))
			text_rect = text_surface.get_rect(topleft=(200, 10))
			self.display_surface.blit(text_surface, text_rect)
			self.speed = 24

	def run(self):
		self.levels()
		#level tiles
		self.tiles.update(self.world_shift)
		self.tiles.draw(self.display_surface)
		self.scroll_x()
        
		#dust particles
		self.dust_sprite.update(self.world_shift)
		self.dust_sprite.draw(self.display_surface)

		#player
		self.player.update()
		self.horizontal_movement_collision()
		self.get_player_on_ground()
		self.vertical_movement_collision()
		self.create_landing_dust()
		self.player.draw(self.display_surface)
		
		self.circle_sprites.draw(self.display_surface)
		
        # Inside the player update method
		self.handle_circle_collisions()

		 # Render and display score text
		font = pygame.font.Font(None, 36)
		text_surface = font.render(f"Score: {self.scores}", True, (255, 255, 255))
		text_rect = text_surface.get_rect(topleft=(10, 10))
		self.display_surface.blit(text_surface, text_rect)


		
    