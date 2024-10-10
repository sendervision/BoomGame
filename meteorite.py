import random
import pygame
from pygame.sprite import Sprite

from constant import PATH_ASSETS_DIR, PATH_SOUND_DIR


class Meteorite(Sprite):
	def __init__(self, game) -> None:
		super().__init__()
		self.game = game
		self.speed = self.game.get_speed_meteorite

		self.sound_meteorite = pygame.mixer.Sound(PATH_SOUND_DIR / "meteorite.ogg")
		self.image = pygame.image.load(PATH_ASSETS_DIR / "comet.png")
		self.image = pygame.transform.scale(self.image, (60, 60))
		self.rect = self.image.get_rect()
		self.rect.x = self.get_pos_x
		self.rect.y = self.get_pos_y

	@property
	def get_pos_x(self) -> int:
		return random.randint(0, self.game.screen.get_size()[0])

	@property
	def get_pos_y(self) -> int:
		return random.randint(0, 300) - self.game.screen.get_size()[1]

	def destroy_meorite(self):
		self.game.meteorite_group.remove(self)

	def move(self):
		self.rect.y += self.speed
		# Permet de detruire la météorite s'il quitte l'écran
		if self.rect.y >= self.game.screen.get_height() - 100:
			self.rect.y = self.get_pos_y
			self.rect.x = self.get_pos_x
			self.speed = self.game.get_speed_meteorite
			self.sound_meteorite.play()
