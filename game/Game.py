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

class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.board = Board()
        self.space_ship = SpaceShip()
        self.sounds = Sounds()
        self.sounds.play_music(self.sounds.start_screen_music)
        self.shield_start_time = 0
        self.collectable_shields = []
        self.lasers = []
        self.rockets = []
        self.enemy_lasers = []
        self.enemies = [Enemy() for _ in range(10)]
        self.enemy_can_shoot = False
        self.enemy_cooldown = 2000
        self.controls = Controls(
            self.space_ship,
            self.lasers,
            self.rockets,
            self.enemies,
            self.sounds
        )
        self.run = True

    def handle_bullets(self, bullets, dy, sound, enemies, board):
        for bullet in bullets:
            bullet.dy += dy
            if self.check_collition(bullet.rect, enemies, sound):
                board.score += 1
                bullets.remove(bullet)
            elif bullet.rect.centery <= 0:
                bullets.remove(bullet)
            bullet.move()

    def check_collition(self, rect, enemies, sound=None):
        for enemy in enemies:
            if rect.colliderect(enemy.rect) and rect is not enemy.rect:
                if sound != None:
                    sound.play()
                enemy.create()
                return True

        return False

    def main(self):
        # Main game loop
        while self.run:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                if event.type == pygame.KEYDOWN and self.space_ship.is_alive:
                    self.controls.move(event)
                    self.controls.actions(event)
                # Game Start
                elif event.type == pygame.KEYDOWN and not self.space_ship.is_alive:
                    self.controls.start_game(event)
                if event.type == pygame.KEYUP and self.space_ship.is_alive:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        self.space_ship.dx = 0
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        self.space_ship.dy = 0

            # Play ingame Music
            if not pygame.mixer.music.get_busy():
                self.sounds.play_music(self.sounds.in_game_music)

            if self.space_ship.is_alive:
                self.board.draw_background()
                self.board.draw_score(game_font)
                self.space_ship.move()

                for shield in self.collectable_shields:
                    shield.move()
                    if shield.rect.centery >= HEIGHT:
                        self.collectable_shields.remove(shield)
                    if shield.rect.colliderect(self.space_ship.rect):
                        self.collectable_shields.remove(shield)
                        self.space_ship.shields += 1

                if randint(0, 1000) / 2 == 0:
                    self.collectable_shields.append(Shield())

                if self.check_collition(self.space_ship.rect, self.enemies, self.sounds.laser_hit_sound):
                    self.space_ship.is_hit()

                if self.space_ship.lives == 0:
                    self.space_ship.is_alive = False
                    pygame.mixer.music.stop()
                    self.sounds.play_music(self.sounds.start_screen_music)
                # Checks so enemies don't spawn one inside another
                for enemy in self.enemies:
                    self.check_collition(enemy.rect, self.enemies)
                    enemy.move()
                # Shield Active Duration
                if pygame.time.get_ticks() - self.controls.shield_start_time >= 5000:
                    self.space_ship.is_shielded = False

                self.handle_bullets(
                    self.lasers, 6,
                    self.sounds.laser_hit_sound,
                    self.enemies,
                    self.board
                )

                self.handle_bullets(
                    self.rockets, 3,
                    self.sounds.rocket_hit_sound,
                    self.enemies,
                    self.board
                )

                if pygame.time.get_ticks() - 2000 >= self.enemy_cooldown:
                    self.enemy_can_shoot = True
                    laser = Laser(self.enemies[randint(0, 9)].rect)
                    self.enemy_lasers.append(laser)
                    self.sounds.laser_sound.play()
                    self.enemy_cooldown = pygame.time.get_ticks()

                if self.enemy_can_shoot:
                    for laser in self.enemy_lasers:
                        laser.dy -= 6
                        if laser.rect.centery >= HEIGHT:
                            self.enemy_lasers.remove(laser)
                        elif laser.rect.colliderect(self.space_ship.rect):
                            self.sounds.laser_hit_sound.play()
                            self.space_ship.is_hit()
                            self.enemy_lasers.remove(laser)
                        laser.move()
            else:
                self.board.draw_starting_screen()

            pygame.display.update()
