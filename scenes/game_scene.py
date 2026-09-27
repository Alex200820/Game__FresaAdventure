import pygame
import math
import random
from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE, COLORS, PLAYER_MAX_HP,
    SPIKE_DAMAGE, STOMP_BOUNCE, LEVEL_THEMES,
)
from levels import LEVELS, SPIKE
from camera import Camera
from entities.player import Player
from entities.enemy import Enemy
from sprites import get_sprite, get_dynamic_sprite, get_glow, get_cloud
from background import get_sky, get_sun, make_hill_layer, make_ground_layer, blit_tiled, make_sparkles, draw_sparkles
from music import music_gen, play_sfx


class GameScene:
    def __init__(self, game):
        self.game = game
        self.level_data = None
        self.grid = None
        self.player = None
        self.camera = None
        self.strawberries_collected = 0
        self.total_strawberries = 0
        self.collected_strawberries = set()
        self.strawberry_rects = {}
        self.enemies = []
        self.theme = {}
        self.level_complete = False
        self.complete_timer = 0
        self.fade_alpha = 0
        self.fading = False
        self.time = 0.0
        self.particles = []
        self.motes = []
        self.clouds = []
        self.parallax = {}
        self.menu_open = False
        self.menu_timer = 0.0
        self.game_over = False
        self.game_over_timer = 0.0
        self.death_delay = 1.0
        self.track_dropdown_open = False
        self.track_keys = music_gen.get_tracks()
        self.font_large = pygame.font.Font(None, 52)
        self.font_medium = pygame.font.Font(None, 30)
        self.font_small = pygame.font.Font(None, 20)
        self._heart_full = self._make_heart(COLORS['heart'])
        self._heart_empty = self._make_heart(COLORS['heart_empty'])

    def _make_heart(self, color):
        s = pygame.Surface((22, 20), pygame.SRCALPHA)
        pygame.draw.polygon(s, color, [(11, 18), (3, 9), (3, 5), (7, 2), (11, 6), (15, 2), (19, 5), (19, 9)])
        pygame.draw.polygon(s, (255, 255, 255, 120), [(11, 18), (3, 9), (3, 5), (5, 3), (8, 8)])
        return s

    def load_level(self, level_id):
        self.level_data = LEVELS[level_id - 1]
        self.grid = [row[:] for row in self.level_data['grid']]
        self.total_strawberries = self.level_data['strawberries']
        self.strawberries_collected = 0
        self.collected_strawberries.clear()
        self.strawberry_rects.clear()
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                if self.grid[y][x] == 5:
                    r = pygame.Rect(x * TILE_SIZE + 4, y * TILE_SIZE + 4, TILE_SIZE - 8, TILE_SIZE - 8)
                    self.strawberry_rects[(x, y)] = r

        self.enemies = []
        for ex, ey in self.level_data['enemies']:
            px = ex * TILE_SIZE + (TILE_SIZE - 20) // 2
            py = ey * TILE_SIZE
            self.enemies.append(Enemy(px, py))

        start = self.level_data['player_start']
        px = start[0] * TILE_SIZE + (TILE_SIZE - 20) // 2
        py = start[1] * TILE_SIZE - 28
        self.player = Player(px, py, self.game.player_name)
        self.player.hp = PLAYER_MAX_HP
        self.player.max_hp = PLAYER_MAX_HP
        self.camera = Camera(self.level_data['width'], self.level_data['height'], TILE_SIZE)
        self.level_complete = False
        self.complete_timer = 0
        self.fade_alpha = 0
        self.fading = False
        self.menu_open = False
        self.track_dropdown_open = False
        self.menu_timer = 0.0
        self.game_over = False
        self.game_over_timer = 0.0
        self.time = 0.0
        self.particles.clear()
        self.motes.clear()
        self.theme = LEVEL_THEMES.get(self.level_data['id'], {})
        self.parallax['far'] = make_hill_layer(
            220, self.theme.get('hill_far', COLORS['hill_far']),
            self.theme.get('hill_far_dark', COLORS['hill_far_dark']), 12, seed=21)
        self.parallax['mid'] = make_hill_layer(
            190, self.theme.get('hill_mid', COLORS['hill_mid']),
            self.theme.get('hill_mid_dark', COLORS['hill_mid_dark']), 11, seed=31)
        self.parallax['near'] = make_ground_layer(150, seed=5)
        self._build_clouds()
        self._build_motes()
        self.sparkles = make_sparkles(16, seed=6)
        self.camera.follow(self.player.rect)

    def _build_clouds(self):
        rng = random.Random(7)
        self.clouds = []
        for _ in range(9):
            scale = rng.choice([0.5, 0.6, 0.7, 0.8, 1.0, 1.1, 1.2])
            self.clouds.append({
                'surf': get_cloud(scale),
                'x': rng.uniform(0, SCREEN_WIDTH),
                'y': rng.uniform(24, 200),
                'speed': rng.uniform(5, 16),
            })

    def _build_motes(self):
        rng = random.Random(12)
        self.motes = []
        for _ in range(22):
            self.motes.append({
                'x': rng.uniform(0, SCREEN_WIDTH),
                'y': rng.uniform(0, SCREEN_HEIGHT),
                'spd': rng.uniform(8, 26),
                'phase': rng.uniform(0, math.pi * 2),
                'color': rng.choice([COLORS['deco_white'], COLORS['deco_yellow'], COLORS['deco_pink']]),
            })

    def _spawn_particles(self, pos, vel, color, count, life=0.6, size=3, gravity=0, drag=2.0):
        if not self.game.gfx_particles:
            return
        if len(self.particles) > 320:
            return
        for _ in range(count):
            self.particles.append({
                'pos': pygame.math.Vector2(pos),
                'vel': vel + pygame.math.Vector2(random.uniform(-45, 45), random.uniform(-70, 0)),
                'life': 0.0,
                'max': random.uniform(life * 0.6, life * 1.3),
                'color': color,
                'size': random.uniform(size * 0.6, size * 1.4),
                'gravity': gravity,
                'drag': drag,
            })

    def _spawn_dust(self, pos):
        self._spawn_particles(pos, pygame.math.Vector2(random.uniform(-20, 20), 0),
                              (255, 240, 235), 4, life=0.4, size=2, gravity=-40, drag=3.0)

    # --- Pause menu ------------------------------------------------------

    def _hamburger_rect(self):
        return pygame.Rect(SCREEN_WIDTH - 54, 52, 40, 34)

    def _open_menu(self):
        self.menu_open = True
        self.track_dropdown_open = False
        self.menu_timer = 0.0

    def _close_menu(self):
        self.menu_open = False
        self.track_dropdown_open = False

    def _menu_layout(self):
        n = len(self.track_keys)
        extra = n * 32 + 8 if self.track_dropdown_open else 0
        pw = 440
        ph = 360 + extra
        panel = pygame.Rect(SCREEN_WIDTH // 2 - pw // 2, (SCREEN_HEIGHT - ph) // 2, pw, ph)
        resume = pygame.Rect(panel.left + 24, panel.top + 52, pw - 48, 42)
        vol_label = (panel.left + 24, resume.bottom + 20)
        vol_slider = pygame.Rect(panel.left + 24, vol_label[1] + 24, pw - 48, 16)
        song_label = (panel.left + 24, vol_slider.bottom + 20)
        combo = pygame.Rect(panel.left + 24, song_label[1] + 26, pw - 48, 34)
        items = []
        if self.track_dropdown_open:
            for i in range(n):
                items.append(pygame.Rect(panel.left + 24, combo.bottom + 4 + i * 32, pw - 48, 30))
        bottom_anchor = combo.bottom + extra
        bright_label = (panel.left + 24, bottom_anchor + 20)
        bright_slider = pygame.Rect(panel.left + 24, bright_label[1] + 24, pw - 48, 16)
        exit_btn = pygame.Rect(panel.left + 24, bright_slider.bottom + 22, pw - 48, 40)
        return {
            'panel': panel,
            'resume': resume,
            'vol_label': vol_label,
            'vol_slider': vol_slider,
            'song_label': song_label,
            'combo': combo,
            'items': items,
            'bright_label': bright_label,
            'bright_slider': bright_slider,
            'exit': exit_btn,
        }

    def _slider_value(self, rect, mx, minv, maxv):
        t = max(0.0, min(1.0, (mx - rect.left) / rect.width))
        return minv + t * (maxv - minv)

    def _handle_click(self, mx, my):
        if self.game_over:
            if self.game_over_timer < self.death_delay:
                return
            layout = self._game_over_layout()
            if layout['retry'].collidepoint(mx, my):
                self.load_level(self.level_data['id'])
            elif layout['exit'].collidepoint(mx, my):
                self.game.change_state('level_select')
            return
        if self.menu_open:
            layout = self._menu_layout()
            if layout['resume'].collidepoint(mx, my):
                self._close_menu()
            elif layout['combo'].collidepoint(mx, my):
                self.track_dropdown_open = not self.track_dropdown_open
            elif any(r.collidepoint(mx, my) for r in layout['items']):
                for i, r in enumerate(layout['items']):
                    if r.collidepoint(mx, my):
                        key = self.track_keys[i]
                        self.game.music_track = key
                        music_gen.select_track(key)
                        self.track_dropdown_open = False
                        break
            elif layout['vol_slider'].collidepoint(mx, my):
                v = self._slider_value(layout['vol_slider'], mx, 0.0, 1.0)
                v = round(v * 20) / 20
                self.game.music_volume = v
                music_gen.set_volume(v)
            elif layout['bright_slider'].collidepoint(mx, my):
                v = self._slider_value(layout['bright_slider'], mx, 0.5, 1.5)
                v = round(v * 20) / 20
                self.game.brightness = max(0.5, min(1.5, v))
            elif layout['exit'].collidepoint(mx, my):
                self._close_menu()
                self.game.change_state('level_select')
            elif layout['panel'].collidepoint(mx, my):
                pass
            else:
                self._close_menu()
        else:
            if self._hamburger_rect().collidepoint(mx, my):
                self._open_menu()

    def handle_event(self, event):
        if self.level_complete or self.fading:
            return
        if self.game_over:
            if self.game_over_timer < self.death_delay:
                return
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    self.load_level(self.level_data['id'])
                elif event.key == pygame.K_ESCAPE:
                    self.game.change_state('level_select')
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = getattr(event, 'pos', pygame.mouse.get_pos())
                self._handle_click(mx // self.game.scale, my // self.game.scale)
            return
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self.menu_open:
                    self._close_menu()
                else:
                    self._open_menu()
                return
            if self.menu_open:
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    self._close_menu()
                return
            if event.key in (pygame.K_UP, pygame.K_SPACE, pygame.K_w):
                self.player.jump()
        if event.type == pygame.KEYUP:
            if self.menu_open:
                return
            if event.key in (pygame.K_UP, pygame.K_SPACE, pygame.K_w):
                self.player.cut_jump()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = getattr(event, 'pos', pygame.mouse.get_pos())
            self._handle_click(mx // self.game.scale, my // self.game.scale)

    def _complete_level(self):
        self.level_complete = True
        self.complete_timer = 0
        self.game.completed_levels.add(self.level_data['id'])
        collected = self.game.level_strawberries.get(self.level_data['id'], 0)
        if self.strawberries_collected > collected:
            self.game.level_strawberries[self.level_data['id']] = self.strawberries_collected

    def _respawn(self):
        start = self.level_data['player_start']
        self.player.invincible_timer = 1.5
        px = start[0] * TILE_SIZE + (TILE_SIZE - 20) // 2
        py = start[1] * TILE_SIZE - 28
        self.player.set_position(px, py)
        self.camera.follow(self.player.rect, dt=0.02)
        self.camera.shake(5, 0.3)

    def _spawn_death_particles(self):
        pos = self.player.rect.center
        self._spawn_particles(pos, pygame.math.Vector2(0, 0),
                              COLORS['deep_pink'], 16, life=0.8, size=3, gravity=-80, drag=2.0)
        self._spawn_particles(pos, pygame.math.Vector2(0, 0),
                              COLORS['gold'], 10, life=0.6, size=2, gravity=-40, drag=3.0)

    def _trigger_game_over(self):
        if self.game_over:
            return
        self.game_over = True
        self.game_over_timer = 0.0
        self.player.hp = 0
        self._spawn_death_particles()

    def _check_spike_damage(self):
        if self.player.invincible_timer > 0:
            return
        grid = self.grid
        ts = TILE_SIZE
        col = self.player.rect.centerx // ts
        row = (self.player.rect.bottom - 1) // ts
        if 0 <= row < len(grid) and 0 <= col < len(grid[0]):
            if grid[row][col] == SPIKE:
                direction = 1 if self.player.facing_right else -1
                self.player.take_damage(SPIKE_DAMAGE, direction)
                self.camera.shake(6, 0.3)
                self._spawn_particles(self.player.rect.midbottom,
                                      pygame.math.Vector2(direction * 60, -80),
                                      COLORS['deep_pink'], 12, life=0.5, size=3, gravity=500)

    def update(self, dt):
        self.time += dt

        if self.game_over:
            self.game_over_timer += dt
            if self.game_over_timer < self.death_delay:
                self.player.moving_left = False
                self.player.moving_right = False
                self.player.update(dt, self.grid)
            self._update_particles(dt)
            return

        if self.menu_open:
            self.menu_timer = min(1.0, self.menu_timer + dt * 8)
            return

        if self.level_complete:
            self.complete_timer += dt
            if self.complete_timer > 2.0:
                self.fading = True
            if self.fading:
                self.fade_alpha = min(255, self.fade_alpha + dt * 300)
                if self.fade_alpha >= 255:
                    self.game.change_state('victory')
            return

        for c in self.clouds:
            c['x'] += c['speed'] * dt
            if c['x'] - c['surf'].get_width() > SCREEN_WIDTH:
                c['x'] = -c['surf'].get_width()
        for m in self.motes:
            m['y'] -= m['spd'] * dt
            if m['y'] < -5:
                m['y'] = SCREEN_HEIGHT + 5
                m['x'] = random.uniform(0, SCREEN_WIDTH)

        keys = pygame.key.get_pressed()
        self.player.moving_left = keys[pygame.K_LEFT] or keys[pygame.K_a]
        self.player.moving_right = keys[pygame.K_RIGHT] or keys[pygame.K_d]

        if self.player.fell:
            self.player.take_damage(1, 1)
            if self.player.dead:
                self._trigger_game_over()
            else:
                self._respawn()
                self._update_particles(dt)
            return

        prev_ground = self.player.on_ground
        self.player.update(dt, self.grid)

        if self.player.just_landed:
            self._spawn_dust(self.player.rect.midbottom)
        if self.player.pending_dust:
            self._spawn_dust((self.player.rect.centerx, self.player.rect.bottom))

        self._check_spike_damage()
        if self.player.dead:
            self._trigger_game_over()
            return

        for e in list(self.enemies):
            e.update(dt, self.grid)
            if not self.player.rect.colliderect(e.rect):
                continue
            stomped = (self.player.vy > 0 and
                       self.player.rect.centery < e.rect.centery)
            if stomped:
                self.enemies.remove(e)
                self.player.vy = -STOMP_BOUNCE
                pos = e.rect.center
                self._spawn_particles(pos, pygame.math.Vector2(0, 0),
                                      COLORS['strawberry_top'], 8, life=0.5, size=3, gravity=-60, drag=2.5)
                self._spawn_particles(pos, pygame.math.Vector2(0, 0),
                                      COLORS['gold'], 6, life=0.4, size=2, gravity=-40, drag=3.0)
                play_sfx('stomp')
            else:
                direction = 1 if self.player.facing_right else -1
                self.player.take_damage(1, direction)
                self.camera.shake(5, 0.3)

        for (sx, sy), s_rect in list(self.strawberry_rects.items()):
            if (sx, sy) not in self.collected_strawberries:
                if self.player.rect.colliderect(s_rect):
                    self.collected_strawberries.add((sx, sy))
                    self.strawberries_collected += 1
                    self.grid[sy][sx] = 0
                    pos = (sx * TILE_SIZE + TILE_SIZE // 2, sy * TILE_SIZE + TILE_SIZE // 2)
                    self._spawn_particles(pos, pygame.math.Vector2(0, 0),
                                          COLORS['gold'], 8, life=0.7, size=3, gravity=-60, drag=2.5)
                    self._spawn_particles(pos, pygame.math.Vector2(0, 0),
                                          COLORS['strawberry'], 6, life=0.5, size=2, gravity=-40, drag=3.0)

        ex = self.level_data['exit_pos']
        if ex:
            exit_rect = pygame.Rect(ex[0] * TILE_SIZE, ex[1] * TILE_SIZE - 32, TILE_SIZE, TILE_SIZE * 2)
            if exit_rect.contains(self.player.rect) and self.player.on_ground:
                self._complete_level()

        self.camera.follow(self.player.rect, self.player.vx, dt)
        self.camera.update_shake(dt)
        self._update_particles(dt)

    def _update_particles(self, dt):
        for p in self.particles[:]:
            p['life'] += dt
            if p['life'] >= p['max']:
                self.particles.remove(p)
                continue
            p['vel'].y += p.get('gravity', 0) * dt
            drag = p.get('drag', 0)
            if drag:
                p['vel'].x *= max(0.0, 1 - drag * dt)
                p['vel'].y *= max(0.0, 1 - drag * dt)
            p['pos'] += p['vel'] * dt

    def _blit_parallax(self, surface, layer, y, factor):
        blit_tiled(surface, layer, y, self.camera.x * factor)

    def draw(self, surface):
        cam_x = int(self.camera.x) + self.camera.ox
        cam_y = int(self.camera.y) + self.camera.oy

        surface.blit(get_sky(SCREEN_WIDTH, SCREEN_HEIGHT, self.theme), (0, 0))
        surface.blit(get_sun(self.theme), (SCREEN_WIDTH - 200, 56))

        if self.game.gfx_parallax:
            self._blit_parallax(surface, self.parallax['far'], 264, 0.12)
            self._blit_parallax(surface, self.parallax['mid'], 328, 0.25)
        self._blit_parallax(surface, self.parallax['near'], 13 * TILE_SIZE, 1.0)

        if self.game.gfx_clouds:
            for c in self.clouds:
                surface.blit(c['surf'], (int(c['x']), int(c['y'])))

        if self.game.gfx_sparkles:
            draw_sparkles(surface, self.sparkles, self.time, cam_x * 0.15)

        if self.game.gfx_sparkles:
            for m in self.motes:
                off = math.sin(self.time * 2 + m['phase']) * 5
                mx = int(m['x'])
                surface.blit(get_glow(m['color'], 3), (mx, int(m['y'] + off)))

        if self.grid:
            ts = TILE_SIZE
            grid_w = len(self.grid[0])
            grid_h = len(self.grid)
            col_start = max(0, cam_x // ts - 1)
            col_end = min(grid_w, (cam_x + SCREEN_WIDTH) // ts + 2)
            row_start = max(0, cam_y // ts - 1)
            row_end = min(grid_h, (cam_y + SCREEN_HEIGHT) // ts + 2)

            for y in range(row_start, row_end):
                row = self.grid[y]
                for x in range(col_start, col_end):
                    tile = row[x]
                    if tile == 0:
                        continue
                    screen_x = x * ts - cam_x
                    screen_y = y * ts - cam_y
                    if tile == 5:
                        if (x, y) in self.collected_strawberries:
                            continue
                        bob = int(3 * math.sin(self.time * 3 + x * 0.7))
                        surface.blit(get_glow(COLORS['strawberry'], 14), (screen_x + ts // 2 - 14, screen_y + ts // 2 - 14 + bob))
                        surface.blit(get_sprite('strawberry'), (screen_x, screen_y + bob))
                    elif tile == 6:
                        surface.blit(get_glow(COLORS['exit_glow'], 20), (screen_x + ts // 2 - 20, screen_y + ts // 2 - 20))
                        surface.blit(get_dynamic_sprite('exit'), (screen_x, screen_y))
                    else:
                        name = {1: 'grass', 2: 'brick', 3: 'wall', 4: 'spike', 7: 'bush'}.get(tile)
                        if name:
                            surface.blit(get_sprite(name), (screen_x, screen_y))
                        else:
                            continue
                    if tile == 1 and y - 1 >= 0 and self.grid[y - 1][x] == 0:
                        h = (x * 73856093) ^ (y * 19349663)
                        r = h % 100
                        if r < 22:
                            deco = ['flower_pink', 'flower_yellow', 'flower_white', 'tuft'][r % 4]
                            sp = get_sprite(deco)
                            sway = int(2 * math.sin(self.time * 2 + x * 0.8))
                            surface.blit(sp, (screen_x - 2, screen_y - sp.get_height() + 10 + sway))

        self.player.draw(surface, self.camera)

        for e in self.enemies:
            e.draw(surface, self.camera)

        for p in self.particles:
            t = p['life'] / p['max']
            size = max(1, int(p['size'] * (1 - t)))
            surf = get_glow(p['color'], size)
            surface.blit(surf, (int(p['pos'].x) - size, int(p['pos'].y) - size))

        self._draw_hud(surface)
        if not self.level_complete and not self.game_over:
            self._draw_hamburger(surface)
        if self.menu_open:
            self._draw_menu(surface)
        if self.game_over and self.game_over_timer >= self.death_delay:
            self._draw_game_over(surface)

        if self.level_complete:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 100))
            surface.blit(overlay, (0, 0))
            complete_text = self.font_large.render("Nivel Completado!", True, COLORS['gold'])
            text_rect = complete_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
            surface.blit(complete_text, text_rect)
            straw_text = self.font_medium.render(
                f"Fresas: {self.strawberries_collected}/{self.total_strawberries}",
                True, COLORS['white'])
            straw_rect = straw_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10))
            surface.blit(straw_text, straw_rect)

        if self.fading:
            fade_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            fade_surf.fill(COLORS['pink'])
            fade_surf.set_alpha(self.fade_alpha)
            surface.blit(fade_surf, (0, 0))

    def _draw_hamburger(self, surface):
        r = self._hamburger_rect()
        s = pygame.Surface((r.width, r.height), pygame.SRCALPHA)
        s.fill((255, 209, 220, 215))
        pygame.draw.rect(s, COLORS['hot_pink'], s.get_rect(), 2, border_radius=8)
        for i in range(3):
            y = 8 + i * 9
            pygame.draw.line(s, COLORS['text'], (10, y), (r.width - 10, y), 3)
        surface.blit(s, r.topleft)

    def _draw_button(self, surface, rect, text, border):
        pygame.draw.rect(surface, (255, 255, 255), rect, border_radius=12)
        pygame.draw.rect(surface, border, rect, 2, border_radius=12)
        t = self.font_medium.render(text, True, COLORS['text'])
        surface.blit(t, t.get_rect(center=rect.center))

    def _game_over_layout(self):
        pw = 440
        ph = 240
        panel = pygame.Rect(SCREEN_WIDTH // 2 - pw // 2, (SCREEN_HEIGHT - ph) // 2, pw, ph)
        retry = pygame.Rect(panel.left + 24, panel.top + 96, pw - 48, 44)
        exit_btn = pygame.Rect(panel.left + 24, retry.bottom + 18, pw - 48, 44)
        return {'panel': panel, 'retry': retry, 'exit': exit_btn}

    def _draw_game_over(self, surface):
        t = max(0.0, min(1.0, (self.game_over_timer - self.death_delay) / 0.35))
        alpha = int(185 * t)
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((30, 10, 25, alpha))
        surface.blit(overlay, (0, 0))

        layout = self._game_over_layout()
        panel = layout['panel']
        panel_surf = pygame.Surface((panel.width, panel.height), pygame.SRCALPHA)
        panel_surf.fill((255, 220, 230, 245))
        surface.blit(panel_surf, panel.topleft)
        pygame.draw.rect(surface, COLORS['hot_pink'], panel, 3, border_radius=16)

        title = self.font_medium.render("Has perdido todas las vidas", True, COLORS['deep_pink'])
        surface.blit(title, title.get_rect(center=(panel.centerx, panel.top + 46)))

        subtitle = self.font_small.render("Tendr\u00e1s que volver a recoger las fresas", True, COLORS['text'])
        surface.blit(subtitle, subtitle.get_rect(center=(panel.centerx, panel.top + 72)))

        self._draw_button(surface, layout['retry'], "Reintentar", COLORS['hot_pink'])
        self._draw_button(surface, layout['exit'], "Salir al men\u00fa principal", COLORS['text_light'])

    def _draw_slider(self, surface, rect, value):
        pygame.draw.rect(surface, (255, 255, 255), rect, border_radius=8)
        fill_w = int(rect.width * value)
        if fill_w > 0:
            pygame.draw.rect(surface, COLORS['hot_pink'], (rect.left, rect.top, fill_w, rect.height), border_radius=8)
        knob_x = rect.left + int(rect.width * value)
        pygame.draw.circle(surface, COLORS['deep_pink'], (knob_x, rect.centery), rect.height // 2 + 4)
        pygame.draw.circle(surface, (255, 255, 255), (knob_x, rect.centery), rect.height // 2 + 1)

    def _draw_combo(self, surface, rect, items):
        pygame.draw.rect(surface, (255, 255, 255), rect, border_radius=10)
        pygame.draw.rect(surface, COLORS['hot_pink'], rect, 2, border_radius=10)
        name = music_gen.track_name(self.game.music_track)
        t = self.font_small.render(name, True, COLORS['text'])
        surface.blit(t, (rect.left + 12, rect.centery - t.get_height() // 2))
        pygame.draw.polygon(surface, COLORS['hot_pink'], [
            (rect.right - 20, rect.centery - 4),
            (rect.right - 10, rect.centery - 4),
            (rect.right - 15, rect.centery + 5)])
        for i, r in enumerate(items):
            key = self.track_keys[i]
            selected = key == self.game.music_track
            pygame.draw.rect(surface, (255, 240, 244) if selected else (255, 255, 255), r, border_radius=8)
            pygame.draw.rect(surface, COLORS['hot_pink'] if selected else (230, 210, 216), r, 1, border_radius=8)
            name_i = music_gen.track_name(key)
            t = self.font_small.render(name_i, True, COLORS['text'])
            surface.blit(t, (r.left + 12, r.centery - t.get_height() // 2))

    def _draw_menu(self, surface):
        alpha = int(160 * self.menu_timer)
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((30, 10, 25, alpha))
        surface.blit(overlay, (0, 0))

        layout = self._menu_layout()
        panel = layout['panel']

        panel_surf = pygame.Surface((panel.width, panel.height), pygame.SRCALPHA)
        panel_surf.fill((255, 220, 230, 245))
        surface.blit(panel_surf, panel.topleft)
        pygame.draw.rect(surface, COLORS['hot_pink'], panel, 3, border_radius=16)

        title = self.font_medium.render("Pausa", True, COLORS['deep_pink'])
        surface.blit(title, title.get_rect(center=(panel.centerx, panel.top + 32)))

        self._draw_button(surface, layout['resume'], "Reanudar", COLORS['hot_pink'])

        label = self.font_small.render("Volumen de m\u00fasica", True, COLORS['text'])
        surface.blit(label, layout['vol_label'])
        self._draw_slider(surface, layout['vol_slider'], self.game.music_volume)

        label = self.font_small.render("Canci\u00f3n de fondo", True, COLORS['text'])
        surface.blit(label, layout['song_label'])
        self._draw_combo(surface, layout['combo'], layout['items'])

        label = self.font_small.render("Brillo", True, COLORS['text'])
        surface.blit(label, layout['bright_label'])
        bright_norm = max(0.0, min(1.0, (self.game.brightness - 0.5) / 1.0))
        self._draw_slider(surface, layout['bright_slider'], bright_norm)

        self._draw_button(surface, layout['exit'], "Salir al selector de niveles", COLORS['text_light'])

    def _draw_hud(self, surface):
        bar = pygame.Surface((SCREEN_WIDTH, 46), pygame.SRCALPHA)
        bar.fill((255, 209, 220, 175))
        pygame.draw.line(bar, COLORS['hot_pink'], (0, 45), (SCREEN_WIDTH, 45), 2)
        surface.blit(bar, (0, 0))

        name_text = self.font_small.render(self.game.player_name, True, COLORS['text'])
        surface.blit(name_text, (12, 4))
        level_text = self.font_small.render(
            f"Nivel {self.level_data['id']}: {self.level_data['name']}", True, COLORS['text'])
        surface.blit(level_text, (12, 25))

        heart_x = SCREEN_WIDTH - 204
        for i in range(self.player.max_hp):
            heart_surf = self._heart_full if i < self.player.hp else self._heart_empty
            surface.blit(heart_surf, (heart_x + i * 24, 13))

        straw_icon = get_sprite('strawberry')
        surface.blit(straw_icon, (SCREEN_WIDTH - 44, 6))
        count_text = self.font_small.render(
            f"{self.strawberries_collected}/{self.total_strawberries}", True, COLORS['text'])
        surface.blit(count_text, (SCREEN_WIDTH - 44, 27))
