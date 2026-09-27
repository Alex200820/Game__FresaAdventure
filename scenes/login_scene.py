import pygame
import math
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, COLORS
from background import MenuBackground


class LoginScene:
    def __init__(self, game):
        self.game = game
        self.bg = MenuBackground(game)
        self.font_large = pygame.font.Font(None, 52)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 20)
        self.player_name = ""
        self.active = True
        self.error = ""
        self.blink_timer = 0
        self.show_cursor = True

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if len(self.player_name.strip()) > 0:
                    self.game.player_name = self.player_name.strip()
                    self.game.change_state('level_select')
                else:
                    self.error = "Por favor ingresa un nombre"
            elif event.key == pygame.K_BACKSPACE:
                self.player_name = self.player_name[:-1]
                self.error = ""
            elif event.key == pygame.K_ESCAPE:
                return False
            else:
                unicode_char = getattr(event, 'unicode', '')
                if len(self.player_name) < 15 and unicode_char and unicode_char.isprintable():
                    self.player_name += unicode_char
                    self.error = ""

    def update(self, dt):
        self.blink_timer += dt
        if self.blink_timer > 0.5:
            self.blink_timer = 0
            self.show_cursor = not self.show_cursor

    def draw(self, surface):
        self.bg.draw(surface, 1 / 60)

        title = self.font_large.render("Fresa Adventure \u2727", True, COLORS['deep_pink'])
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 130))
        surface.blit(title, title_rect)

        subtitle = self.font_small.render("\u00bfC\u00f3mo te llamas?", True, COLORS['text'])
        sub_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, 185))
        surface.blit(subtitle, sub_rect)

        box_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, 215, 300, 50)
        pygame.draw.rect(surface, COLORS['white'], box_rect, border_radius=12)
        pygame.draw.rect(surface, COLORS['hot_pink'], box_rect, 3, border_radius=12)

        display_name = self.player_name
        if self.show_cursor:
            display_name += "|"
        name_text = self.font_medium.render(display_name, True, COLORS['text'])
        name_rect = name_text.get_rect(center=(SCREEN_WIDTH // 2, 240))
        surface.blit(name_text, name_rect)

        if self.error:
            err_text = self.font_small.render(self.error, True, COLORS['deep_pink'])
            err_rect = err_text.get_rect(center=(SCREEN_WIDTH // 2, 285))
            surface.blit(err_text, err_rect)
        else:
            hint = self.font_small.render("Presiona Enter para empezar", True, COLORS['text_light'])
            hint_rect = hint.get_rect(center=(SCREEN_WIDTH // 2, 285))
            surface.blit(hint, hint_rect)

        self._draw_decoration(surface)

    def _draw_decoration(self, surface):
        t = pygame.time.get_ticks() / 1000
        cx, cy = SCREEN_WIDTH // 2, 355
        for i in range(6):
            angle = t + (i * math.pi * 2 / 6)
            x = cx + int(40 * math.cos(angle))
            y = cy + int(15 * math.sin(angle * 2))
            colors = [COLORS['strawberry'], COLORS['flower_pink'],
                      COLORS['flower_yellow'], COLORS['flower_white'],
                      COLORS['hot_pink'], COLORS['pink']]
            pygame.draw.circle(surface, colors[i], (x, y), 6)
