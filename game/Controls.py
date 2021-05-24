import pygame
from .Laser import Laser
from .Rocket import Rocket

class Controls():
	def __init__(self, space_ship, lasers, rockets, enemies, sounds):
		self.space_ship = space_ship
		self.lasers = lasers
		self.rockets = rockets
		self.sounds = sounds
		self.enemies = enemies
		self.shield_start_time = 0


	def move(self, event):
		if event.key == pygame.K_LEFT:
			self.space_ship.dx -= 4
		if event.key == pygame.K_RIGHT:
			self.space_ship.dx += 4
		if event.key == pygame.K_UP:
			self.space_ship.dy -= 4
		if event.key == pygame.K_DOWN:
			self.space_ship.dy += 4


	def actions(self, event):
		if event.key == pygame.K_s:
			if not self.space_ship.is_shielded and self.space_ship.shields > 0:
				self.activate_shield()

		if event.key == pygame.K_SPACE:
			self.shoot(Laser, self.lasers, self.sounds.laser_sound)
			
		if event.key == pygame.K_r:
			if len(self.rockets) < 3:
				self.shoot(Rocket, self.rockets, self.sounds.rocket_sound)


	def start_game(self, event):
		if event.key == pygame.K_p:
			self.space_ship.is_alive = True
			self.space_ship.create()
			pygame.mixer.music.stop()
			for enemy in self.enemies:
				enemy.create()


	def shoot(self, weapon_class, weapons, sound):
		weapon = weapon_class(self.space_ship.rect)
		weapons.append(weapon)
		sound.play()


	def activate_shield(self):
		self.space_ship.is_shielded = True
		self.space_ship.shields -= 1
		self.shield_start_time = pygame.time.get_ticks()
		self.sounds.shield_sound.play()