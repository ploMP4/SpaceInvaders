import pygame

WIDTH = 700
HEIGHT = 900

win = pygame.display.set_mode((WIDTH, HEIGHT))

class SpaceShip():
	def __init__(self):
		self.surface = (
			pygame.image.load("game/Images/fighter.png").convert_alpha(), 
			pygame.image.load("game/Images/fighterThrust.png").convert_alpha()
		)	
		self.lives_surface = pygame.transform.scale(self.surface[0], (16, 16))
		self.shields_surface = pygame.transform.scale(pygame.image.load("game/Images/deflectorshield.png").convert_alpha(), (100, 100))
		self.shield_radius = self.shields_surface.get_width()*0.5
		self.is_shielded = False
		self.mini_shields_surface = pygame.transform.scale(self.shields_surface, (16, 16))
		self.is_alive = False

		self.create()


	def create(self):
		self.x = WIDTH / 2
		self.y = HEIGHT - 2 * self.surface[0].get_height()
		self.rect = self.surface[0].get_rect(center=(self.x, self.y))
		self.dx = 0
		self.dy = 0
		self.shields = 10
		self.lives = 5


	def draw_spaceShip(self, moving=False):
		if moving:
			win.blit(self.surface[1], self.rect)
		else:
			win.blit(self.surface[0], self.rect)


	def draw_utils(self):
		# Draw Lives UI
		for i in range(self.lives):
			win.blit(self.lives_surface, (i * self.lives_surface.get_width() + 10, 20))

		# Draw Shields UI
		for i in range(self.shields):
			win.blit(self.mini_shields_surface, (WIDTH-i *(self.mini_shields_surface.get_width()+5), 20))


	def draw_shield(self):
		if self.is_shielded:
			win.blit(self.shields_surface, (self.rect.centerx - self.shield_radius, self.rect.centery - self.shield_radius))


	def move(self):
		self.rect.centerx += self.dx
		self.rect.centery += self.dy

		if self.rect.centerx >= 20 + WIDTH - self.surface[0].get_width():
			self.rect.centerx = 20 + WIDTH - self.surface[0].get_width()

		if self.rect.centerx <= self.surface[0].get_width() - 20:
			self.rect.centerx = self.surface[0].get_width() - 20 

		if self.rect.centery >= 20 + HEIGHT - self.surface[0].get_height():
			self.rect.centery = 20 + HEIGHT - self.surface[0].get_height()

		if self.rect.centery <= self.surface[0].get_height() - 20:
			self.rect.centery = self.surface[0].get_height() - 20

		if self.dx != 0 or self.dy != 0:
			self.draw_spaceShip(moving=True)
		else:
			self.draw_spaceShip(moving=False)

		self.draw_shield()
		self.draw_utils()


	def is_hit(self):
		if self.is_shielded:
			self.is_shielded = False
		else:
			self.lives -= 1