import pygame
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT


class Camera:
    def __init__(self, map_width, map_height, tile_size):
        self.tile_size = tile_size
        self.map_pixel_width = map_width * tile_size
        self.map_pixel_height = map_height * tile_size
        self.x = 0.0
        self.y = 0.0
        self._target_x = 0.0
        self._target_y = 0.0
        self.ox = 0
        self.oy = 0
        self.smoothing = 8.0
        self.lookahead = 70.0
        self.shake_time = 0.0
        self.shake_mag = 0.0

    def follow(self, target_rect, player_vx=0, dt=None):
        target_x = target_rect.centerx - SCREEN_WIDTH // 2
        target_y = target_rect.centery - SCREEN_HEIGHT // 2
        if abs(player_vx) > 10:
            target_x += player_vx * 0.18
        target_y -= 24

        self._target_x = max(0, min(target_x, self.map_pixel_width - SCREEN_WIDTH))
        self._target_y = max(0, min(target_y, self.map_pixel_height - SCREEN_HEIGHT))

        if dt:
            k = min(1.0, dt * self.smoothing)
            self.x += (self._target_x - self.x) * k
            self.y += (self._target_y - self.y) * k
        else:
            self.x = self._target_x
            self.y = self._target_y

    def shake(self, magnitude, duration):
        self.shake_mag = magnitude
        self.shake_time = max(self.shake_time, duration)

    def update_shake(self, dt):
        if self.shake_time > 0:
            self.shake_time -= dt
            mag = self.shake_mag * max(0.0, self.shake_time * 4)
            self.ox = random.randint(-1, 1) * int(mag)
            self.oy = random.randint(-1, 1) * int(mag)
            return (self.ox, self.oy)
        self.ox = 0
        self.oy = 0
        return (0, 0)

    def apply(self, rect):
        return rect.move(int(-self.x) + self.ox, int(-self.y) + self.oy)

    def apply_point(self, point):
        return (point[0] - int(self.x) + self.ox, point[1] - int(self.y) + self.oy)
