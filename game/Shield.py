import pygame
from random import randint

WIDTH = 700
HEIGHT = 900

win = pygame.display.set_mode((WIDTH, HEIGHT))

class Shield():
	def __init__(self):
		self.surface = pygame.transform.scale(pygame.image.load("game/Images/deflectorshield.png").convert_alpha(), (50, 50))
		self.rect = self.surface.get_rect(center=(0, 0))
		self.dy = 2
		self.spawn()


	def spawn(self):
		self.rect.centerx = randint(20, WIDTH - 20)
		self.rect.centery = randint(0, HEIGHT) - HEIGHT


	def generate(self, collectable_shields):
		if randint(0, 1000) / 2 == 0:
			collectable_shields.append(Shield())


	def move(self):
		self.rect.centery += self.dy
		win.blit(self.surface, self.rect)