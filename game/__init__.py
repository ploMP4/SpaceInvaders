import pygame
from random import randint
from .Board import Board
from .SpaceShip import SpaceShip
from .Laser import Laser
from .Rocket import Rocket
from .Enemy import Enemy
from .Controls import Controls
from .Shield import Shield
from .Sounds import Sounds
# Constants
WIDTH = 700
HEIGHT = 900
FPS = 60

pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")
favicon = pygame.image.load("game/Images/fighter.png").convert_alpha()
pygame.display.set_icon(favicon)

game_font = pygame.font.SysFont("comicsans", 40)


def handle_bullets(bullets, dy, sound, enemies):
	for bullet in bullets:
		bullet.dy += dy
		if bullet.rect.centery <= 0 or check_collition(bullet.rect, enemies, sound):
			bullets.remove(bullet)
		bullet.move()


def check_collition(rect, enemies, sound=None):
	for enemy in enemies:
		if rect.colliderect(enemy.rect) and rect is not enemy.rect:
			if sound != None:
				sound.play()
			enemy.create()
			return True


def main():
	# Game Variables
	clock = pygame.time.Clock()
	board = Board()
	space_ship = SpaceShip()
	sounds = Sounds()
	sounds.play_music(sounds.start_screen_music)
	shield_start_time = 0
	collectable_shields = []
	lasers = []
	rockets = []
	enemy_lasers = []
	enemies = [Enemy() for _ in range(10)]
	enemy_can_shoot = False
	enemy_cooldown = 2000
	controls = Controls(space_ship, lasers, rockets, enemies, sounds)
	run = True
	# Main game loop
	while run:
		clock.tick(FPS)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			if event.type == pygame.KEYDOWN and space_ship.is_alive:
				controls.move(event)
				controls.actions(event)
			# Game Start
			elif event.type == pygame.KEYDOWN and not space_ship.is_alive:
				controls.start_game(event)
			if event.type == pygame.KEYUP and space_ship.is_alive:
				if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
					space_ship.dx = 0
				if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
					space_ship.dy = 0

		# Play ingame Music
		if not pygame.mixer.music.get_busy():
			sounds.play_music(sounds.in_game_music)

		if space_ship.is_alive:
			board.draw_background()
			board.draw_score(game_font)
			space_ship.move()
			
			for shield in collectable_shields:
				shield.move()
				if shield.rect.centery >= HEIGHT:
					collectable_shields.remove(shield)
				if shield.rect.colliderect(space_ship.rect):
					collectable_shields.remove(shield)
					space_ship.shields += 1

			if randint(0, 1000) / 2 == 0:
				collectable_shields.append(Shield())

			if check_collition(space_ship.rect, enemies, sounds.laser_hit_sound):
				space_ship.is_hit()

			if space_ship.lives == 0:
				space_ship.is_alive = False
				pygame.mixer.music.stop()
				sounds.play_music(sounds.start_screen_music)
			# Checks so enemies dont spawn one inside another
			for enemy in enemies:
				check_collition(enemy.rect, enemies)
				enemy.move()
			# Shield Active Duration
			if pygame.time.get_ticks() - controls.shield_start_time >= 5000:
				space_ship.is_shielded = False


			handle_bullets(lasers, 6, sounds.laser_hit_sound, enemies)
			handle_bullets(rockets, 3, sounds.rocket_hit_sound, enemies)


			if pygame.time.get_ticks() - 2000 >= enemy_cooldown:
				enemy_can_shoot = True
				laser = Laser(enemies[randint(0, 9)].rect)
				enemy_lasers.append(laser)
				sounds.laser_sound.play()
				enemy_cooldown = pygame.time.get_ticks()

			if enemy_can_shoot:
				for laser in enemy_lasers:
					laser.dy -= 6
					if laser.rect.centery >= HEIGHT:
						enemy_lasers.remove(laser)
					elif laser.rect.colliderect(space_ship.rect):
						sounds.laser_hit_sound.play()
						space_ship.is_hit()
						enemy_lasers.remove(laser)
					laser.move()
		else:
			board.draw_starting_screen()


		pygame.display.update()