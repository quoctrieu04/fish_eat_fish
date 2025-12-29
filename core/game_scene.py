# core/game_scene.py
import pygame
from config.settings import *
from entities.player import Player
from entities.enemy import Enemy
from core.maps_config import MAPS


class GameScene:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()

        self.font = pygame.font.Font(
            "assets/fonts/BeVietnamPro-Bold.ttf", 26
        )

        # ===== MAP =====
        self.map_index = 0
        self.map_data = MAPS[self.map_index]
        self.load_map()

        # ===== PLAYER =====
        self.player = Player(
            SCREEN_WIDTH // 4,
            SCREEN_HEIGHT // 2
        )

        self.enemies = pygame.sprite.Group()

        self.spawn_timer = 0
        self.score = 0

    def load_map(self):
        self.background = pygame.image.load(
            self.map_data["background"]
        ).convert()

        self.background = pygame.transform.scale(
            self.background,
            (SCREEN_WIDTH, SCREEN_HEIGHT)
        )

        self.spawn_rate = self.map_data["spawn_rate"]
        self.enemy_speed = self.map_data["enemy_speed"]

    def run(self):
        running = True
        while running:
            self.clock.tick(FPS)

            # ===== EVENT =====
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

            # ===== SPAWN ENEMY =====
            self.spawn_timer += 1
            if self.spawn_timer >= self.spawn_rate:
                enemy = Enemy(self.enemy_speed)
                self.enemies.add(enemy)
                self.spawn_timer = 0

            # ===== UPDATE =====
            self.player.update()
            self.enemies.update()

            # ===== COLLISION =====
            hits = pygame.sprite.spritecollide(
                self.player, self.enemies, True
            )
            for _ in hits:
                self.score += 1
                self.player.grow(1)

            # ===== CHANGE MAP =====
            target = self.map_data["score_to_next"]
            if target and self.score >= target:
                self.map_index += 1
                if self.map_index < len(MAPS):
                    self.map_data = MAPS[self.map_index]
                    self.load_map()
                    self.enemies.empty()

            # ===== DRAW =====
            self.screen.blit(self.background, (0, 0))

            # Enemy
            for enemy in self.enemies:
                self.screen.blit(enemy.image, enemy.rect)

            # Player (body + tail)
            self.player.draw(self.screen)

            # UI
            self.screen.blit(
                self.font.render(f"Điểm: {self.score}", True, WHITE),
                (20, 20),
            )
            self.screen.blit(
                self.font.render(
                    f"Map {self.map_data['id']}",
                    True,
                    WHITE
                ),
                (20, 50),
            )

            pygame.display.flip()
