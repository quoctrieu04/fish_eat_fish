import pygame
import os
import math
from config.settings import *
from utils.button import Button


class Lobby:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()

        # ===== LOAD BACKGROUND =====
        bg_path = os.path.join("assets", "backgrounds", "lobby.png")
        self.background = pygame.image.load(bg_path).convert()
        self.background = pygame.transform.scale(
            self.background,
            (SCREEN_WIDTH, SCREEN_HEIGHT)
        )

        # ===== LOAD ICON =====
        icon_path = os.path.join("assets", "icons", "fishicon.png")
        self.icon = pygame.image.load(icon_path).convert_alpha()
        self.icon = pygame.transform.smoothscale(self.icon, (32, 32))

        # ===== FONT =====
        font_path = "assets/fonts/BeVietnamPro-Bold.ttf"
        self.font_title = pygame.font.Font(font_path, 56)
        self.font_btn = pygame.font.Font(font_path, 30)

        # ===== ANIMATION =====
        self.alpha = 0
        self.slide_y = -40
        self.fade_speed = 6

        # ===== BUTTON LAYOUT =====
        BTN_W, BTN_H = 240, 55
        GAP = 40

        total_width = BTN_W * 2 + GAP
        start_x = SCREEN_WIDTH // 2 - total_width // 2
        left_x = start_x
        right_x = start_x + BTN_W + GAP

        row1_y = 220
        row2_y = 290

        self.buttons = []

        self.btn1_player_btn = Button(
            left_x, row1_y, BTN_W, BTN_H,
            "1 Player", self.font_btn,
            BLUE, DARK_BLUE,
            rounded=16,
            icon=self.icon
        )

        self.btn2_player_btn = Button(
            right_x, row1_y, BTN_W, BTN_H,
            "2 Player", self.font_btn,
            BLUE, DARK_BLUE,
            rounded=16,
            icon=self.icon
        )

        self.setting_btn = Button(
            left_x, row2_y, BTN_W, BTN_H,
            "Setting", self.font_btn,
            (200, 60, 60), (160, 40, 40),
            rounded=16,
            icon=self.icon
        )

        self.exit_btn = Button(
            right_x, row2_y, BTN_W, BTN_H,
            "Exit", self.font_btn,
            BLUE, DARK_BLUE,
            rounded=16,
            icon=self.icon
        )

        self.buttons = [
            self.btn1_player_btn,
            self.btn2_player_btn,
            self.setting_btn,
            self.exit_btn
        ]

    def run(self):
        running = True
        while running:
            self.clock.tick(60)

            # ===== BACKGROUND =====
            self.screen.blit(self.background, (0, 0))

            # ===== FADE + SLIDE =====
            if self.alpha < 255:
                self.alpha += self.fade_speed
                self.slide_y += 2

            # ===== TITLE =====
            title = self.font_title.render(
                "CÁ LỚN NUỐT CÁ BÉ",
                True,
                WHITE
            )
            title.set_alpha(self.alpha)
            self.screen.blit(
                title,
                title.get_rect(center=(SCREEN_WIDTH // 2, 130 + self.slide_y))
            )

            # ===== BUTTONS =====
            for btn in self.buttons:
                btn.update_hover_effect()
                btn.draw(self.screen, offset_y=self.slide_y, alpha=self.alpha)

            # ===== EVENTS =====
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if self.btn1_player_btn.is_clicked(event):
                    return 1

                if self.btn2_player_btn.is_clicked(event):
                    print("👉 2 Player")
                    running = False

                if self.setting_btn.is_clicked(event):
                    print("👉 Setting")
                    running = False

                if self.exit_btn.is_clicked(event):
                    pygame.quit()
                    quit()

            pygame.display.flip()
