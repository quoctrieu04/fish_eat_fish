import pygame
import random
import math
import os

# ==================================================
# CẤU HÌNH CÁC LOẠI MỒI
# ==================================================
ENEMY_TYPES = [
    {
        "name": "small_fish",
        "folder": "fish_1",
        "face": "left",
        "scale": (0.40, 0.45),
        "speed": (1, 2),
        "tail_speed": (0.010, 0.018),
        "tail_anchor": {"x": 0.01, "y": 0.50},
        "score": 10,
    },
    {
        "name": "shark",
        "folder": "fish_2",
        "face": "right",
        "scale": (1.2, 1.5),
        "speed": (1, 1),
        "tail_speed": (0.01, 0.02),
        "tail_anchor": {"x": -0.09, "y": 0.4},
        "score": 50,
    },
    {
        "name": "fast_fish",
        "folder": "fish_3",
        "face": "right",
        "scale": (0.22, 0.28),
        "speed": (1, 2),
        "tail_speed": (0.015, 0.020),
        "tail_anchor": {"x": 0.01, "y": 0.50},
        "score": 5,
    },
    {
        "name": "fish_04",
        "folder": "fish_4",
        "face": "right",
        "scale": (0.22, 0.28),
        "speed": (1, 2),
        "tail_speed": (0.015, 0.020),
        "tail_anchor": {"x": 0.01, "y": 0.50},
        "score": 2,
    },
    {
        "name": "fish_05",
        "folder": "fish_5",
        "face": "right",
        "scale": (0.5, 0.55),
        "speed": (1, 2),
        "tail_speed": (0.015, 0.020),
        "tail_anchor": {"x": 0.01, "y": 0.50},
        "score": 10,
    },
    {
        "name": "fish_06",
        "folder": "fish_6",
        "face": "right",
        "scale": (2.0, 2.2),
        "speed": (1, 2),
        "tail_speed": (0.015, 0.020),
        "tail_anchor": {"x": -0.03, "y": 0.55},
        "score": 100,
    },
    {
        "name": "fish_07",
        "folder": "fish_7",
        "face": "right",
        "scale": (0.6, 0.65),
        "speed": (1, 2),
        "tail_speed": (0.015, 0.020),
        "tail_anchor": {"x": 0.01, "y": 0.50},
        "score": 5,
    },
    {
        "name": "fish_08",
        "folder": "fish_8",
        "face": "right",
        "scale": (0.22, 0.28),
        "speed": (1, 2),
        "tail_speed": (0.015, 0.020),
        "tail_anchor": {"x": 0.01, "y": 0.50},
        "score": 10,
    },
    {
        "name": "fish_09",
        "folder": "fish_9",
        "face": "right",
        "scale": (0.4, 0.45),
        "speed": (1, 2),
        "tail_speed": (0.015, 0.020),
        "tail_anchor": {"x": 0.01, "y": 0.50},
        "score": 20,
    },
    {
        "name": "fish_10",
        "folder": "fish_10",
        "face": "left",
        "scale": (0.22, 0.28),
        "speed": (1, 2),
        "tail_speed": (0.015, 0.020),
        "tail_anchor": {"x": 0.01, "y": 0.50},
        "score": 4,
    },
]


class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed_range, player_pos):
        super().__init__()

        # ===== CHỌN LOẠI CÁ =====
        self.type = random.choice(ENEMY_TYPES)
        fish_path = os.path.join("assets", "enemies", self.type["folder"])

        # ===== LOAD ẢNH =====
        self.body_img = pygame.image.load(
            os.path.join(fish_path, "body.png")
        ).convert_alpha()
        self.tail_img = pygame.image.load(
            os.path.join(fish_path, "tail.png")
        ).convert_alpha()

        # ===== CHUẨN HÓA HƯỚNG (ẢNH GỐC → QUAY PHẢI) =====
        if self.type["face"] == "left":
            self.body_img = pygame.transform.flip(self.body_img, True, False)
            self.tail_img = pygame.transform.flip(self.tail_img, True, False)

        # ===== SCALE =====
        self.scale = random.uniform(*self.type["scale"])

        # 🔑 SIZE DÙNG LOGIC
        self.size = self.scale

        # 🔑 SIZE HIỂN THỊ (5, 10, 50...)
        self.size_value = int(self.scale * 10)

        # 🔑 ĐIỂM
        self.score = self.type["score"]

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

        self.tail_anchor = self.type["tail_anchor"]

        # ===== SPAWN QUANH PLAYER =====
        dist = random.randint(500, 800)
        angle = random.uniform(0, math.tau)

        self.pos = pygame.Vector2(
            player_pos[0] + dist * math.cos(angle),
            player_pos[1] + dist * math.sin(angle),
        )

        self.rect = self.body.get_rect(center=self.pos)

        # ===== HƯỚNG BƠI =====
        self.direction = -1 if self.pos.x > player_pos[0] else 1
        self.speed = random.randint(*self.type["speed"])

        # ===== ANIMATION =====
        self.tail_speed = random.uniform(*self.type["tail_speed"])

    # ==================================================
    # UPDATE
    # ==================================================
    def update(self):
        self.pos.x += self.speed * self.direction
        self.pos.y += math.sin(pygame.time.get_ticks() * 0.003) * 0.6
        self.rect.center = self.pos

    # ==================================================
    # DRAW
    # ==================================================
    def draw(self, screen, camera_offset):
        angle = math.sin(pygame.time.get_ticks() * self.tail_speed) * 15
        tail_rot = pygame.transform.rotate(self.tail, angle)

        w = self.body.get_width() + self.tail.get_width() + 20
        h = max(self.body.get_height(), self.tail.get_height())
        surf = pygame.Surface((w, h), pygame.SRCALPHA)

        center_y = h // 2

        body_x = self.tail.get_width()
        body_y = center_y - self.body.get_height() // 2
        surf.blit(self.body, (body_x, body_y))

        attach_x = body_x + int(self.body.get_width() * self.tail_anchor["x"])
        attach_y = body_y + int(self.body.get_height() * self.tail_anchor["y"])

        tail_rect = tail_rot.get_rect(center=(attach_x, attach_y))
        surf.blit(tail_rot, tail_rect)

        if self.direction == -1:
            surf = pygame.transform.flip(surf, True, False)

        screen.blit(
            surf,
            surf.get_rect(center=self.rect.center - camera_offset)
        )
