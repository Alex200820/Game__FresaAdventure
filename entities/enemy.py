import pygame
import math
from settings import (
    TILE_SIZE, GRAVITY, MAX_FALL_SPEED, SOLID_TILES, COLORS,
)

ENEMY_WIDTH = 20
ENEMY_HEIGHT = 28
ENEMY_SPEED = 75


class Enemy:
    def __init__(self, x, y, direction=1):
        self.pos = pygame.math.Vector2(float(x), float(y))
        self.rect = pygame.Rect(int(x), int(y), ENEMY_WIDTH, ENEMY_HEIGHT)
        self.dir = direction
        self.vy = 0.0
        self.on_ground = False
        self.walk_frame = 0.0

    def _solid(self, grid, col, row):
        if col < 0 or col >= len(grid[0]):
            return True
        if row < 0 or row >= len(grid):
            return False
        return grid[row][col] in SOLID_TILES

    def update(self, dt, grid):
        ts = TILE_SIZE
        self.walk_frame += dt * 6

        # --- horizontal patrol (keep float accumulation so sub-pixel
        # movement is not lost to int() truncation) ---
        self.pos.x += self.dir * ENEMY_SPEED * dt
        self.rect.x = int(self.pos.x)

        top = max(0, self.rect.top // ts)
        bottom = min(len(grid) - 1, (self.rect.bottom - 1) // ts)
        if self.dir > 0:
            col = (self.rect.right) // ts
            hit = col >= len(grid[0])
            if not hit:
                for row in range(top, bottom + 1):
                    if self._solid(grid, col, row):
                        hit = True
                        break
            if hit:
                self.rect.right = min(col * ts, len(grid[0]) * ts)
                self.pos.x = float(self.rect.x)
                self.dir = -1
        else:
            col = (self.rect.left - 1) // ts
            hit = col < 0
            if not hit:
                for row in range(top, bottom + 1):
                    if self._solid(grid, col, row):
                        hit = True
                        break
            if hit:
                self.rect.left = max(0, (col + 1) * ts)
                self.pos.x = float(self.rect.x)
                self.dir = 1

        # --- vertical ---
        self.vy = min(self.vy + GRAVITY * dt, MAX_FALL_SPEED)
        self.pos.y += self.vy * dt
        self.rect.y = int(self.pos.y)
        self.on_ground = False
        top = max(0, self.rect.top // ts)
        bottom = min(len(grid) - 1, (self.rect.bottom - 1) // ts)
        left = max(0, self.rect.left // ts)
        right = min(len(grid[0]) - 1, (self.rect.right - 1) // ts)
        for row in range(top, bottom + 1):
            for col in range(left, right + 1):
                if grid[row][col] in SOLID_TILES:
                    tile_rect = pygame.Rect(col * ts, row * ts, ts, ts)
                    if self.rect.colliderect(tile_rect):
                        if self.vy > 0:
                            self.rect.bottom = tile_rect.top
                        elif self.vy < 0:
                            self.rect.top = tile_rect.bottom
                        self.vy = 0
        self.pos.y = float(self.rect.y)

        # --- grounded check: solid tile directly under the feet ---
        below_row = (self.rect.bottom + 1) // ts
        if 0 <= below_row < len(grid):
            below_left = max(0, self.rect.left // ts)
            below_right = min(len(grid[0]) - 1, (self.rect.right - 1) // ts)
            if any(grid[below_row][c] in SOLID_TILES for c in range(below_left, below_right + 1)):
                self.on_ground = True

        # --- turn around before walking off a ledge ---
        if self.on_ground:
            ahead_col = (self.rect.right + 2) // ts if self.dir > 0 else (self.rect.left - 2) // ts
            below_row = (self.rect.bottom + 2) // ts
            if below_row >= len(grid) or not self._solid(grid, ahead_col, below_row):
                self.dir *= -1

    def draw(self, surface, camera):
        screen_rect = camera.apply(self.rect)
        cx = screen_rect.centerx
        cy = screen_rect.centery + 2

        red = COLORS['strawberry']
        dark = COLORS['strawberry_top']
        seed = COLORS['gold']
        face = COLORS['white']
        eye = COLORS['dog_eye']

        pygame.draw.ellipse(surface, red, (cx - 9, cy - 8, 18, 18))
        for sx, sy in [(-4, -3), (4, -3), (0, 1), (-5, 3), (5, 3)]:
            pygame.draw.circle(surface, seed, (cx + sx, cy + sy), 1)
        pygame.draw.ellipse(surface, dark, (cx - 6, cy - 12, 12, 6))
        pygame.draw.line(surface, COLORS['grass_dark'], (cx, cy - 9), (cx, cy - 12), 2)

        pygame.draw.circle(surface, face, (cx - 4, cy - 3), 3)
        pygame.draw.circle(surface, face, (cx + 4, cy - 3), 3)
        pygame.draw.circle(surface, eye, (cx - 4, cy - 3), 2)
        pygame.draw.circle(surface, eye, (cx + 4, cy - 3), 2)
        pygame.draw.line(surface, eye, (cx - 7, cy - 7), (cx - 2, cy - 5), 2)
        pygame.draw.line(surface, eye, (cx + 7, cy - 7), (cx + 2, cy - 5), 2)

        step = int(2 * math.sin(self.walk_frame))
        pygame.draw.ellipse(surface, dark, (cx - 6, cy + 8, 5, 3))
        pygame.draw.ellipse(surface, dark, (cx + 1, cy + 8 + step, 5, 3))
