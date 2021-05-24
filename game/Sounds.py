import pygame

class Sounds():
	def __init__(self):
		self.shield_sound = pygame.mixer.Sound("game/Sounds/deflectorshieldSound.wav")
		self.laser_sound = pygame.mixer.Sound("game/Sounds/laserSound.wav")
		self.laser_hit_sound = pygame.mixer.Sound("game/Sounds/spaceShipExplosionSound.wav")
		self.rocket_sound = pygame.mixer.Sound("game/Sounds/rocketLaunch.wav")
		self.rocket_hit_sound = pygame.mixer.Sound("game/Sounds/rocketExplosion.wav")
		self.start_screen_music = "game/Sounds/CityStomper.wav"
		self.in_game_music = "game/Sounds/RaceToMars.wav"

	def play_music(self, music):
		pygame.mixer.music.load(music)
		pygame.mixer.music.play()