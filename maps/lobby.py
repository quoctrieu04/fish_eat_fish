# maps/lobby.py
import pygame
import os
from config.settings import *
from utils.button import Button


class Lobby:
    def __init__(self, screen):
        self.screen = screen

        # ===== LOAD BACKGROUND =====
        bg_path = os.path.join("assets", "backgrounds", "lobby.png")
        self.background = pygame.image.load(bg_path).convert()
        self.background = pygame.transform.scale(
            self.background,
            (SCREEN_WIDTH, SCREEN_HEIGHT)
        )

        # ===== FONT =====
        font_path = "assets/fonts/BeVietnamPro-Bold.ttf"
        self.font_title = pygame.font.Font(font_path, 56)
        self.font_btn = pygame.font.Font(font_path, 30)
        
        self.btn1_player_btn = Button(
            x=SCREEN_WIDTH // 2 - 120,
            y=200,
            w=240,
            h=55,
            text="1 Player",
            font=self.font_btn,
            color=BLUE,
            hover_color=DARK_BLUE
        )
        self.btn2_player_btn = Button(
            x=SCREEN_WIDTH // 2 - 120,
            y=260,
            w=240,
            h=55,
            text="2 Player",
            font=self.font_btn,
            color=BLUE,
            hover_color=DARK_BLUE
        )

        # ===== BUTTON START =====
        self.exit_btn = Button(
            x=SCREEN_WIDTH // 2 - 120,
            y=320,
            w=240,
            h=55,
            text="Exit",
            font=self.font_btn,
            color=BLUE,
            hover_color=DARK_BLUE
        )

        # ===== BUTTON EXIT =====
        self.setting_btn = Button(
            x=SCREEN_WIDTH // 2 - 120,
            y=380,
            w=240,
            h=55,
            text="Setting",
            font=self.font_btn,
            color=(200, 60, 60),
            hover_color=(160, 40, 40)
        )
        

    def run(self):
        running = True
        while running:
            # ===== DRAW BACKGROUND =====
            self.screen.blit(self.background, (0, 0))

            # ===== TITLE =====
            title = self.font_title.render(
                "CÁ LỚN NUỐT CÁ BÉ",
                True,
                WHITE
            )
            self.screen.blit(
                title,
                title.get_rect(center=(SCREEN_WIDTH // 2, 140))
            )

            # ===== BUTTONS =====
            self.btn1_player_btn.draw(self.screen)
            self.btn2_player_btn.draw(self.screen)
            self.exit_btn.draw(self.screen)
            self.setting_btn.draw(self.screen)
            

            # ===== EVENTS =====
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                    
                if self.btn1_player_btn.is_clicked(event):
                   # print("👉 Chọn chế độ 1 người chơi")   
                    return 1   # sau này đổi sang scene chọn cá
                if self.btn2_player_btn.is_clicked(event):
                    print("👉 Chọn chế độ 2 người chơi")
                    running = False   # sau này đổi sang scene chọn cá
                    
                    
                if self.setting_btn.is_clicked(event):
                    print("Cài đặt")
                    running = False   # sau này đổi sang scene chọn cá

                if self.exit_btn.is_clicked(event):
                    pygame.quit()
                    quit()

            pygame.display.flip()
