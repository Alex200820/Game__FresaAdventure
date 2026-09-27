import pygame
import math
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, COLORS
from levels import LEVELS
from sprites import get_sprite, get_glow
from background import MenuBackground


class BonusIntroScene:
    def __init__(self, game):
        self.game = game
        self.bg = MenuBackground()
        self.font_title = pygame.font.Font(None, 46)
        self.font_medium = pygame.font.Font(None, 26)
        self.font_small = pygame.font.Font(None, 20)
        self.anim_timer = 0

    def _bonus_level(self):
        for lvl in LEVELS:
            if lvl.get('bonus'):
                return lvl
        return LEVELS[-1]

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self.game.change_state('game')

    def update(self, dt):
        self.anim_timer += dt

    def draw(self, surface):
        self.bg.draw(surface, 1 / 60)

        surf = get_sprite('strawberry')
        t = self.anim_timer
        for i in range(7):
            x = 60 + i * ((SCREEN_WIDTH - 120) // 6) + int(18 * math.sin(t * 2 + i * 1.2))
            y = 70 + int(16 * math.sin(t * 3 + i * 2))
            surface.blit(surf, (x, y))

        panel = pygame.Surface((520, 300), pygame.SRCALPHA)
        panel.fill((255, 250, 240, 235))
        panel_rect = panel.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        surface.blit(panel, panel_rect)
        pygame.draw.rect(surface, COLORS['hot_pink'], panel_rect, 4, border_radius=18)

        title = self.font_title.render("\u2605 Nivel Bonus \u2605", True, COLORS['gold'])
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, panel_rect.top + 45))
        surface.blit(title, title_rect)

        name = self._bonus_level()['name']
        name_text = self.font_medium.render(name, True, COLORS['deep_pink'])
        name_rect = name_text.get_rect(center=(SCREEN_WIDTH // 2, panel_rect.top + 90))
        surface.blit(name_text, name_rect)

        msg1 = self.font_small.render(
            "\u00a1Felicitaciones, recogiste todas las fresas!", True, COLORS['text'])
        msg1_rect = msg1.get_rect(center=(SCREEN_WIDTH // 2, panel_rect.top + 135))
        surface.blit(msg1, msg1_rect)

        msg2 = self.font_small.render(
            "En este nivel no es necesario recoger todas las fresas.",
            True, COLORS['text'])
        msg2_rect = msg2.get_rect(center=(SCREEN_WIDTH // 2, panel_rect.top + 162))
        surface.blit(msg2, msg2_rect)

        msg3 = self.font_small.render(
            "\u00a1Solo disfruta del paseo por el jard\u00edn secreto!",
            True, COLORS['hot_pink'])
        msg3_rect = msg3.get_rect(center=(SCREEN_WIDTH // 2, panel_rect.top + 195))
        surface.blit(msg3, msg3_rect)

        hint = self.font_small.render("Presiona Enter para comenzar", True, COLORS['deep_pink'])
        hint_rect = hint.get_rect(center=(SCREEN_WIDTH // 2, panel_rect.top + 250))
        surface.blit(hint, hint_rect)

        glow = get_glow(COLORS['heart'], 6)
        for i in range(4):
            hx = panel_rect.left + 30 + i * ((panel_rect.width - 60) // 3)
            hy = panel_rect.top + int(8 * math.sin(t * 4 + i))
            surface.blit(glow, (hx, hy))
