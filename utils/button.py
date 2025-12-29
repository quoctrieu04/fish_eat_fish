import pygame
import math


class Button:
    def __init__(
        self,
        x, y, w, h,
        text,
        font,
        color,
        hover_color,
        rounded=0,
        icon=None
    ):
        self.rect = pygame.Rect(x, y, w, h)
        self.base_rect = self.rect.copy()

        self.text = text
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.rounded = rounded
        self.icon = icon

        self.hovered = False
        self.scale = 1.0
        self.shake_offset = 0
        self.shake_time = 0

        self.text_surf = self.font.render(self.text, True, (255, 255, 255))

    def update_hover_effect(self):
        mouse_pos = pygame.mouse.get_pos()
        self.hovered = self.rect.collidepoint(mouse_pos)

        if self.hovered:
            self.scale = min(self.scale + 0.05, 1.08)
            self.shake_time += 1
            self.shake_offset = math.sin(self.shake_time * 0.6) * 2
        else:
            self.scale = max(self.scale - 0.05, 1.0)
            self.shake_offset = 0
            self.shake_time = 0

        # scale rect
        self.rect.width = int(self.base_rect.width * self.scale)
        self.rect.height = int(self.base_rect.height * self.scale)
        self.rect.center = self.base_rect.center

    def draw(self, screen, offset_y=0, alpha=255):
        # Button surface
        surf = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        draw_color = self.hover_color if self.hovered else self.color

        pygame.draw.rect(
            surf,
            draw_color,
            surf.get_rect(),
            border_radius=self.rounded
        )

        surf.set_alpha(alpha)

        # Icon
        text_x_offset = 0
        if self.icon:
            icon_rect = self.icon.get_rect()
            icon_rect.centery = surf.get_height() // 2
            icon_rect.x = 16
            surf.blit(self.icon, icon_rect)
            text_x_offset = icon_rect.width + 24

        # Text
        text_rect = self.text_surf.get_rect(
            center=(surf.get_width() // 2 + text_x_offset // 2,
                    surf.get_height() // 2)
        )
        surf.blit(self.text_surf, text_rect)

        screen.blit(
            surf,
            (self.rect.x + self.shake_offset,
             self.rect.y + offset_y)
        )

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                return True
        return False
