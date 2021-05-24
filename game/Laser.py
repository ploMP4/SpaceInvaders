import pygame

WIDTH = 700
HEIGHT = 900

win = pygame.display.set_mode((WIDTH, HEIGHT))

class Laser():
	def __init__(self, spaceship_pos):
		self.surface = pygame.image.load("game/Images/torpedo.png").convert_alpha()
		self.x = spaceship_pos[0] 
		self.y = spaceship_pos[1]
		self.dx = 0
		self.dy = 0
		self.rect = self.surface.get_rect(center=(self.x + 20, self.y))

	def move(self):
		self.rect.centery -= self.dy
		win.blit(self.surface, self.rect)

		self.dy = 0
