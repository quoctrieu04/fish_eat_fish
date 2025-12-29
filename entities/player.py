import pygame
import math
import os


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, fish_index=0):
        super().__init__()

        # ===== LOAD BODY & TAIL THEO CÁ ĐƯỢC CHỌN =====
        fish_path = os.path.join(
            "assets", "player", f"fish_{fish_index + 1}"
        )

        self.body_img = pygame.image.load(
            os.path.join(fish_path, "body.png")
        ).convert_alpha()

        self.tail_img = pygame.image.load(
            os.path.join(fish_path, "tail.png")
        ).convert_alpha()

        # ===== SCALE =====
        self.base_scale = 1.0
        self.scale = self.base_scale
        self.score = 0

        self._rescale_parts()

        # ===== POSITION (WORLD POSITION) =====
        self.rect = self.body.get_rect(center=(x, y))

        # ===== MOVEMENT =====
        self.speed = 5
        self.direction = 1   # 1 = phải, -1 = trái

        # ===== TAIL ANIMATION =====
        self.tail_speed = 0.012

    # ==================================================
    # SCALE BODY + TAIL
    # ==================================================
    def _rescale_parts(self):
        self.body = pygame.transform.smoothscale(
            self.body_img,
            (
                int(self.body_img.get_width() * self.scale),
                int(self.body_img.get_height() * self.scale),
            ),
        )

        self.tail = pygame.transform.smoothscale(
            self.tail_img,
            (
                int(self.tail_img.get_width() * self.scale),
                int(self.tail_img.get_height() * self.scale),
            ),
        )

    # ==================================================
    # KHI ĂN MỒI → CÁ TO DẦN
    # ==================================================
    def grow(self, amount=1):
        self.score += amount
        self.scale = min(self.base_scale + self.score * 0.03, 1.35)

        center = self.rect.center
        self._rescale_parts()
        self.rect = self.body.get_rect(center=center)

    # ==================================================
    # UPDATE LOGIC (KHÔNG CLAMP)
    # ==================================================
    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            self.direction = -1

        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            self.direction = 1

        if keys[pygame.K_UP]:
            self.rect.y -= self.speed

        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

    # ==================================================
    # DRAW PLAYER (THEO CAMERA OFFSET)
    # ==================================================
    def draw(self, screen, offset):
        angle = math.sin(
            pygame.time.get_ticks() * self.tail_speed
        ) * 18

        tail_rot = pygame.transform.rotate(self.tail, angle)

        w = self.body.get_width() + self.tail.get_width()
        h = max(self.body.get_height(), self.tail.get_height())
        surf = pygame.Surface((w, h), pygame.SRCALPHA)

        center_y = h // 2
        tail_offset_y = int(self.body.get_height() * 0.05)
        pivot_x = int(self.tail.get_width() * 0.9)

        tail_rect = tail_rot.get_rect()
        tail_rect.center = (
            pivot_x,
            center_y + tail_offset_y
        )

        body_x = pivot_x + 4
        body_y = center_y - self.body.get_height() // 2

        surf.blit(tail_rot, tail_rect)
        surf.blit(self.body, (body_x, body_y))

        if self.direction == -1:
            surf = pygame.transform.flip(surf, True, False)

        screen.blit(
            surf,
            surf.get_rect(center=self.rect.center - offset)
        )
