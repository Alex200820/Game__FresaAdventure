import pygame
import math
from settings import TILE_SIZE, COLORS

_surfaces = {}
_glow_cache = {}
_cloud_cache = {}

def get_sprite(name):
    if name not in _surfaces:
        generator = _generators.get(name)
        if generator:
            _surfaces[name] = generator()
        else:
            s = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
            s.fill((255, 0, 255, 0))
            _surfaces[name] = s
    return _surfaces[name]

def get_dynamic_sprite(name):
    generator = _generators.get(name)
    if generator:
        return generator()
    return get_sprite(name)

def get_cloud(scale):
    key = round(scale, 2)
    if key not in _cloud_cache:
        w, h = int(96 * key), int(40 * key)
        s = pygame.Surface((w, h), pygame.SRCALPHA)
        white = COLORS['cloud']
        shadow = COLORS['cloud_shadow']
        pygame.draw.ellipse(s, shadow, (int(w * 0.10), int(h * 0.68), int(w * 0.80), int(h * 0.24)))
        pygame.draw.ellipse(s, white, (int(w * 0.08), int(h * 0.40), int(w * 0.44), int(h * 0.44)))
        pygame.draw.ellipse(s, white, (int(w * 0.30), int(h * 0.26), int(w * 0.42), int(h * 0.52)))
        pygame.draw.ellipse(s, white, (int(w * 0.54), int(h * 0.42), int(w * 0.38), int(h * 0.42)))
        _cloud_cache[key] = s
    return _cloud_cache[key]

def get_glow(color, radius):
    key = (color, radius)
    if key not in _glow_cache:
        s = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        for i in range(radius, 0, -1):
            a = int(255 * (1 - i / radius) ** 1.5)
            pygame.draw.circle(s, (color[0], color[1], color[2], a), (radius, radius), i)
        _glow_cache[key] = s
    return _glow_cache[key]

def get_shadow():
    if 'shadow' not in _surfaces:
        s = pygame.Surface((28, 12), pygame.SRCALPHA)
        pygame.draw.ellipse(s, (60, 30, 40, 80), (0, 0, 28, 12))
        _surfaces['shadow'] = s
    return _surfaces['shadow']

def _draw_strawberry():
    s = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
    cx, cy = TILE_SIZE // 2, TILE_SIZE // 2 + 2
    r = 7
    pygame.draw.circle(s, (200, 40, 80), (cx, cy), r + 1)
    pygame.draw.circle(s, COLORS['strawberry'], (cx, cy), r)
    pygame.draw.circle(s, COLORS['strawberry_light'], (cx - 2, cy - 2), r - 3)
    leaf_points = [(cx, cy - r - 2), (cx - 5, cy - r + 3), (cx + 5, cy - r + 3)]
    pygame.draw.polygon(s, COLORS['strawberry_top'], leaf_points)
    dots = [(cx - 3, cy - 2), (cx + 2, cy - 3), (cx - 1, cy + 2), (cx + 3, cy + 1)]
    for dx, dy in dots:
        pygame.draw.circle(s, (255, 210, 210), (dx, dy), 1)
    return s

def _draw_grass():
    s = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
    s.fill(COLORS['dirt'])
    pygame.draw.rect(s, COLORS['dirt_dark'], (0, 0, TILE_SIZE, TILE_SIZE), 1)
    pygame.draw.rect(s, COLORS['grass_top'], (0, 0, TILE_SIZE, 8))
    pygame.draw.rect(s, (176, 232, 182), (0, 0, TILE_SIZE, 2))
    for i in range(4):
        x = 4 + i * 8
        pygame.draw.line(s, COLORS['grass_dark'], (x, 8), (x + 1, 4), 1)
        pygame.draw.line(s, (176, 232, 182), (x, 8), (x + 1, 5), 1)
    for i in range(3):
        x = 5 + (hash(str(i * 7)) % 22)
        y = 12 + (hash(str(i * 13)) % 16)
        pygame.draw.circle(s, COLORS['dirt_dark'], (x, y), 1)
        pygame.draw.circle(s, (200, 170, 130), (x + 1, y + 1), 1)
    return s

def _draw_brick():
    s = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
    s.fill(COLORS['brick'])
    pygame.draw.rect(s, COLORS['brick_light'], (0, 0, TILE_SIZE, 3))
    pygame.draw.line(s, COLORS['brick_dark'], (0, 0), (TILE_SIZE, 0), 1)
    pygame.draw.line(s, COLORS['brick_dark'], (0, TILE_SIZE // 2), (TILE_SIZE, TILE_SIZE // 2), 1)
    pygame.draw.line(s, COLORS['brick_dark'], (0, TILE_SIZE), (TILE_SIZE, TILE_SIZE), 1)
    pygame.draw.line(s, COLORS['brick_dark'], (TILE_SIZE // 2, 0), (TILE_SIZE // 2, TILE_SIZE // 2), 1)
    pygame.draw.line(s, COLORS['brick_light'], (TILE_SIZE // 4, TILE_SIZE // 2), (TILE_SIZE // 4, TILE_SIZE), 1)
    pygame.draw.line(s, COLORS['brick_light'], (TILE_SIZE * 3 // 4, TILE_SIZE // 2), (TILE_SIZE * 3 // 4, TILE_SIZE), 1)
    return s

def _draw_wall():
    s = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
    s.fill(COLORS['wall'])
    pygame.draw.rect(s, COLORS['wall_dark'], (1, 1, TILE_SIZE - 2, TILE_SIZE - 2), 1)
    pygame.draw.rect(s, (224, 208, 178), (1, 1, TILE_SIZE - 2, 3))
    pygame.draw.line(s, COLORS['wall_dark'], (TILE_SIZE // 2, 1), (TILE_SIZE // 2, TILE_SIZE - 2), 1)
    pygame.draw.line(s, COLORS['wall_dark'], (1, TILE_SIZE // 2), (TILE_SIZE - 2, TILE_SIZE // 2), 1)
    return s

def _mix(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))


def _draw_spike():
    s = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
    n = 4
    sw = TILE_SIZE // n
    base_y = TILE_SIZE - 3
    tip_h = 22

    pygame.draw.rect(s, COLORS['spike_base_dark'], (0, TILE_SIZE - 5, TILE_SIZE, 5))
    pygame.draw.rect(s, COLORS['spike_base'], (0, TILE_SIZE - 5, TILE_SIZE, 3))

    for i in range(n):
        x0 = i * sw
        xc = x0 + sw // 2
        top = base_y - tip_h
        for yy in range(top, base_y + 1):
            t = (yy - top) / tip_h
            half = max(1, int(sw / 2 * (1 - t)))
            col = _mix(COLORS['spike_light'], COLORS['spike_dark'], t)
            pygame.draw.line(s, col, (xc - half, yy), (xc + half, yy))

    for i in range(n):
        x0 = i * sw
        xc = x0 + sw // 2
        top = base_y - tip_h
        pygame.draw.line(s, (255, 235, 242), (xc, top + 2), (xc, top + 6), 1)

    for i in range(1, n):
        x = i * sw
        pygame.draw.line(s, COLORS['spike_base_dark'], (x, TILE_SIZE - 5), (x, base_y), 1)
    return s

def _draw_bush():
    s = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
    pygame.draw.circle(s, COLORS['bush'], (TILE_SIZE // 2, TILE_SIZE // 2 + 4), 12)
    pygame.draw.circle(s, COLORS['bush_dark'], (TILE_SIZE // 2 - 5, TILE_SIZE // 2 + 2), 9)
    pygame.draw.circle(s, COLORS['bush'], (TILE_SIZE // 2 + 6, TILE_SIZE // 2 + 5), 7)
    pygame.draw.circle(s, (170, 210, 160), (TILE_SIZE // 2 - 4, TILE_SIZE // 2 - 1), 3)
    for dx, dy, c in ((6, 3, COLORS['deco_pink']), (-7, 8, COLORS['deco_yellow']), (9, 9, COLORS['deco_pink'])):
        pygame.draw.circle(s, c, (TILE_SIZE // 2 + dx, TILE_SIZE // 2 + dy), 2)
    return s

def _draw_exit():
    s = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
    t = pygame.time.get_ticks() / 1000
    w = TILE_SIZE
    pole_x = w // 2 - 2
    pygame.draw.rect(s, COLORS['exit_pole'], (pole_x, 4, 4, TILE_SIZE - 4))
    pygame.draw.rect(s, (150, 130, 105), (pole_x - 1, TILE_SIZE - 4, 6, 2))
    flag_h = 14
    flag_w = 16
    flag_y = 4 + int(3 * math.sin(t * 2))
    flag_pts = [
        (pole_x + 4, flag_y),
        (pole_x + 4 + flag_w, flag_y + flag_h // 2),
        (pole_x + 4, flag_y + flag_h),
    ]
    glow = int(120 + 80 * math.sin(t * 3))
    pygame.draw.polygon(s, (*COLORS['flag'][:3], glow), flag_pts)
    pygame.draw.polygon(s, (255, 140, 200), [
        (pole_x + 4, flag_y), (pole_x + 4 + flag_w - 4, flag_y + flag_h // 2), (pole_x + 4, flag_y + flag_h)])
    return s

def _draw_flower_pink():
    return _deco_flower(COLORS['deco_pink'])

def _draw_flower_yellow():
    return _deco_flower(COLORS['deco_yellow'])

def _draw_flower_white():
    return _deco_flower(COLORS['deco_white'])

def _draw_tuft():
    s = pygame.Surface((16, 18), pygame.SRCALPHA)
    for i in range(4):
        x = 4 + i * 3
        pygame.draw.line(s, COLORS['grass_blade'], (x, 18), (x + (i % 2), 8 + (i % 3)), 2)
    pygame.draw.line(s, (176, 232, 182), (3, 18), (4, 12), 2)
    return s

def _deco_flower(color):
    s = pygame.Surface((16, 22), pygame.SRCALPHA)
    pygame.draw.line(s, COLORS['grass_blade'], (8, 22), (8, 9), 2)
    pygame.draw.ellipse(s, COLORS['grass_blade'], (3, 12, 5, 9))
    for i in range(5):
        ang = i * math.pi * 2 / 5
        px = 8 + int(4 * math.cos(ang))
        py = 6 + int(4 * math.sin(ang))
        pygame.draw.circle(s, color, (px, py), 2)
    pygame.draw.circle(s, COLORS['deco_yellow'], (8, 6), 2)
    return s

_generators = {
    'strawberry': _draw_strawberry,
    'grass': _draw_grass,
    'brick': _draw_brick,
    'wall': _draw_wall,
    'spike': _draw_spike,
    'exit': _draw_exit,
    'bush': _draw_bush,
    'flower_pink': _draw_flower_pink,
    'flower_yellow': _draw_flower_yellow,
    'flower_white': _draw_flower_white,
    'tuft': _draw_tuft,
}

def clear_cached():
    _surfaces.clear()
    _glow_cache.clear()
    _cloud_cache.clear()
