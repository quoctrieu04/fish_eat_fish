import pygame
import math
import os


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, fish_index=0):
        super().__init__()

        # ===== LOAD BODY & TAIL =====
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
        self.max_scale = 2.5        # to tối đa
        self.score = 0

        self._rescale_parts()

        # ===== POSITION =====
        self.rect = self.body.get_rect(center=(x, y))

        # ===== MOVEMENT =====
        self.speed = 5
        self.vel = pygame.Vector2(0, 0)

        self.angle = 0
        self.angle_target = 0
        self.facing = 1     # 1 = phải, -1 = trái

        # ===== TAIL ANIMATION =====
        self.tail_speed = 0.012

        # ===== SIZE (LOGIC) =====
        self.size = self.scale

    # ==================================================
    # SCALE BODY + TAIL
    # ==================================================
    def _rescale_parts(self):
        self.body = pygame.transform.smoothscale(
            self.body_img,
            (
                int(self.body_img.get_width() * self.scale),
                int(self.body_img.get_height() * self.scale),
            )
        )

        self.tail = pygame.transform.smoothscale(
            self.tail_img,
            (
                int(self.tail_img.get_width() * self.scale),
                int(self.tail_img.get_height() * self.scale),
            )
        )

    # ==================================================
    # KHI ĂN MỒI → TO DẦN
    # ==================================================
    def grow(self, enemy_size, enemy_score):
        self.score += enemy_score

        # to dần theo size mồi
        self.scale += enemy_size * 0.03
        self.scale = min(self.scale, self.max_scale)
        self.size = self.scale

        center = self.rect.center
        self._rescale_parts()
        self.rect = self.body.get_rect(center=center)

    # ==================================================
    # UPDATE LOGIC (KHÔNG NGỬA BỤNG)
    # ==================================================
    def update(self):
        keys = pygame.key.get_pressed()
        self.vel.update(0, 0)

        if keys[pygame.K_LEFT]:
            self.vel.x = -1
            self.facing = -1
        if keys[pygame.K_RIGHT]:
            self.vel.x = 1
            self.facing = 1
        if keys[pygame.K_UP]:
            self.vel.y = -1
        if keys[pygame.K_DOWN]:
            self.vel.y = 1

        if self.vel.length() > 0:
            self.vel = self.vel.normalize()
            self.rect.center += self.vel * self.speed

            # góc xoay ±90° (không lật bụng)
            self.angle_target = -math.degrees(
                math.atan2(self.vel.y, abs(self.vel.x))
            )
        else:
            self.angle_target = 0

        # xoay mượt
        self.angle += (self.angle_target - self.angle) * 0.15

    # ==================================================
    # DRAW PLAYER
    # ==================================================
    def draw(self, screen, offset):
        # ===== VẪY ĐUÔI =====
        tail_angle = math.sin(
            pygame.time.get_ticks() * self.tail_speed
        ) * 18

        tail_rot = pygame.transform.rotate(self.tail, tail_angle)

        # ===== GHÉP BODY + TAIL =====
        w = self.body.get_width() + self.tail.get_width()
        h = max(self.body.get_height(), self.tail.get_height())
        surf = pygame.Surface((w, h), pygame.SRCALPHA)

        center_y = h // 2
        pivot_x = int(self.tail.get_width() * 0.9)

        tail_rect = tail_rot.get_rect(
            center=(pivot_x, center_y)
        )

        body_x = pivot_x + 4
        body_y = center_y - self.body.get_height() // 2

        surf.blit(tail_rot, tail_rect)
        surf.blit(self.body, (body_x, body_y))

        # ===== XOAY LÊN / XUỐNG =====
        surf = pygame.transform.rotate(surf, self.angle)

        # ===== QUAY TRÁI / PHẢI (KHÔNG LẬT BỤNG) =====
        if self.facing == -1:
            surf = pygame.transform.flip(surf, True, False)

        screen.blit(
            surf,
            surf.get_rect(center=self.rect.center - offset)
        )

    # ==================================================
    # GIÁ TRỊ KÍCH THƯỚC HIỂN THỊ (10, 20, 50...)
    # ==================================================
    @property
    def size_value(self):
        return int(self.scale * 10)
