import pygame
import math
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, COLORS, QUALITY_ORDER, GRAPHICS_EFFECTS
from levels import LEVELS, regular_levels
from background import MenuBackground


class LevelSelectScene:
    def __init__(self, game):
        self.game = game
        self.bg = MenuBackground(game)
        self.font_title = pygame.font.Font(None, 42)
        self.font_level = pygame.font.Font(None, 28)
        self.font_small = pygame.font.Font(None, 18)
        self.font_stats = pygame.font.Font(None, 20)
        self.scroll_y = 0
        self.anim_timer = 0
        self.menu_open = False
        self.show_tips = False
        self.gfx_open = False

    def _hamburger_rect(self):
        return pygame.Rect(SCREEN_WIDTH - 54, 12, 40, 34)

    def _menu_panel_rect(self):
        return pygame.Rect(SCREEN_WIDTH - 210, 54, 180, 150)

    def _graphics_rect(self):
        panel = self._menu_panel_rect()
        return pygame.Rect(panel.left + 10, panel.top + 12, panel.width - 20, 36)

    def _tips_rect(self):
        panel = self._menu_panel_rect()
        return pygame.Rect(panel.left + 10, panel.top + 56, panel.width - 20, 36)

    def _exit_rect(self):
        panel = self._menu_panel_rect()
        return pygame.Rect(panel.left + 10, panel.top + 100, panel.width - 20, 36)

    def _regular_totals(self):
        collected = 0
        available = 0
        for lvl in regular_levels():
            collected += self.game.level_strawberries.get(lvl['id'], 0)
            available += lvl['strawberries']
        return collected, available

    def _is_unlocked(self, level):
        if level.get('bonus'):
            collected, available = self._regular_totals()
            return collected >= available
        return level['id'] == 1 or level['id'] - 1 in self.game.completed_levels

    def _bonus_level(self):
        for lvl in LEVELS:
            if lvl.get('bonus'):
                return lvl
        return None

    def _graphics_layout(self):
        pw, ph = 560, 380
        panel = pygame.Rect((SCREEN_WIDTH - pw) // 2, (SCREEN_HEIGHT - ph) // 2, pw, ph)
        quality_btns = []
        bw = 150
        for i in range(len(QUALITY_ORDER)):
            quality_btns.append(pygame.Rect(panel.left + 30 + i * (bw + 16), panel.top + 100, bw, 44))
        toggles = []
        toggle_w = (pw - 60 - 12) // 2
        for i, (key, _label) in enumerate(GRAPHICS_EFFECTS):
            col = i % 2
            row = i // 2
            toggles.append((key, pygame.Rect(panel.left + 30 + col * (toggle_w + 12),
                                             panel.top + 200 + row * 44, toggle_w, 36)))
        close = pygame.Rect(panel.left + pw // 2 - 80, panel.bottom - 60, 160, 40)
        return {
            'panel': panel,
            'res_label': (panel.left + 30, panel.top + 68),
            'quality_btns': quality_btns,
            'eff_label': (panel.left + 30, panel.top + 168),
            'toggles': toggles,
            'close': close,
        }

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self.gfx_open:
                    self.gfx_open = False
                    return True
                if self.show_tips:
                    self.show_tips = False
                    return True
                if self.menu_open:
                    self.menu_open = False
                    return True
                return False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                self.scroll_y = min(self.scroll_y + 30, 0)
            elif event.button == 5:
                max_scroll = -max(0, len(LEVELS) * 110 + 50 - (SCREEN_HEIGHT - 150))
                self.scroll_y = max(self.scroll_y - 30, max_scroll)
            elif event.button == 1:
                mx, my = pygame.mouse.get_pos()
                mx = mx // self.game.scale
                my = my // self.game.scale
                if self.gfx_open:
                    layout = self._graphics_layout()
                    if layout['close'].collidepoint(mx, my):
                        self.gfx_open = False
                    elif not layout['panel'].collidepoint(mx, my):
                        self.gfx_open = False
                    else:
                        for i, q in enumerate(QUALITY_ORDER):
                            if layout['quality_btns'][i].collidepoint(mx, my):
                                if q != self.game.gfx_quality:
                                    self.game.gfx_quality = q
                                    self.game.apply_graphics()
                                return
                        for key, rect in layout['toggles']:
                            if rect.collidepoint(mx, my):
                                setattr(self.game, key, not getattr(self.game, key))
                                return
                    return
                if self.show_tips:
                    self.show_tips = False
                    return
                if self.menu_open:
                    if self._exit_rect().collidepoint(mx, my):
                        self.game.running = False
                    elif self._tips_rect().collidepoint(mx, my):
                        self.menu_open = False
                        self.show_tips = True
                    elif self._graphics_rect().collidepoint(mx, my):
                        self.menu_open = False
                        self.gfx_open = True
                    elif not self._menu_panel_rect().collidepoint(mx, my):
                        self.menu_open = False
                    return
                if self._hamburger_rect().collidepoint(mx, my):
                    self.menu_open = True
                    return
                for i, level in enumerate(LEVELS):
                    bx = SCREEN_WIDTH // 2 - 150
                    by = 150 + i * 110 + self.scroll_y
                    btn_rect = pygame.Rect(bx, by, 300, 90)
                    if btn_rect.collidepoint(mx, my):
                        if self._is_unlocked(level):
                            self.game.current_level = level['id']
                            self.game.change_state('bonus_intro' if level.get('bonus') else 'game')
                        break

    def update(self, dt):
        self.anim_timer += dt

    def draw(self, surface):
        self.bg.draw(surface, 1 / 60)

        name_display = self.game.player_name if self.game.player_name else "Jugador"
        title = self.font_title.render(f"\u00a1Hola {name_display}! Selecciona un nivel", True, COLORS['deep_pink'])
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 60))
        surface.blit(title, title_rect)

        total_strawberries, total_available = self._regular_totals()
        if total_available > 0:
            stats_text = self.font_stats.render(
                f"Fresas: {total_strawberries}/{total_available}  |  Niveles completados: {len(self.game.completed_levels)}/{len(regular_levels())}",
                True, COLORS['text'])
            stats_rect = stats_text.get_rect(center=(SCREEN_WIDTH // 2, 95))
            surface.blit(stats_text, stats_rect)

        clip_rect = pygame.Rect(0, 120, SCREEN_WIDTH, SCREEN_HEIGHT - 120)
        old_clip = surface.get_clip()
        surface.set_clip(clip_rect)

        for i, level in enumerate(LEVELS):
            bx = SCREEN_WIDTH // 2 - 180
            by = 140 + i * 110 + self.scroll_y
            if by + 90 < 120 or by > SCREEN_HEIGHT:
                continue

            is_bonus = level.get('bonus')
            unlocked = self._is_unlocked(level)
            completed = level['id'] in self.game.completed_levels

            btn_color = COLORS['white'] if unlocked else COLORS['ui_bg']
            if is_bonus:
                border_color = COLORS['gold'] if unlocked else COLORS['lock']
            else:
                border_color = COLORS['gold'] if completed else (COLORS['hot_pink'] if unlocked else COLORS['lock'])
            btn_rect = pygame.Rect(bx, by, 360, 90)
            pygame.draw.rect(surface, btn_color, btn_rect, border_radius=15)
            pygame.draw.rect(surface, border_color, btn_rect, 3, border_radius=15)

            if completed and not is_bonus:
                check = self.font_level.render("\u2713", True, COLORS['gold'])
                surface.blit(check, (bx + 325, by + 10))
            if is_bonus and unlocked:
                star = self.font_level.render("\u2605", True, COLORS['gold'])
                surface.blit(star, (bx + 322, by + 12))

            if is_bonus:
                level_num = self.font_level.render("\u2605 Nivel Bonus \u2605", True,
                    COLORS['gold'] if unlocked else COLORS['lock'])
            else:
                level_num = self.font_level.render(f"Nivel {level['id']}", True,
                    COLORS['text'] if unlocked else COLORS['lock'])
            surface.blit(level_num, (bx + 15, by + 10))

            level_name = self.font_small.render(level['name'], True, COLORS['text_light'] if unlocked else COLORS['lock'])
            surface.blit(level_name, (bx + 15, by + 38))

            if is_bonus:
                straw_count = self.game.level_strawberries.get(level['id'], 0)
                straw_str = f"Fresas: {straw_count}/{level['strawberries']}"
                straw_text = self.font_small.render(straw_str, True,
                    COLORS['text_light'] if unlocked else COLORS['lock'])
                surface.blit(straw_text, (bx + 15, by + 56))
                if not unlocked:
                    collected, available = self._regular_totals()
                    missing = available - collected
                    prog_w = 150
                    fill = int(prog_w * collected / available) if available else 0
                    pygame.draw.rect(surface, COLORS['light_pink'],
                                     (bx + 180, by + 58, prog_w, 9), border_radius=4)
                    pygame.draw.rect(surface, COLORS['deep_pink'],
                                     (bx + 180, by + 58, fill, 9), border_radius=4)
                    miss_text = self.font_small.render(
                        f"Te faltan {missing} fresa{'s' if missing != 1 else ''}",
                        True, COLORS['hot_pink'])
                    surface.blit(miss_text, (bx + 180, by + 70))
                else:
                    hint = self.font_small.render("\u00a1Desbloqueado!", True, COLORS['deep_pink'])
                    surface.blit(hint, (bx + 180, by + 58))
            else:
                straw_count = self.game.level_strawberries.get(level['id'], 0)
                straw_str = f"Fresas: {straw_count}/{level['strawberries']}"
                straw_text = self.font_small.render(straw_str, True, COLORS['text_light'] if unlocked else COLORS['lock'])
                surface.blit(straw_text, (bx + 15, by + 60))

            if not unlocked:
                lock_surf = pygame.Surface((24, 24), pygame.SRCALPHA)
                pygame.draw.rect(lock_surf, COLORS['lock'], (4, 10, 16, 12), border_radius=3)
                pygame.draw.arc(lock_surf, COLORS['lock'], (6, 4, 12, 10), math.pi, 2 * math.pi, 3)
                surface.blit(lock_surf, (bx + 310, by + 30))

            if i < len(LEVELS) - 1:
                next_unlocked = (i + 2) == 1 or (i + 1) in self.game.completed_levels
                connector_color = COLORS['hot_pink'] if next_unlocked else COLORS['lock']
                pygame.draw.line(surface, connector_color,
                    (bx + 180, by + 90), (bx + 180, by + 110), 2)

        surface.set_clip(old_clip)

        if self.scroll_y < 0:
            pygame.draw.line(surface, COLORS['pink'], (0, 119), (SCREEN_WIDTH, 119), 2)
        total_h = len(LEVELS) * 110 + 50
        visible_h = SCREEN_HEIGHT - 120
        if total_h > visible_h:
            bar_h = int(visible_h * visible_h / total_h)
            bar_y = 120 + int(-self.scroll_y / (total_h - visible_h) * (visible_h - bar_h))
            pygame.draw.rect(surface, COLORS['hot_pink'], (SCREEN_WIDTH - 8, bar_y, 6, bar_h), border_radius=3)

        self._draw_hamburger(surface)
        if self.menu_open:
            self._draw_menu(surface)
        if self.gfx_open:
            self._draw_graphics(surface)
        if self.show_tips:
            self._draw_tips(surface)

    def _draw_hamburger(self, surface):
        r = self._hamburger_rect()
        s = pygame.Surface((r.width, r.height), pygame.SRCALPHA)
        s.fill((255, 209, 220, 215))
        pygame.draw.rect(s, COLORS['hot_pink'], s.get_rect(), 2, border_radius=8)
        for i in range(3):
            y = 8 + i * 9
            pygame.draw.line(s, COLORS['text'], (10, y), (r.width - 10, y), 3)
        surface.blit(s, r.topleft)

    def _draw_menu(self, surface):
        panel = self._menu_panel_rect()
        panel_surf = pygame.Surface((panel.width, panel.height), pygame.SRCALPHA)
        panel_surf.fill((255, 220, 230, 245))
        surface.blit(panel_surf, panel.topleft)
        pygame.draw.rect(surface, COLORS['hot_pink'], panel, 2, border_radius=12)

        graphics_btn = self._graphics_rect()
        pygame.draw.rect(surface, COLORS['white'], graphics_btn, border_radius=10)
        pygame.draw.rect(surface, COLORS['deep_pink'], graphics_btn, 2, border_radius=10)
        t = self.font_small.render("Gr\u00e1ficos", True, COLORS['text'])
        surface.blit(t, t.get_rect(center=graphics_btn.center))

        tips_btn = self._tips_rect()
        pygame.draw.rect(surface, COLORS['white'], tips_btn, border_radius=10)
        pygame.draw.rect(surface, COLORS['deep_pink'], tips_btn, 2, border_radius=10)
        t = self.font_small.render("Consejos", True, COLORS['text'])
        surface.blit(t, t.get_rect(center=tips_btn.center))

        exit_btn = self._exit_rect()
        pygame.draw.rect(surface, COLORS['white'], exit_btn, border_radius=10)
        pygame.draw.rect(surface, COLORS['deep_pink'], exit_btn, 2, border_radius=10)
        t = self.font_small.render("Salir del juego", True, COLORS['text'])
        surface.blit(t, t.get_rect(center=exit_btn.center))

    def _draw_graphics(self, surface):
        layout = self._graphics_layout()
        panel = layout['panel']

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((40, 20, 30, 150))
        surface.blit(overlay, (0, 0))
        panel_surf = pygame.Surface((panel.width, panel.height), pygame.SRCALPHA)
        panel_surf.fill((255, 245, 250, 245))
        surface.blit(panel_surf, panel.topleft)
        pygame.draw.rect(surface, COLORS['hot_pink'], panel, 4, border_radius=18)

        title = self.font_title.render("\u2699 Gr\u00e1ficos", True, COLORS['deep_pink'])
        surface.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, panel.top + 40)))

        res_text = self.font_small.render("Resoluci\u00f3n de renderizado", True, COLORS['text_light'])
        surface.blit(res_text, layout['res_label'])
        for i, q in enumerate(QUALITY_ORDER):
            btn = layout['quality_btns'][i]
            selected = (q == self.game.gfx_quality)
            pygame.draw.rect(surface, COLORS['deep_pink'] if selected else COLORS['white'],
                             btn, border_radius=10)
            pygame.draw.rect(surface, COLORS['deep_pink'], btn, 2, border_radius=10)
            label = self.font_small.render(q, True,
                                           COLORS['white'] if selected else COLORS['text'])
            surface.blit(label, label.get_rect(center=btn.center))

        eff_text = self.font_small.render("Efectos visuales", True, COLORS['text_light'])
        surface.blit(eff_text, layout['eff_label'])
        for key, rect in layout['toggles']:
            on = getattr(self.game, key)
            pygame.draw.rect(surface, COLORS['deep_pink'] if on else COLORS['white'],
                             rect, border_radius=10)
            pygame.draw.rect(surface, COLORS['deep_pink'], rect, 2, border_radius=10)
            label_text = f"{'\u2713' if on else '\u2717'} {dict(GRAPHICS_EFFECTS)[key]}"
            t = self.font_small.render(label_text, True,
                                       COLORS['white'] if on else COLORS['text'])
            surface.blit(t, t.get_rect(center=rect.center))

        close_btn = layout['close']
        pygame.draw.rect(surface, COLORS['deep_pink'], close_btn, border_radius=12)
        t = self.font_small.render("Cerrar", True, COLORS['white'])
        surface.blit(t, t.get_rect(center=close_btn.center))

    def _draw_tips(self, surface):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((40, 20, 30, 150))
        surface.blit(overlay, (0, 0))

        panel_w, panel_h = 660, 400
        panel = pygame.Rect((SCREEN_WIDTH - panel_w) // 2, (SCREEN_HEIGHT - panel_h) // 2, panel_w, panel_h)
        panel_surf = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
        panel_surf.fill((255, 245, 250, 245))
        surface.blit(panel_surf, panel.topleft)
        pygame.draw.rect(surface, COLORS['hot_pink'], panel, 4, border_radius=18)

        title = self.font_title.render("\u2726 Consejos para jugar \u2726", True, COLORS['deep_pink'])
        surface.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, panel.top + 45)))

        tips = [
            "No hay puntos de control: si mueres, vuelves al inicio del mapa.",
            "No hay guardado: al cerrar el juego se pierde el progreso.",
            "No es necesario completar el juego al 100% para disfrutarlo.",
            "Recoge todas las fresas de los 10 niveles para desbloquear el bonus.",
            "Juega en un espacio c\u00f3modo y a tu propio ritmo.",
            "T\u00f3mate pausas y descansa si lo necesitas.",
        ]
        y = panel.top + 95
        for tip in tips:
            text = self.font_small.render("\u2022 " + tip, True, COLORS['text'])
            surface.blit(text, (panel.left + 40, y))
            y += 40

        hint = self.font_small.render("Haz clic o presiona ESC para cerrar", True, COLORS['deep_pink'])
        surface.blit(hint, hint.get_rect(center=(SCREEN_WIDTH // 2, panel.bottom - 30)))
