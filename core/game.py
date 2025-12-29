# core/game.py
import pygame
from config.settings import *
from maps.lobby import Lobby

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Fish Eat Fish")
        self.clock = pygame.time.Clock()

    def run(self):
        lobby = Lobby(self.screen)
        lobby.run()

        # Sau này bạn sẽ gọi:
        # self.play_game()

        while True:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
