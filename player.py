import math
from typing import Tuple, Dict, List, Optional

import pygame
from pygame import Rect
from pygame.sprite import Sprite, Group
from constant import PATH_ASSETS_DIR
from grenade import Grenade
from meteorite import Meteorite

PATH_ASSESTS_PLAYER = PATH_ASSETS_DIR / "player"

class Player(Sprite):
	def __init__(self, game) -> None:
		super().__init__()
		self.speed = 10
		self.opacity = 255
		self.max_life = self.life = 150
		self.damage_momi = 2  
		self.damage_meteorite = 20
		self.score: int = 0                                                                      

		self.image = pygame.image.load(PATH_ASSESTS_PLAYER / "player1.png")
		self.image.set_alpha(self.opacity)

		self.rect: Rect = self.image.get_rect()
		self.rect.x = math.ceil(1100 / 4)
		self.rect.y = 400

		self.game = game

		self.all_grenade = Group()
		self.key_pressed = {}

	@property
	def get_rect(self) -> Rect:
		return self.rect

	@property
	def get_size(self) -> Tuple[int, int]:
		return self.image.get_size()

	@property
	def is_collidered_with_momi(self):
		return self.game.check_collision(self, self.game.momi_group)

	@property
	def is_collidered_with_meteorite(self) -> Optional[Meteorite]:
		list_meteorite: List[Meteorite] = self.game.check_collision(self, self.game.meteorite_group)
		return list_meteorite[0] if list_meteorite else None

	def add_score(self, point: int):
		self.score += point

	def reduce_life(self, point: int):
		self.life -= point

	# Désinner la bar de vie au centre de l'image du joueur
	def draw_life_bar(self, surface: pygame.SurfaceType):
		# Couleur de la bar
		color_bar_bg = (39, 51, 38)
		color_bar = (0, 255, 0)

		# Position de la bar
		pos_x = self.rect.x + 30
		pos_y = self.rect.y + 20
		position_bar = (pos_x, pos_y, self.life, 10)
		position_bar_bg = (pos_x, pos_y, self.max_life, 10)

		# Dessine la bar et la bar bg
		pygame.draw.rect(surface, color_bar_bg, position_bar_bg)
		pygame.draw.rect(surface, color_bar, position_bar)

	def display_score(self, surface: pygame.SurfaceType):
		score_player = f"SCORE: {self.score}"
		text_score_player = self.game.font.render(score_player, False, (255, 255, 255))
		surface.blit(text_score_player, (10, 0))

	def move(self, key_pressed: Dict[int, bool]):
		if key_pressed.get(pygame.K_RIGHT):
			self.move_right()
		elif key_pressed.get(pygame.K_LEFT):
			self.move_left()

	def move_right(self):
		if not self.is_collidered_with_momi and self.rect.x < 900:
			self.rect.x += self.speed
	
	def move_left(self):
		if self.rect.x > 0:
			self.rect.x -= self.speed

	def attack(self):
		self.grenade =Grenade(self)
		self.all_grenade.add(self.grenade)


