import pygame
from random import randint

WIDTH = 700
HEIGHT = 900

win = pygame.display.set_mode((WIDTH, HEIGHT))

class Enemy():
	def __init__(self):
		self.surfaces = (
			pygame.transform.scale(pygame.image.load("game/Images/enemy1.png").convert_alpha(), (56, 56)),
			pygame.transform.scale(pygame.image.load("game/Images/enemy2.png").convert_alpha(), (50, 50)),
			pygame.transform.scale(pygame.image.load("game/Images/enemy3.png").convert_alpha(), (68, 68))
		)
		self.x = 0
		self.y = 0
		self.speed = 3
		self.rects = tuple([self.surfaces[i].get_rect(center=(self.x, self.y)) for i in range(len(self.surfaces))])

	def create(self):
		enemy_img = randint(0, 2)
		self.rects[enemy_img].centerx = randint(20, WIDTH - 20)
		self.rects[enemy_img].centery = randint(0, HEIGHT) - HEIGHT
		self.surface = self.surfaces[enemy_img]
		self.rect = self.rects[enemy_img]

	def move(self):
		self.rect.centery += self.speed
		if self.rect.centery >= HEIGHT:
			self.create()

		win.blit(self.surface, self.rect)