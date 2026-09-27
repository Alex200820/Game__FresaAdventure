import pygame

# --- Resolution ----------------------------------------------------------
# The game renders internally at a compact logical resolution and is scaled
# up to whatever fits the current monitor. The window size is computed at
# runtime in game.Game from the desktop resolution, so the whole game always
# fits on the screen (laptops, small monitors, etc.).
LOGICAL_WIDTH = 960
LOGICAL_HEIGHT = 540
# Safety fallback used only if the monitor size cannot be detected.
DISPLAY_WIDTH = 1920
DISPLAY_HEIGHT = 1080

# --- Graphics quality ----------------------------------------------------
# Render scale applied over the logical resolution for each quality level.
# The scale is always clamped to the monitor so the window fits the screen.
QUALITY_ORDER = ['Baja', 'Media', 'Alta']
QUALITY_SCALES = {
    'Baja': 1.0,
    'Media': 1.5,
    'Alta': 2.0,
}
# Visual effects that can be toggled (attribute name on Game, menu label).
GRAPHICS_EFFECTS = [
    ('gfx_particles', 'Part\u00edculas'),
    ('gfx_parallax', 'Fondo animado'),
    ('gfx_clouds', 'Nubes'),
    ('gfx_sparkles', 'Destellos'),
]

TILE_SIZE = 32
FPS = 60
TITLE = "Fresa Adventure \u2727"
VERSION = "1.0.1"

# Backwards-compatible aliases used by the scenes (logical size).
SCREEN_WIDTH = LOGICAL_WIDTH
SCREEN_HEIGHT = LOGICAL_HEIGHT

# --- Player physics ------------------------------------------------------
PLAYER_MAX_HP = 6
GRAVITY = 2000
MAX_FALL_SPEED = 920
PLAYER_MOVE_SPEED = 300
ACCELERATION = 2600
AIR_ACCELERATION = 1800
FRICTION = 2600
AIR_FRICTION = 1100
STOP_THRESHOLD = 12
PLAYER_JUMP_SPEED = 640
JUMP_CUT_MULTIPLIER = 0.45
COYOTE_TIME = 0.1
JUMP_BUFFER_TIME = 0.13
SPIKE_DAMAGE = 1
KNOCKBACK_X = 260
KNOCKBACK_Y = -300
STOMP_BOUNCE = 380

SOLID_TILES = {1, 2, 3, 6}  # 6 = EXIT: la bandera es sólida para poder pararse encima

COLORS = {
    'pink': (255, 182, 193),
    'light_pink': (255, 209, 220),
    'hot_pink': (255, 105, 180),
    'deep_pink': (255, 20, 147),
    'white': (255, 255, 255),
    'black': (40, 20, 30),
    'grass_top': (152, 216, 160),
    'grass_dark': (130, 190, 140),
    'dirt': (180, 150, 110),
    'dirt_dark': (150, 125, 90),
    'brick': (200, 110, 130),
    'brick_dark': (170, 85, 105),
    'brick_light': (220, 140, 160),
    'wall': (201, 185, 154),
    'wall_dark': (170, 155, 125),
    'spike': (180, 130, 140),
    'spike_highlight': (200, 155, 165),
    'spike_dark': (150, 95, 120),
    'spike_light': (245, 190, 205),
    'spike_base': (170, 125, 150),
    'spike_base_dark': (135, 95, 118),
    'pit': (176, 136, 192),
    'pit_dark': (140, 100, 160),
    'strawberry': (255, 77, 109),
    'strawberry_light': (255, 130, 150),
    'strawberry_top': (126, 200, 80),
    'monkey_body': (212, 163, 115),
    'monkey_dark': (180, 130, 85),
    'monkey_face': (245, 230, 204),
    'monkey_ear': (230, 180, 140),
    'monkey_eye': (60, 40, 30),
    'monkey_mouth': (180, 100, 80),
    'girl_hair': (140, 92, 60),
    'girl_hair_dark': (115, 72, 46),
    'girl_skin': (255, 226, 196),
    'girl_dress': (255, 184, 200),
    'girl_dress_dark': (245, 155, 178),
    'girl_dress_light': (255, 214, 226),
    'girl_bow': (255, 140, 180),
    'girl_sock': (255, 255, 255),
    'girl_shoe': (255, 198, 220),
    'girl_blush': (255, 168, 182),
    'girl_eye': (70, 48, 56),
    'girl_mouth': (220, 120, 140),
    'dog_fur': (255, 236, 212),
    'dog_fur_dark': (232, 200, 170),
    'dog_ear': (188, 143, 106),
    'dog_ear_inner': (255, 205, 188),
    'dog_belly': (255, 250, 240),
    'dog_eye': (70, 48, 46),
    'dog_nose': (240, 130, 150),
    'dog_tongue': (255, 150, 168),
    'dog_collar': (255, 150, 190),
    'dog_paw': (232, 200, 170),
    'bush': (143, 188, 143),
    'bush_dark': (120, 165, 120),
    'exit': (255, 200, 50),
    'exit_glow': (255, 220, 100),
    'exit_pole': (200, 180, 150),
    'sky_top': (255, 178, 180),
    'sky_mid': (255, 214, 206),
    'sky_bottom': (255, 236, 228),
    'cloud': (255, 255, 255),
    'cloud_shadow': (240, 230, 235),
    'sun': (255, 240, 190),
    'sun_glow': (255, 218, 160),
    'hill_far': (232, 176, 196),
    'hill_far_dark': (214, 158, 182),
    'hill_mid': (188, 216, 176),
    'hill_mid_dark': (168, 200, 158),
    'hill_near': (150, 194, 150),
    'grass_blade': (120, 200, 120),
    'deco_yellow': (255, 214, 90),
    'deco_white': (255, 248, 250),
    'deco_pink': (255, 150, 190),
    'ui_bg': (255, 209, 220, 200),
    'ui_border': (255, 105, 180),
    'text': (80, 40, 60),
    'text_light': (180, 100, 140),
    'gold': (255, 215, 0),
    'heart': (255, 60, 90),
    'heart_empty': (200, 150, 160),
    'flower_pink': (255, 179, 198),
    'flower_yellow': (255, 230, 150),
    'flower_white': (255, 240, 245),
    'lock': (160, 140, 150),
    'flag': (255, 105, 180),
    'flag_pole': (200, 180, 150),
}

TILE_NAMES = {
    0: 'air',
    1: 'grass',
    2: 'brick',
    3: 'wall',
    4: 'spike',
    5: 'strawberry',
    6: 'exit',
    7: 'bush',
}

# --- Per-level background palettes (only sky/sun/hills, not the tiles) ----
LEVEL_THEMES = {
    1: dict(
        name='prado',
        sky_top=(255, 178, 180), sky_mid=(255, 214, 206), sky_bottom=(255, 236, 228),
        sun=(255, 240, 190), sun_highlight=(255, 250, 222),
        hill_far=(232, 176, 196), hill_far_dark=(214, 158, 182),
        hill_mid=(188, 216, 176), hill_mid_dark=(168, 200, 158),
    ),
    2: dict(
        name='fresas',
        sky_top=(255, 150, 165), sky_mid=(255, 196, 196), sky_bottom=(255, 226, 214),
        sun=(255, 225, 160), sun_highlight=(255, 245, 210),
        hill_far=(240, 152, 170), hill_far_dark=(222, 132, 152),
        hill_mid=(214, 168, 176), hill_mid_dark=(196, 148, 158),
    ),
    3: dict(
        name='colinas',
        sky_top=(128, 196, 252), sky_mid=(186, 226, 244), sky_bottom=(232, 246, 238),
        sun=(255, 247, 185), sun_highlight=(255, 252, 222),
        hill_far=(170, 206, 228), hill_far_dark=(150, 186, 210),
        hill_mid=(140, 212, 158), hill_mid_dark=(120, 194, 140),
    ),
    4: dict(
        name='bosque',
        sky_top=(118, 168, 142), sky_mid=(158, 202, 168), sky_bottom=(206, 232, 202),
        sun=(242, 236, 158), sun_highlight=(250, 244, 190),
        hill_far=(122, 168, 132), hill_far_dark=(104, 150, 114),
        hill_mid=(92, 152, 102), hill_mid_dark=(76, 132, 88),
    ),
    5: dict(
        name='laberinto',
        sky_top=(122, 92, 162), sky_mid=(162, 124, 182), sky_bottom=(212, 174, 206),
        sun=(255, 186, 222), sun_highlight=(255, 220, 240),
        hill_far=(152, 112, 182), hill_far_dark=(132, 96, 162),
        hill_mid=(112, 92, 152), hill_mid_dark=(96, 78, 136),
    ),
    6: dict(
        name='viento',
        sky_top=(158, 210, 255), sky_mid=(202, 232, 252), sky_bottom=(238, 246, 255),
        sun=(255, 250, 200), sun_highlight=(255, 254, 230),
        hill_far=(192, 216, 242), hill_far_dark=(172, 198, 226),
        hill_mid=(148, 202, 212), hill_mid_dark=(128, 184, 196),
    ),
    7: dict(
        name='jardin',
        sky_top=(148, 216, 182), sky_mid=(196, 236, 206), sky_bottom=(236, 248, 226),
        sun=(255, 240, 162), sun_highlight=(255, 250, 210),
        hill_far=(176, 216, 182), hill_far_dark=(156, 196, 162),
        hill_mid=(132, 196, 142), hill_mid_dark=(112, 176, 126),
    ),
    8: dict(
        name='helado',
        sky_top=(118, 180, 236), sky_mid=(176, 216, 242), sky_bottom=(226, 244, 250),
        sun=(236, 250, 255), sun_highlight=(250, 255, 255),
        hill_far=(166, 206, 236), hill_far_dark=(146, 186, 220),
        hill_mid=(122, 172, 216), hill_mid_dark=(102, 152, 200),
    ),
    9: dict(
        name='torre',
        sky_top=(198, 118, 92), sky_mid=(234, 164, 120), sky_bottom=(255, 214, 168),
        sun=(255, 198, 120), sun_highlight=(255, 228, 170),
        hill_far=(220, 138, 110), hill_far_dark=(200, 118, 96),
        hill_mid=(162, 120, 110), hill_mid_dark=(142, 100, 96),
    ),
    10: dict(
        name='paraiso',
        sky_top=(255, 148, 118), sky_mid=(255, 192, 140), sky_bottom=(255, 236, 192),
        sun=(255, 232, 140), sun_highlight=(255, 248, 190),
        hill_far=(250, 170, 130), hill_far_dark=(235, 150, 114),
        hill_mid=(255, 200, 150), hill_mid_dark=(240, 180, 134),
    ),
    11: dict(
        name='jardin_secreto',
        sky_top=(108, 176, 150), sky_mid=(178, 226, 190), sky_bottom=(240, 250, 224),
        sun=(255, 236, 158), sun_highlight=(255, 250, 206),
        hill_far=(206, 172, 230), hill_far_dark=(186, 152, 214),
        hill_mid=(146, 214, 168), hill_mid_dark=(124, 196, 148),
    ),
}
