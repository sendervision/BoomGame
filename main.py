import sys
import pygame
from constant import PATH_ASSETS_DIR
from game import Game

class BoomGame(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.screen = pygame.display.set_mode((1100, 600))
        self.SIZE_SCREEN = self.screen.get_size()
        self.clock = pygame.time.Clock()
        self.image_bg = pygame.image.load(PATH_ASSETS_DIR / "bg.jpg")
        self.font = pygame.font.SysFont("JetBrains Mono", 25)

        self.running = True
        self.game = Game(self)

    def display_onboarding_screen(self):
        self.screen.blit(self.image_bg, (0, -300))

    def stop_game(self):
        self.running = False

    def manager_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stop_game()
            elif event.type == pygame.KEYDOWN:
                self.game.keydown_event(event)
            elif event.type == pygame.KEYUP:
                self.game.keyup_event(event)

    def run(self):
        # Boucle du jeux
        while self.running:
            self.display_onboarding_screen()
            self.manager_event()
            self.game.display_game_element()
            self.game.loop_game()
            self.clock.tick(60)
            pygame.display.flip()

        pygame.quit()
        sys.exit()


def main():
    pygame.init()

    boomgame = BoomGame()
    boomgame.run()

if __name__ == "__main__":
    main()