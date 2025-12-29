import pygame
from config.settings import *
from entities.player import Player
from entities.enemy import Enemy
from core.maps_config import MAPS


class GameScene:
    def __init__(self, screen, fish_index=0):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.fish_index = fish_index

        self.font = pygame.font.Font(
            "assets/fonts/BeVietnamPro-Bold.ttf", 26
        )

        # ===== CAMERA (FREE) =====
        self.camera_offset = pygame.Vector2(0, 0)

        # ===== MAP =====
        self.map_index = 0
        self.map_data = MAPS[self.map_index]
        self.load_map()

        # ===== PLAYER (WORLD POSITION) =====
        self.player = Player(
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2,
            fish_index=self.fish_index
        )

        self.enemies = pygame.sprite.Group()
        self.spawn_timer = 0
        self.score = 0

    # ==================================================
    # LOAD MAP
    # ==================================================
    def load_map(self):
        self.background = pygame.image.load(
            self.map_data["background"]
        ).convert()

        self.spawn_rate = self.map_data["spawn_rate"]
        self.enemy_speed = self.map_data["enemy_speed"]

        self.camera_offset.update(0, 0)

    # ==================================================
    # UPDATE CAMERA (FREE – KHÔNG GIỚI HẠN)
    # ==================================================
    def update_camera(self):
        self.camera_offset.x = (
            self.player.rect.centerx - SCREEN_WIDTH // 2
        )
        self.camera_offset.y = (
            self.player.rect.centery - SCREEN_HEIGHT // 2
        )

    # ==================================================
    # DRAW BACKGROUND TILE (VÔ HẠN)
    # ==================================================
    def draw_tiled_background(self):
        bg_w, bg_h = self.background.get_size()

        offset_x = -self.camera_offset.x % bg_w
        offset_y = -self.camera_offset.y % bg_h

        for x in range(-bg_w, SCREEN_WIDTH + bg_w, bg_w):
            for y in range(-bg_h, SCREEN_HEIGHT + bg_h, bg_h):
                self.screen.blit(
                    self.background,
                    (x + offset_x, y + offset_y)
                )

    # ==================================================
    # RUN
    # ==================================================
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
                enemy = Enemy(self.enemy_speed,self.player.rect.center)
                self.enemies.add(enemy)
                self.spawn_timer = 0

            # ===== UPDATE =====
            self.player.update()
            self.enemies.update()
            self.update_camera()

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

            # ===== DRAW BACKGROUND (TILE) =====
            self.draw_tiled_background()

            # ===== DRAW ENEMY =====
            for enemy in self.enemies:
                enemy.draw(
                    self.screen,
                    self.camera_offset
                )   

            # ===== DRAW PLAYER =====
            self.player.draw(
                self.screen,
                self.camera_offset
            )

            # ===== UI (KHÔNG THEO CAMERA) =====
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
