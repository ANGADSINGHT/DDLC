import pygame
import sys
import os

pygame.init()

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
FPS = 30

# FULLSCREEN = pygame.FULLSCREEN if input("Fullscreen? y/n: ").lower() == 'y' else 0  # noqa: E501

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),
                                 flags=0)

pygame.display.set_caption("Doki Doki Literature C*nts")


def resource_path(path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, path)
    return os.path.join(path)


class Game:
    def __init__(self):
        pass


class Intro:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.running = True
        self.stage = None
        self.TeamSalvato = pygame.image.load(resource_path('assets/teamsalvato.png')).convert_alpha()  # noqa: E501
        self.ddcc = pygame.image.load(resource_path('assets/ddcc.png')).convert_alpha()  # noqa: E501
        self.image_width = self.TeamSalvato.get_width()
        self.image_height = self.TeamSalvato.get_height()
        self.alpha = 0
        self.flip = False
        self.warning = False
        self.stage = 0
        self.reset = False
        self.stages = {
            0: self.loading,
            1: self.menu
        }

    def run(self):
        while self.running:
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.stage = self.stages[self.stage]()

            pygame.display.flip()

    def menu(self):
        if not self.reset:
            self.alpha = 0
            self.flip = False
            self.warning = False
            self.reset = True

        self.ddcc.set_alpha(self.alpha)
        if self.alpha < 255:
            self.alpha += 10

        screen.blit(self.ddcc, (0, 0))

        return self.stage

    def loading(self):
        self.TeamSalvato.set_alpha(self.alpha)
        if self.alpha < 0:
            return self.stage + 1
        elif self.alpha < 255 and not self.flip:
            self.alpha += 4
        elif self.alpha >= 255 and not self.flip:
            self.flip = True
        elif self.flip and self.alpha > 0:
            self.alpha -= 5

        screen.fill((255, 255, 255))
        center_x = (SCREEN_WIDTH - self.image_width) // 2
        center_y = (SCREEN_HEIGHT - self.image_height) // 2
        screen.blit(self.TeamSalvato, (center_x, center_y))

        return self.stage


if __name__ == "__main__":
    intro = Intro()
    game = Game()
    intro.run()

pygame.quit()
sys.exit()
