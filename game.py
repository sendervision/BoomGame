import math
import random
from typing import Callable, Optional, Dict, Any
import pygame
from pygame.font import FontType
from pygame.sprite import Group
from pygame.event import Event

from meteorite import Meteorite
from player import Player
from momi import Momi

class AddDifficult:
	def __init__(self, number: int, func: Callable, **kwargs) -> None:
		self.number = number
		self.func = func
		self.kwargs = kwargs

class Game(pygame.sprite.Sprite):
	def __init__(self, game) -> None:
		super().__init__()
		self.screen: pygame.SurfaceType = game.screen
		self.font: FontType = game.font
		self.stop_game: Callable = game.stop_game

		self.speed_momi = 2
		self.max_speed_momi = 5

		self.speed_meteorite = 3
		self.max_speed_meteorite = 5

		self.momi_group = Group()
		self.meteorite_group = Group()
		self.keys = {}

		self.difficults: Dict[int, AddDifficult] = {
		    0: AddDifficult(number=4, func=self.generate_momi),  # Au début du jeu, génère 1 "momi"
		    100: AddDifficult(number=1, func=self.change_speed_momi, speed=3, max_speed=8),  # À 100 points, augmente la vitesse de "momi"
		    150: AddDifficult(number=3, func=self.generate_meteorite),  # À 150 points, génère 2 "météorites"
		    200: AddDifficult(number=1, func=self.change_speed_meteorite, speed=5, max_speed=10),  # À 200 points, augmente la vitesse des "météorites"
		    400: AddDifficult(number=1, func=self.change_speed_momi, speed=8, max_speed=15),  # À 400 points, augmente encore la vitesse de "momi"
		    500: AddDifficult(number=3, func=self.generate_meteorite),  # À 500 points, génère 2 "météorites"
		    600: AddDifficult(number=1, func=self.change_speed_meteorite, speed=8, max_speed=15),  # À 600 points, augmente la vitesse des "météorites"
		    1000: AddDifficult(number=1, func=self.change_speed_momi, speed=12, max_speed=20),  # À 1000 points, augmente la vitesse de "momi" à 12
		}

		self.player = Player(self)

	@property
	def get_speed_momi(self):
		return random.randint(self.speed_momi, self.max_speed_momi)

	@property
	def get_speed_meteorite(self) -> int:
		return random.randint(self.speed_meteorite, self.max_speed_meteorite)

	def check_collision(self, sprite, group: Group):
		return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask)

	def check_grenade_collision(self, group1, group2):
		res = pygame.sprite.groupcollide(group1, group2, False, False, pygame.sprite.collide_mask)
		for g1 in group1:
			if res.get(g1):
				res[g1][0].momi_damage()
				g1.remove_grenade()

	def collision(self):
		meteorite: Optional[Meteorite] = self.player.is_collidered_with_meteorite
		if meteorite:
			self.player.reduce_life(self.player.damage_meteorite)
			meteorite.destroy_meorite()

	def display_game_element(self):
		self.screen.blit(self.player.image, self.player.rect)
		self.player.draw_life_bar(self.screen)
		self.player.all_grenade.draw(self.screen)
		self.momi_group.draw(self.screen)
		self.meteorite_group.draw(self.screen)

		# Affiche le score du joueur
		self.player.display_score(self.screen)

	def add_diffucult(self):
		if self.difficults.get(self.player.score):
			value: AddDifficult = self.difficults[self.player.score]
			for _ in range(value.number):
				value.func(**value.kwargs)
			self.difficults.pop(self.player.score)

	def loop_game(self):
		self.player.move(self.keys)
		self.check_grenade_collision(self.player.all_grenade, self.momi_group)
		self.collision()
		self.add_diffucult()

		# Boucle pour déplacer les grenades
		for grenade in self.player.all_grenade:
			grenade.move()

		# Boucle pour déplacer les momis
		for momi in self.momi_group:
			momi.move()
			momi.draw_bar_life()

		# Boucle pour déplacer les méteorites
		for meteorite in self.meteorite_group:
			meteorite.move()
		
	def keydown_event(self, event: Event) -> None:
		match event.key:
			case pygame.K_RIGHT:
				self.keys[pygame.K_RIGHT] = True
			case pygame.K_LEFT:
				self.keys[pygame.K_LEFT] = True
			case pygame.K_SPACE:
				self.player.attack()

	def keyup_event(self, event: Event) -> None:
		self.keys[event.key] = False
		self.keys.pop(event.key)

	def generate_momi(self):
		self.momi = Momi(self, self.player)
		self.momi_group.add(self.momi)

	def generate_meteorite(self):
		self.meteorite = Meteorite(self)
		self.meteorite_group.add(self.meteorite)

	def change_speed_momi(self, speed: int, max_speed: int):
		self.speed_momi = speed
		self.max_speed_momi = max_speed

	def change_speed_meteorite(self, speed: int, max_speed: int):
		self.speed_meteorite = speed
		self.max_speed_meteorite = max_speed



	