import pygame
from .Laser import Laser

WIDTH = 700
HEIGHT = 900

win = pygame.display.set_mode((WIDTH, HEIGHT))

class Rocket(Laser):
	def __init__(self, spaceship_pos):
		super().__init__(spaceship_pos)
		self.surface = pygame.transform.scale(pygame.image.load("game/Images/rocket.png").convert_alpha(), (17, 50))
		self.rect = self.surface.get_rect(center=(self.x + 20, self.y))

