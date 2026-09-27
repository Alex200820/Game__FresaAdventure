import pygame
import math
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, COLORS
from levels import LEVELS
from sprites import get_sprite, get_glow
from background import MenuBackground


class VictoryScene:
    def __init__(self, game):
        self.game = game
        self.bg = MenuBackground()
        self.font_large = pygame.font.Font(None, 52)
        self.font_medium = pygame.font.Font(None, 28)
        self.font_small = pygame.font.Font(None, 18)
        self.anim_timer = 0
        self.strawberries_in_level = 0
        self.total_in_level = 0
        self.game_complete = False
        self.particles = []

    def on_enter(self):
        level = self.game.current_level
        self.strawberries_in_level = self.game.level_strawberries.get(level, 0)
        self.total_in_level = LEVELS[level - 1]['strawberries']
        self.game_complete = len(self.game.completed_levels) >= len(LEVELS)
        self.is_bonus = bool(LEVELS[level - 1].get('bonus'))
        self.particles = []
        for _ in range(20):
            angle = random_angle()
            speed = 100 + hash(str(_ * 7)) % 150
            self.particles.append({
                'pos': pygame.math.Vector2(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50),
                'vel': pygame.math.Vector2(math.cos(angle), math.sin(angle)) * speed,
                'time': 0,
                'max_time': 1.5 + (hash(str(_)) % 100) / 100,
                'color': [COLORS['strawberry'], COLORS['gold'], COLORS['hot_pink'],
                          COLORS['flower_pink'], COLORS['flower_yellow']][_ % 5],
            })

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_ESCAPE):
                self.game.change_state('level_select')

    def update(self, dt):
        self.anim_timer += dt
        for p in self.particles:
            p['time'] += dt
            p['pos'] += p['vel'] * dt
            p['vel'].y += 200 * dt

    def draw(self, surface):
        if self.is_bonus:
            self._draw_thanks(surface)
            return
        self.bg.draw(surface, 1 / 60)

        for p in self.particles:
            if p['time'] < p['max_time']:
                t = p['time'] / p['max_time']
                size = max(2, int(6 * (1 - t)))
                surface.blit(get_glow(p['color'], size),
                             (int(p['pos'].x) - size, int(p['pos'].y) - size))

        if not self.game_complete:
            title = self.font_large.render(f"Nivel {self.game.current_level} Completado!",
                True, COLORS['deep_pink'])
        else:
            title = self.font_large.render("\u00a1Juego Completado! \u2728",
                True, COLORS['gold'])
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 120))
        surface.blit(title, title_rect)

        panel = pygame.Surface((420, 250), pygame.SRCALPHA)
        panel.fill(COLORS['ui_bg'])
        panel_rect = panel.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10))
        surface.blit(panel, panel_rect)
        pygame.draw.rect(surface, COLORS['hot_pink'], panel_rect, 3, border_radius=15)

        level_name = LEVELS[self.game.current_level - 1]['name']
        name_text = self.font_medium.render(level_name, True, COLORS['text'])
        name_rect = name_text.get_rect(center=(SCREEN_WIDTH // 2, panel_rect.top + 35))
        surface.blit(name_text, name_rect)

        straw_text = self.font_medium.render(
            f"Fresas recogidas: {self.strawberries_in_level} / {self.total_in_level}",
            True, COLORS['text'])
        straw_rect = straw_text.get_rect(center=(SCREEN_WIDTH // 2, panel_rect.top + 75))
        surface.blit(straw_text, straw_rect)

        missing = self.total_in_level - self.strawberries_in_level
        if missing > 0:
            miss_text = self.font_small.render(
                f"Te faltaron {missing} fresa{'s' if missing != 1 else ''} :(",
                True, COLORS['deep_pink'])
        else:
            miss_text = self.font_small.render(
                "\u00a1Recogiste todas las fresas! \u2728", True, COLORS['gold'])
        miss_rect = miss_text.get_rect(center=(SCREEN_WIDTH // 2, panel_rect.top + 105))
        surface.blit(miss_text, miss_rect)

        total_all = sum(self.game.level_strawberries.get(lv, 0) for lv in range(1, len(LEVELS) + 1))
        total_avail = sum(lv['strawberries'] for lv in LEVELS)
        total_text = self.font_small.render(
            f"Total global: {total_all} / {total_avail} fresas", True, COLORS['text_light'])
        total_rect = total_text.get_rect(center=(SCREEN_WIDTH // 2, panel_rect.top + 140))
        surface.blit(total_text, total_rect)

        if self.game_complete:
            congrats = self.font_large.render(
                f"\u00a1Felicidades {self.game.player_name}!", True, COLORS['gold'])
            congrats_rect = congrats.get_rect(center=(SCREEN_WIDTH // 2, panel_rect.top + 190))
            surface.blit(congrats, congrats_rect)

        hint = self.font_small.render("Presiona Enter o Espacio para continuar", True, COLORS['deep_pink'])
        hint_rect = hint.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 35))
        surface.blit(hint, hint_rect)

        self._draw_floating_strawberries(surface)

    def _draw_floating_strawberries(self, surface):
        t = self.anim_timer
        surf = get_sprite('strawberry')
        for i in range(5):
            x = 100 + i * 150 + int(20 * math.sin(t * 2 + i))
            y = 50 + int(15 * math.sin(t * 3 + i * 1.5))
            surface.blit(surf, (x, y))

    def _draw_thanks(self, surface):
        self.bg.draw(surface, 1 / 60)

        for p in self.particles:
            if p['time'] < p['max_time']:
                t = p['time'] / p['max_time']
                size = max(2, int(6 * (1 - t)))
                surface.blit(get_glow(p['color'], size),
                             (int(p['pos'].x) - size, int(p['pos'].y) - size))

        t = self.anim_timer
        surf = get_sprite('strawberry')
        for i in range(7):
            x = 60 + i * ((SCREEN_WIDTH - 120) // 6) + int(18 * math.sin(t * 2 + i * 1.3))
            y = 80 + int(16 * math.sin(t * 3 + i * 1.8))
            surface.blit(surf, (x, y))

        name = self.game.player_name if self.game.player_name else "Jugador"
        title = self.font_large.render(f"\u00a1Gracias por jugar, {name}! \u2661",
                                       True, COLORS['gold'])
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 120))
        surface.blit(title, title_rect)

        panel = pygame.Surface((560, 320), pygame.SRCALPHA)
        panel.fill((255, 250, 240, 235))
        panel_rect = panel.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        surface.blit(panel, panel_rect)
        pygame.draw.rect(surface, COLORS['hot_pink'], panel_rect, 4, border_radius=18)

        lines = [
            ("Completaste el Jard\u00edn Secreto \u2605", COLORS['deep_pink']),
            ("Has dedicado todo tu tiempo a este peque\u00f1o jard\u00edn:", COLORS['text']),
            ("recorriste cada nivel, venciste a las fresitas malvadas", COLORS['text']),
            ("y recogiste cada fresa que encontraste en el camino.", COLORS['text']),
            (f"\u00a1Eres incre\u00edble, {name}! \u2661", COLORS['hot_pink']),
        ]
        y = panel_rect.top + 50
        for text, color in lines:
            rendered = self.font_small.render(text, True, color)
            rect = rendered.get_rect(center=(SCREEN_WIDTH // 2, y))
            surface.blit(rendered, rect)
            y += 38

        from levels import regular_levels
        reg = regular_levels()
        collected = sum(self.game.level_strawberries.get(lv['id'], 0) for lv in reg)
        available = sum(lv['strawberries'] for lv in reg)
        total_text = self.font_medium.render(
            f"Fresas del juego: {collected}/{available}", True, COLORS['gold'])
        total_rect = total_text.get_rect(center=(SCREEN_WIDTH // 2, panel_rect.bottom - 45))
        surface.blit(total_text, total_rect)

        hint = self.font_small.render("Presiona Enter o Espacio para continuar", True, COLORS['deep_pink'])
        hint_rect = hint.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
        surface.blit(hint, hint_rect)

        glow = get_glow(COLORS['heart'], 6)
        for i in range(5):
            hx = panel_rect.left + 26 + i * ((panel_rect.width - 52) // 4)
            hy = panel_rect.top + int(10 * math.sin(t * 4 + i))
            surface.blit(glow, (hx, hy))


def random_angle():
    import random
    return random.uniform(0, math.pi * 2)
