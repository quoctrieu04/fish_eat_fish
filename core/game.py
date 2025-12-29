import pygame
from config.settings import *
from maps.lobby import Lobby
from maps.select_fish import SelectFish
from core.game_scene import GameScene


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT)
        )
        pygame.display.set_caption("Fish Eat Fish")
        self.clock = pygame.time.Clock()
        self.running = True

    def run(self):
        scene = "LOBBY"
        selected_fish = None

        while self.running:
            if scene == "LOBBY":
                lobby = Lobby(self.screen)
                result = lobby.run()

                if result == 1:
                    scene = "SELECT_FISH"
                elif result is None:
                    self.running = False

            elif scene == "SELECT_FISH":
                select_fish = SelectFish(self.screen)
                result = select_fish.run()

                if result:
                    selected_fish = result
                    scene = "GAME"
                else:
                    scene = "LOBBY"

            elif scene == "GAME":
                game_scene = GameScene(self.screen, selected_fish)
                game_scene.run()
                scene = "LOBBY"

            self.clock.tick(60)

        pygame.quit()
        quit()
