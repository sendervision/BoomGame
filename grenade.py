import pygame
from pygame.sprite import Sprite
from constant import PATH_ASSETS_DIR


class Grenade(Sprite):
	def __init__(self, player) -> None:
		super().__init__()
		self.image = pygame.image.load(PATH_ASSETS_DIR / "projectile.png")
		self.image = pygame.transform.scale(self.image, (50, 50))
		self.rect = self.image.get_rect()
		self.player = player

		# Positionnement du grenade par rapport au joueur
		self.rect.right = self.player.rect.right
		self.rect.centery = self.player.rect.centery

		self.speed = 7

	def remove_grenade(self):
		self.player.all_grenade.remove(self)

	def move(self):
		self.rect.x += self.speed
		self.image = pygame.transform.rotate(self.image, 90)
		if self.rect.x > 1100:
			self.player.all_grenade.remove(self)
