import pygame
import math
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE, COLORS
from sprites import get_sprite

_sky_cache = {}
_sun_cache = {}


def _mix(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))


def _palette_key(colors):
    if colors:
        return tuple(colors.values())
    return None


def get_sky(w, h, colors=None):
    key = (w, h, _palette_key(colors))
    if key not in _sky_cache:
        s = pygame.Surface((w, h))
        top = (colors or {}).get('sky_top', COLORS['sky_top'])
        mid = (colors or {}).get('sky_mid', COLORS['sky_mid'])
        bot = (colors or {}).get('sky_bottom', COLORS['sky_bottom'])
        for y in range(h):
            t = y / h
            if t < 0.5:
                tt = t / 0.5
                col = _mix(top, mid, tt)
            else:
                tt = (t - 0.5) / 0.5
                col = _mix(mid, bot, tt)
            pygame.draw.line(s, col, (0, y), (w, y))
        _sky_cache[key] = s
    return _sky_cache[key]


def get_sun(colors=None):
    key = _palette_key(colors)
    if key not in _sun_cache:
        r = 38
        s = pygame.Surface((r * 3, r * 3), pygame.SRCALPHA)
        c = r * 1.5
        sun_c = (colors or {}).get('sun', COLORS['sun'])
        hl = (colors or {}).get('sun_highlight', (255, 250, 222))
        pygame.draw.circle(s, sun_c, (c, c), r)
        pygame.draw.circle(s, hl, (c - r // 3, c - r // 3), r // 3)
        _sun_cache[key] = s
    return _sun_cache[key]

def make_hill_layer(height, base, dark, count, seed=1):
    W = SCREEN_WIDTH * 2
    surf = pygame.Surface((W, height), pygame.SRCALPHA)
    rng = random.Random(seed)
    for _ in range(count):
        x = rng.randint(-W // 2, W - 1)
        w = rng.randint(160, 380)
        h = rng.randint(70, max(80, height - 16))
        y = height + rng.randint(-14, 8)
        for dx in (0, W):
            cx = x + dx
            pygame.draw.ellipse(surf, dark, (cx, y - h, w, h * 2))
            pygame.draw.ellipse(surf, base, (cx, y - h, int(w * 0.9), int(h * 1.7)))
    return surf

def make_ground_layer(height, seed=1):
    W = SCREEN_WIDTH * 2
    surf = pygame.Surface((W, height), pygame.SRCALPHA)
    dirt = COLORS['dirt']
    dirt_d = COLORS['dirt_dark']
    for yy in range(height):
        t = yy / height
        col = _mix(dirt_d, dirt, t * t)
        pygame.draw.line(surf, col, (0, yy), (W, yy))
    pygame.draw.rect(surf, COLORS['grass_dark'], (0, 0, W, 12))
    pygame.draw.rect(surf, COLORS['grass_top'], (0, 0, W, 8))
    rng = random.Random(seed)
    for _ in range(30):
        x = rng.uniform(0, W)
        y = rng.uniform(20, 130)
        deco = rng.choice(['flower_pink', 'flower_yellow', 'flower_white', 'tuft'])
        sp = get_sprite(deco)
        surf.blit(sp, (x, y - sp.get_height() + 16))
    return surf

def blit_tiled(surface, layer, y, offset):
    W = layer.get_width()
    ox = int(offset) % W
    surface.blit(layer, (ox - W, y))
    surface.blit(layer, (ox, y))

def make_sparkles(count, seed=5):
    rng = random.Random(seed)
    sparkles = []
    for _ in range(count):
        sparkles.append({
            'x': rng.uniform(0, SCREEN_WIDTH),
            'y': rng.uniform(10, SCREEN_HEIGHT * 0.78),
            'phase': rng.uniform(0, math.pi * 2),
            'speed': rng.uniform(1.2, 3.0),
            'size': rng.uniform(1.6, 3.4),
            'color': rng.choice([(255, 255, 255), (255, 244, 214), (255, 216, 238)]),
        })
    return sparkles

def draw_sparkles(surface, sparkles, t, offset=0):
    for sp in sparkles:
        a = (math.sin(t * sp['speed'] + sp['phase']) + 1) / 2
        if a < 0.10:
            continue
        x = int((sp['x'] - offset) % SCREEN_WIDTH)
        y = int(sp['y'])
        s = max(2, int(sp['size'] * 3.0))
        img = pygame.Surface((s * 2 + 1, s * 2 + 1), pygame.SRCALPHA)
        col = (sp['color'][0], sp['color'][1], sp['color'][2], int(255 * a))
        pygame.draw.circle(img, col, (s, s), max(1, s // 2))
        pygame.draw.line(img, col, (0, s), (s * 2, s), 1)
        pygame.draw.line(img, col, (s, 0), (s, s * 2), 1)
        surface.blit(img, (x - s, y - s))

class MenuBackground:
    """Shared background for the menu-style scenes."""

    def __init__(self, game=None):
        self.game = game
        self.t = 0.0
        self.hills_far = make_hill_layer(220, COLORS['hill_far'], COLORS['hill_far_dark'], 12, seed=3)
        self.hills_mid = make_hill_layer(190, COLORS['hill_mid'], COLORS['hill_mid_dark'], 11, seed=11)
        self.ground = make_ground_layer(150, seed=99)
        self.sparkles = make_sparkles(22, seed=8)

    def draw(self, surface, dt):
        self.t += dt
        surface.blit(get_sky(SCREEN_WIDTH, SCREEN_HEIGHT), (0, 0))
        surface.blit(get_sun(), (SCREEN_WIDTH - 200, 64))
        if self.game is None or self.game.gfx_parallax:
            blit_tiled(surface, self.hills_far, 264, self.t * 1.6)
            blit_tiled(surface, self.hills_mid, 328, self.t * 2.4)
        blit_tiled(surface, self.ground, 13 * TILE_SIZE, self.t * 1.2)
        if self.game is None or self.game.gfx_sparkles:
            draw_sparkles(surface, self.sparkles, self.t)
