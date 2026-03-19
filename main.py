import pygame
import sys
import shutil
import os

DEV_MODE = False

pygame.init()

display_info = pygame.display.Info()
SCREEN_WIDTH = display_info.current_w
SCREEN_HEIGHT = display_info.current_h
FPS = 30

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Doki Doki Literature C*nts")

riffic38 = pygame.font.Font('assets/RifficFree-Bold.ttf', 38)
riffic30 = pygame.font.Font('assets/RifficFree-Bold.ttf', 30)


def resource_path(path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, path)
    return os.path.join(path)


class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.running = True
        self.Name = pygame.image.load(
            resource_path('assets/name.png')).convert_alpha()

        self.Old_ddcc = pygame.image.load(
            resource_path('assets/old_ddcc.png')).convert_alpha()
        
        ddcc_width, ddcc_height = self.Old_ddcc.get_size()
        ddcc_scale = min(
            SCREEN_WIDTH / ddcc_width, SCREEN_HEIGHT / ddcc_height)
        self.Old_ddcc = pygame.transform.smoothscale(
            self.Old_ddcc,
            (int(ddcc_width * ddcc_scale), int(ddcc_height * ddcc_scale)),
        )
        self.Old_ddcc_rect = self.Old_ddcc.get_rect(center=(SCREEN_WIDTH // 2,
                                                    SCREEN_HEIGHT // 2))

        self.stage = 0
        self.stages = {
            0: self.NameInputStart,
            1: self.NameInput
        }
        self.playername = ""
        self.Name_width = self.Name.get_width()
        self.Name_height = self.Name.get_height()
        self.Name_rect = self.Name.get_rect(center=(SCREEN_WIDTH // 2,
                                                    SCREEN_HEIGHT // 2))
        self.overlay = pygame.Surface(
            (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 128))  # 128 = 50% opacity

        self.Nametxt = riffic30.render("" , True, (0,0,0))
        self.Nametxt_width = self.Nametxt.get_width()
        self.Nametxt_height = self.Nametxt.get_height()
        self.Nametxt_rect = self.Nametxt.get_rect(center=(SCREEN_WIDTH // 2,
                                                    SCREEN_HEIGHT // 2))

    def run(self):
        while self.running:
            self.clock.tick(FPS)

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

            self.stages[self.stage](events)
            if len(self.playername) >= 15:
                self.old_ddcc()
            
            screen.blit(self.Name, self.Name_rect)
            screen.blit(self.Nametxt, self.Nametxt_rect)

            pygame.display.flip()

    def NameInput(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                key = event.key
                if key >= pygame.K_a and key <= pygame.K_z:
                    self.playername += chr(key)
                elif key == pygame.K_BACKSPACE:
                    self.playername = self.playername[:len(self.playername)-1]
                
                self.Nametxt = riffic30.render(self.playername, True, (0,0,0))
                self.Nametxt_width = self.Nametxt.get_width()
                self.Nametxt_height = self.Nametxt.get_height()
                self.Nametxt_rect = self.Nametxt.get_rect(center=(SCREEN_WIDTH // 2,
                                                            SCREEN_HEIGHT // 2))
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.playername.lower() != "angad":
                    self.Nametxt = riffic38.render("Stupid name", True, (255,0,0))
                else:
                    self.Nametxt = riffic38.render("Smart name", True, (0,255,0))
                self.Nametxt_width = self.Nametxt.get_width()
                self.Nametxt_height = self.Nametxt.get_height()
                self.Nametxt_rect = self.Nametxt.get_rect(center=(SCREEN_WIDTH // 2,
                                                            SCREEN_HEIGHT // 2))

    def NameInputStart(self, _):
        screen.blit(self.overlay, (0, 0))
        screen.blit(self.Name, self.Name_rect)
        self.stage += 1

    def old_ddcc(self):
        screen.blit(self.Old_ddcc, self.Old_ddcc_rect)
        screen.blit(self.overlay, (0, 0))


class Intro:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.running = True
        self.stage = None
        self.TeamSalvato = pygame.image.load(
            resource_path('assets/teamsalvato.png')).convert_alpha()
        self.ddcc = pygame.image.load(
            resource_path('assets/ddcc.png')).convert_alpha()

        # Scale the DDCC splash to fit the current display
        ddcc_width, ddcc_height = self.ddcc.get_size()
        ddcc_scale = min(
            SCREEN_WIDTH / ddcc_width, SCREEN_HEIGHT / ddcc_height)
        self.ddcc = pygame.transform.smoothscale(
            self.ddcc,
            (int(ddcc_width * ddcc_scale), int(ddcc_height * ddcc_scale)),
        )
        self.ddcc_rect = self.ddcc.get_rect(center=(SCREEN_WIDTH // 2,
                                                    SCREEN_HEIGHT // 2))

        self.image_width = self.TeamSalvato.get_width()
        self.image_height = self.TeamSalvato.get_height()
        self.alpha = 0
        self.flip = False
        self.warning = False
        self.stage = 0
        self.reset = False
        self.hovering = False
        self.stages = {
            0: self.loading,
            1: self.menu,
            2: self.next
        }

    def run(self):
        while self.running:
            self.clock.tick(FPS)

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

            next_stage = self.stages[self.stage](events) or self.stage
            if next_stage != self.stage:
                self.stage = next_stage
            if next_stage == 2:
                return

            pygame.display.flip()

    def menu(self, events):
        if not self.reset:
            self.alpha = 0
            self.flip = False
            self.warning = False
            self.reset = True

        self.ddcc.set_alpha(self.alpha)
        if self.alpha < 255:
            self.alpha += 10

        screen.fill((0, 0, 0))
        screen.blit(self.ddcc, self.ddcc_rect)

        mouse_pos = pygame.mouse.get_pos()

        base_color = (255, 192, 203)      # pink
        glow_color = (255, 210, 210)      # lighter pink glow

        play_text = riffic38.render("Play", True, base_color)
        play_rect = play_text.get_rect()

        play_rect.topleft = (
            self.ddcc_rect.left + 48,
            self.ddcc_rect.centery - play_rect.height // 2,
        )

        # Hover detection
        self.hovering = play_rect.collidepoint(mouse_pos)

        if self.hovering:
            play_text = riffic38.render("Play", True, glow_color)

            # glow effect (draw multiple offsets)
            for dx in (-1, 1):
                for dy in (-1, 1):
                    glow = riffic38.render("Play", True, glow_color)
                    screen.blit(glow, (play_rect.x + dx, play_rect.y + dy))

            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.stage = self.stage + 1

        # main text
        screen.blit(play_text, play_rect)

        return self.stage

    def loading(self, events):
        self.TeamSalvato.set_alpha(self.alpha)

        if not self.flip:
            # Fade in
            if self.alpha < 255:
                self.alpha += 4 if not DEV_MODE else 15
            else:
                self.flip = True
        else:
            # Fade out
            if self.alpha > 0:
                self.alpha -= 5 if not DEV_MODE else 13
            else:
                return self.stage + 1

        screen.fill((255, 255, 255))
        center_x = (SCREEN_WIDTH - self.image_width) // 2
        center_y = (SCREEN_HEIGHT - self.image_height) // 2
        screen.blit(self.TeamSalvato, (center_x, center_y))

        return self.stage

    def next(self, events):
        return 5


class Compiler:
    def __init__(self):
        self.story = []
        self.storyf = None
        self.stats = {
            "routes": 0,
            "dialog": 0
        }

        if os.path.exists("story/story.ddc"):
            self.storyf = "story/story.ddc"

    def compile(self, path):
        if not self.storyf:
            self.storyf = path

        with open(self.storyf, 'r') as story:
            lines = story.readlines()
            for line in lines:
                actions = line.split('|')
                self.story.extend(actions)

        print(self.story)


if __name__ == "__main__":
    print("Compiling story... please wait...")

    src = resource_path("story/story.ddc")
    dst = os.path.join(os.getcwd(), "story.ddc")

    if not os.path.exists(dst) and not DEV_MODE:
        shutil.copy(src, dst)

    compiler = Compiler()
    compiler.compile(resource_path('story/story.ddc'))

    print("Finished!")

    intro = Intro()
    game = Game()
    intro.run()
    game.run()

pygame.quit()
sys.exit()
