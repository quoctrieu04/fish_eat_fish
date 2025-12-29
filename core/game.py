# core/game.py
import pygame
from config.settings import *
from maps.lobby import Lobby
from core.game_scene import GameScene


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT)
        )
        pygame.display.set_caption("Fish Eat Fish")
        self.clock = pygame.time.Clock()

    def run(self):
        while True:
            # ===== MENU =====
            lobby = Lobby(self.screen)
            mode = lobby.run()   # nhận 1 hoặc 2 hoặc None

            # ===== 1 NGƯỜI CHƠI =====
            if mode == 1:
                game_scene = GameScene(self.screen)
                game_scene.run()

            # (sau này mở rộng)
            # if mode == 2:
            #     GameScene(self.screen, mode=2).run()
