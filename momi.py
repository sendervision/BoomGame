import random
import pygame
from pygame.sprite import Sprite

from constant import PATH_ASSETS_DIR
from player import Player

PATH_MOMI = PATH_ASSETS_DIR / "mummy"

class Momi(Sprite):
	def __init__(self, game, player: Player) -> None:
		super().__init__()

		self.game = game
		self.player = player
		self.screen: pygame.SurfaceType = self.game.screen

		# La vitesse du joueur
		self.speed = self.game.get_speed_momi

		self.life = 100
		self.max_life = 100
		self.damage = 20

		self.image = pygame.image.load(PATH_MOMI / "mummy1.png")
		self.rect = self.image.get_rect()

		self.rect.right = self.get_posx_momi
		self.rect.centery = self.screen.get_size()[1] - 100

	@property
	def get_rect(self):
		return self.rect

	@property
	def get_posx_momi(self) -> int:
		return self.screen.get_size()[0] + random.randint(0, 300)

	def draw_bar_life(self):
		color = (0, 255, 0)
		position = (10, 0, self.life, 5)
		pygame.draw.rect(self.image, (39, 51, 38), (10, 0, self.max_life, 5))
		pygame.draw.rect(self.image, color, position)

	def move(self):
		if not self.player.is_collidered_with_momi:
			self.rect.x -= self.speed
		else:
			self.player.life -= self.player.damage_momi

	def remove_momi(self):
		self.game.momi_group.remove(self)

	def momi_damage(self):
		self.life -= self.damage
		if self.life <= 0:
			self.player.add_score(10)
			self.rect.x = self.get_posx_momi
			self.life = self.max_life
			self.speed = self.game.get_speed_momi


