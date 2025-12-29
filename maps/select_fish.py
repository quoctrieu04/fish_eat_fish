import pygame
import os
from config.settings import *
from utils.button import Button
from entities.player import Player


class SelectFish:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()

        # ===== BACKGROUND =====
        self.bg = pygame.image.load(
            os.path.join("assets", "backgrounds", "select_fish.png")
        ).convert()
        self.bg = pygame.transform.scale(
            self.bg, (SCREEN_WIDTH, SCREEN_HEIGHT)
        )

        # ===== VỊ TRÍ =====
        self.pedestal_positions = [
            (SCREEN_WIDTH // 2 - 260, SCREEN_HEIGHT // 2 + 160),  # bệ trái
            (SCREEN_WIDTH // 2 + 230, SCREEN_HEIGHT // 2 + 160),  # bệ phải
        ]

        # vị trí trung tâm khi được chọn
        self.center_position = (
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 + 40
        )

        # ===== PREVIEW PLAYERS =====
        self.players = []
        for i, pos in enumerate(self.pedestal_positions):
            p = Player(pos[0], pos[1], fish_index=i)
            p.speed = 0  # không cho di chuyển

            # scale preview
            p.base_scale = 1.4
            p.scale = p.base_scale
            p._rescale_parts()

            self.players.append(p)

        self.selected_index = None

        # ===== FONT =====
        self.font = pygame.font.Font(
            "assets/fonts/BeVietnamPro-Bold.ttf", 26
        )

        # ===== BUTTON =====
        self.start_btn = Button(
            SCREEN_WIDTH - 180, SCREEN_HEIGHT - 70,
            150, 45,
            "Start", self.font,
            (60, 180, 90), (40, 150, 70),
            rounded=16
        )

        self.back_btn = Button(
            30, SCREEN_HEIGHT - 70,
            150, 45,
            "Back", self.font,
            (200, 60, 60), (160, 40, 40),
            rounded=16
        )

    # ==================================================
    # CẬP NHẬT VỊ TRÍ CÁ
    # ==================================================
    def update_positions(self):
        for i, player in enumerate(self.players):
            if i == self.selected_index:
                player.base_scale = 3
                player.rect.center = self.center_position
            else:
                player.base_scale = 1.4
                player.rect.center = self.pedestal_positions[i]
            player.scale =player.base_scale
            player._rescale_parts() 

    # ==================================================
    # RUN
    # ==================================================
    def run(self):
        running = True
        while running:
            self.clock.tick(60)

            # ===== DRAW BG =====
            self.screen.blit(self.bg, (0, 0))

            # ===== UPDATE POSITIONS =====
            self.update_positions()

            # ===== UPDATE + DRAW FISH =====
            for player in self.players:
                player.update()      # giữ quẫy đuôi
                player.draw(self.screen,pygame.Vector2(0, 0))

            # ===== BUTTON =====
            self.start_btn.update_hover_effect()
            self.back_btn.update_hover_effect()
            self.start_btn.draw(self.screen)
            self.back_btn.draw(self.screen)

            # ===== EVENT =====
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for i, player in enumerate(self.players):
                            if player.rect.collidepoint(event.pos):
                                self.selected_index = i

                if self.start_btn.is_clicked(event):
                    return self.selected_index

                if self.back_btn.is_clicked(event):
                    return None

            pygame.display.flip()
