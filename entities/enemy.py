# entities/enemy.py
import pygame
import random
import math


class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed_range):
        super().__init__()

        img_path = random.choice([
            "assets/enemies/ca6.png",
            "assets/enemies/cangua2.png",
            "assets/enemies/crad1.png",
        ])

        original = pygame.image.load(img_path).convert_alpha()

        # ===== SCALE CÁ (NHỎ LẠI) =====
        scale = random.uniform(0.35, 0.5)
        w = int(original.get_width() * scale)
        h = int(original.get_height() * scale)
        self.image = pygame.transform.smoothscale(original, (w, h))

        self.rect = self.image.get_rect()

        # ===== HƯỚNG BƠI =====
        self.direction = random.choice([-1, 1])  # -1: trái, 1: phải

        screen = pygame.display.get_surface()
        if self.direction == -1:
            self.rect.x = screen.get_width()
        else:
            self.rect.x = -self.rect.width

        self.base_y = random.randint(100, screen.get_height() - 100)
        self.rect.y = self.base_y

        self.speed = random.randint(*speed_range)

        # lật ảnh nếu bơi sang phải
        if self.direction == 1:
            self.image = pygame.transform.flip(self.image, True, False)

        # hiệu ứng lượn sóng
        self.wave_angle = random.uniform(0, math.pi * 2)

    def update(self):
        self.rect.x += self.speed * self.direction

        self.wave_angle += 0.05
        self.rect.y = self.base_y + int(12 * math.sin(self.wave_angle))

        screen = pygame.display.get_surface()
        if self.direction == -1 and self.rect.right < 0:
            self.kill()
        if self.direction == 1 and self.rect.left > screen.get_width():
            self.kill()
