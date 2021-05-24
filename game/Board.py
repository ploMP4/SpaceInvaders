import pygame

WIDTH = 700
HEIGHT = 900

win = pygame.display.set_mode((WIDTH, HEIGHT))

class Board():
	def __init__(self):
		self.bg_surface = pygame.image.load("game/Images/background.jpg").convert()
		self.bg_ypos = 0
		self.score = 0
		self.starting_screen_surface = pygame.image.load("game/Images/startscreen.png").convert_alpha()

	def draw_background(self):
		win.blit(self.bg_surface, (0, self.bg_ypos))
		win.blit(self.bg_surface, (0, self.bg_ypos - HEIGHT))
		self.bg_ypos += .5
		if self.bg_ypos >= HEIGHT:
			self.bg_ypos = 0

	def draw_starting_screen(self):
		win.blit(self.starting_screen_surface, (0, 0))

	def draw_score(self, game_font):
		self.score_surface = game_font.render("Score: " + str(int(self.score)), True, (255,255,255))
		self.score_rect = self.score_surface.get_rect(center = (WIDTH/2, 40))
		win.blit(self.score_surface, self.score_rect)