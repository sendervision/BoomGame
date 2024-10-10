import pygame
from pygame import SurfaceType

class Animation:
    def __init__(self, surface: SurfaceType, duration, loop=False):
        self.surface = surface
        self.duration = duration  # Durée de l'animation en millisecondes
        self.loop = loop  # Si True, l'animation boucle
        self.start_time = pygame.time.get_ticks()  # Temps de début de l'animation
        self.alpha = 0  # Opacité actuelle
        self.fading_in = True  # Indique si l'animation est en train de s'estomper
        self.finished = False  # Indique si l'animation est terminée

    def start(self):
        self.start_time = pygame.time.get_ticks()  # Initialiser le temps de début
        self.finished = False  # Réinitialiser l'état terminé

    @property
    def elapsed_time(self) -> int:
        return pygame.time.get_ticks() - self.start_time

    def fadeIn(self):
        self.alpha = min(255, (self.elapsed_time / self.duration) * 255)  # Augmenter l'opacité
        if self.alpha >= 255:
            if self.loop:
                self.start()  # Redémarrer l'animation si en boucle
            else:
                self.finished = True  # Terminer l'animation
                self.alpha = 255  # S'assurer que l'opacité est à 255
            self.fading_in = False

    def fadeOut(self):
        self.alpha = max(0, 255 - (self.elapsed_time / self.duration) * 255)  # Diminuer l'opacité
        if self.alpha <= 0:
            if self.loop:
                self.start()  # Redémarrer l'animation si en boucle
            else:
                self.finished = True  # Terminer l'animation
                self.alpha = 0  # S'assurer que l'opacité est à 0
            self.fading_in = True  # Passer à l'apparition

    def fade_InOut(self):
        if self.finished:
            return

        if self.fading_in:
            self.fadeIn()
        else:
            self.fadeOut()

        # Appliquer l'opacité à la surface
        self.surface.set_alpha(self.alpha)

    def stop(self):
        self.finished = True
        self.alpha = 0
        self.surface.set_alpha(self.alpha)


