import pygame
import math
from settings import (
    TILE_SIZE, GRAVITY, MAX_FALL_SPEED, PLAYER_MOVE_SPEED,
    ACCELERATION, AIR_ACCELERATION, FRICTION, AIR_FRICTION,
    PLAYER_JUMP_SPEED, JUMP_CUT_MULTIPLIER, COYOTE_TIME,
    JUMP_BUFFER_TIME, PLAYER_MAX_HP, SOLID_TILES, COLORS,
    KNOCKBACK_X, KNOCKBACK_Y,
)
from sprites import get_shadow
from music import play_sfx

PLAYER_WIDTH = 20
PLAYER_HEIGHT = 28


class Player:
    def __init__(self, x, y, name=""):
        self.name = name
        self.pos = pygame.math.Vector2(float(x), float(y))
        self.rect = pygame.Rect(int(x), int(y), PLAYER_WIDTH, PLAYER_HEIGHT)
        self.vx = 0.0
        self.vy = 0.0
        self.on_ground = False
        self.was_on_ground = False
        self.facing_right = True
        self.moving_left = False
        self.moving_right = False
        self.hp = PLAYER_MAX_HP
        self.max_hp = PLAYER_MAX_HP
        self.strawberries = 0
        self.dead = False
        self.invincible_timer = 0.0
        self.fell = False
        self.walk_frame = 0.0
        self.jumping = False
        self.coyote = 0.0
        self.jump_buffer = 0.0
        self.squash = 0.0
        self.stretch = 0.0
        self.land_impact = 0.0
        self.dust_timer = 0.0
        self.pending_dust = False
        self.just_landed = False

    def set_position(self, x, y):
        self.pos.x = float(x)
        self.pos.y = float(y)
        self.rect.topleft = (int(x), int(y))
        self.vx = 0
        self.vy = 0
        self.fell = False
        self.dead = False
        self.jumping = False
        self.squash = 0
        self.stretch = 0

    def move_left(self):
        self.moving_left = True

    def move_right(self):
        self.moving_right = True

    def stop_x(self):
        self.moving_left = False
        self.moving_right = False

    def jump(self):
        self.jump_buffer = JUMP_BUFFER_TIME

    def cut_jump(self):
        if self.vy < 0:
            self.vy *= JUMP_CUT_MULTIPLIER

    def _do_jump(self):
        self.vy = -PLAYER_JUMP_SPEED
        self.on_ground = False
        self.jumping = True
        self.coyote = 0
        self.jump_buffer = 0
        self.stretch = 1.0
        play_sfx('jump')

    def take_damage(self, amount, knockback_dir=1):
        if self.invincible_timer > 0:
            return
        self.hp -= amount
        self.invincible_timer = 1.2
        self.vx = knockback_dir * KNOCKBACK_X
        self.vy = KNOCKBACK_Y
        play_sfx('hurt')
        if self.hp <= 0:
            self.hp = 0
            self.dead = True

    def update(self, dt, grid):
        self.was_on_ground = self.on_ground
        self.just_landed = False
        self.pending_dust = False
        self.invincible_timer = max(0.0, self.invincible_timer - dt)
        self.squash = max(0.0, self.squash - dt * 3.2)
        self.stretch = max(0.0, self.stretch - dt * 3.2)

        # --- horizontal: smooth acceleration / friction ---
        if self.moving_left and not self.moving_right:
            self.facing_right = False
            self.vx -= (ACCELERATION if self.on_ground else AIR_ACCELERATION) * dt
        elif self.moving_right and not self.moving_left:
            self.facing_right = True
            self.vx += (ACCELERATION if self.on_ground else AIR_ACCELERATION) * dt
        else:
            friction = FRICTION if self.on_ground else AIR_FRICTION
            if self.vx > 0:
                self.vx = max(0.0, self.vx - friction * dt)
            elif self.vx < 0:
                self.vx = min(0.0, self.vx + friction * dt)
        if abs(self.vx) < 6:
            self.vx = 0.0
        self.vx = max(-PLAYER_MOVE_SPEED, min(PLAYER_MOVE_SPEED, self.vx))

        # --- vertical ---
        self.vy = min(self.vy + GRAVITY * dt, MAX_FALL_SPEED)

        # --- coyote time + jump buffering ---
        self.coyote = COYOTE_TIME if self.on_ground else max(0.0, self.coyote - dt)
        self.jump_buffer = max(0.0, self.jump_buffer - dt)
        if self.jump_buffer > 0 and self.coyote > 0:
            self._do_jump()

        # --- integrate (float accumulation for smooth motion) ---
        self.pos.x += self.vx * dt
        self.rect.x = int(self.pos.x)
        self._resolve_x(grid)
        self.pos.x = float(self.rect.x)

        impact_speed = self.vy
        self.pos.y += self.vy * dt
        self.rect.y = int(self.pos.y)
        self.on_ground = False
        self._resolve_y(grid)
        self.pos.y = float(self.rect.y)

        if self.on_ground and not self.was_on_ground:
            self.just_landed = True
            self.land_impact = min(1.0, impact_speed / MAX_FALL_SPEED)
            self.squash = 0.35 + 0.55 * self.land_impact
            self.jumping = False

        if self.rect.top > len(grid) * TILE_SIZE:
            self.fell = True

        # --- walk cycle + running dust ---
        if self.on_ground and abs(self.vx) > 40:
            self.walk_frame += abs(self.vx) * dt * 0.01
            self.dust_timer -= dt
            if self.dust_timer <= 0:
                self.dust_timer = 0.12
                self.pending_dust = True
        else:
            self.walk_frame += dt * 2
            self.dust_timer = 0.0

    def _resolve_x(self, grid):
        ts = TILE_SIZE
        top = max(0, self.rect.top // ts)
        bottom = min(len(grid) - 1, (self.rect.bottom - 1) // ts)
        left = max(0, self.rect.left // ts)
        right = min(len(grid[0]) - 1, (self.rect.right - 1) // ts)

        for row in range(top, bottom + 1):
            for col in range(left, right + 1):
                if grid[row][col] in SOLID_TILES:
                    tile_rect = pygame.Rect(col * ts, row * ts, ts, ts)
                    if self.rect.colliderect(tile_rect):
                        if self.vx > 0:
                            self.rect.right = tile_rect.left
                        elif self.vx < 0:
                            self.rect.left = tile_rect.right
                        if self.vx != 0:
                            self.vx = 0

    def _resolve_y(self, grid):
        ts = TILE_SIZE
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
                            self.on_ground = True
                            self.jumping = False
                        elif self.vy < 0:
                            self.rect.top = tile_rect.bottom
                        self.vy = 0

    def get_rect(self):
        return self.rect

    def draw(self, surface, camera):
        if self.invincible_timer > 0 and int(self.invincible_timer * 10) % 2 == 0:
            return

        screen_rect = camera.apply(self.rect)

        cx = screen_rect.centerx
        cy = screen_rect.centery + 2
        ground_y = screen_rect.bottom

        # soft shadow
        shadow = get_shadow()
        sh_w = int(22 * (1 + self.squash * 0.3) * (1 - self.stretch * 0.1))
        sh_w = max(12, sh_w)
        surface.blit(pygame.transform.scale(shadow, (sh_w, 10)), (cx - sh_w // 2, ground_y - 5))

        # squash & stretch
        sx = 1.0 + self.squash * 0.3 - self.stretch * 0.2
        sy = 1.0 - self.squash * 0.3 + self.stretch * 0.2
        bw = max(14, int(20 * sx))
        bh = max(14, int(18 * sy))

        fur = COLORS['dog_fur']
        fur_dark = COLORS['dog_fur_dark']
        ear = COLORS['dog_ear']
        ear_inner = COLORS['dog_ear_inner']
        belly = COLORS['dog_belly']
        eye = COLORS['dog_eye']
        nose = COLORS['dog_nose']
        tongue = COLORS['dog_tongue']
        collar = COLORS['dog_collar']
        paw = COLORS['dog_paw']

        # orejas caídas (detrás de la cabeza)
        pygame.draw.ellipse(surface, ear, (cx - 12, cy - 11, 6, 10))
        pygame.draw.ellipse(surface, ear_inner, (cx - 11, cy - 9, 3, 5))
        pygame.draw.ellipse(surface, ear, (cx + 6, cy - 11, 6, 10))
        pygame.draw.ellipse(surface, ear_inner, (cx + 8, cy - 9, 3, 5))

        # cabeza
        pygame.draw.ellipse(surface, fur, (cx - 8, cy - 8, 16, 16))

        # ojos grandes con brillo
        eye_dx = -3 if not self.facing_right else 3
        pygame.draw.circle(surface, eye, (cx + eye_dx, cy - 4), 2)
        pygame.draw.circle(surface, eye, (cx + eye_dx + 6, cy - 4), 2)
        pygame.draw.circle(surface, COLORS['white'], (cx + eye_dx + 1, cy - 5), 1)
        pygame.draw.circle(surface, COLORS['white'], (cx + eye_dx + 7, cy - 5), 1)

        # hocico
        mx = cx + (1 if self.facing_right else -1)
        pygame.draw.ellipse(surface, belly, (mx - 5, cy, 10, 7))
        pygame.draw.ellipse(surface, nose, (mx - 2, cy - 1, 4, 3))

        # boca y lengua
        if self.jumping:
            pygame.draw.circle(surface, nose, (mx + 1, cy + 3), 2)
        else:
            pygame.draw.line(surface, COLORS['girl_mouth'], (mx - 1, cy + 3), (mx + 3, cy + 3), 1)
            pygame.draw.ellipse(surface, tongue, (mx, cy + 4, 3, 3))

        # cuerpo con pancita
        torso_h = max(7, int(9 * sy))
        pygame.draw.ellipse(surface, fur, (cx - 8, cy + 1, 16, torso_h))
        pygame.draw.ellipse(surface, belly, (cx - 5, cy + 3, 10, 6))

        # collar
        pygame.draw.rect(surface, collar, (cx - 8, cy + 3, 16, 2))
        pygame.draw.circle(surface, COLORS['gold'], (cx, cy + 4), 1)

        # patitas delanteras
        if self.on_ground and abs(self.vx) > 10:
            arm_swing = int(3 * math.sin(self.walk_frame))
        else:
            arm_swing = 0
        pygame.draw.line(surface, fur, (cx - 6, cy + 4), (cx - 10, cy + 8 + arm_swing), 3)
        pygame.draw.line(surface, fur, (cx + 6, cy + 4), (cx + 10, cy + 8 - arm_swing), 3)

        # patas traseras con huellitas
        leg_offset = int(2 * math.sin(self.walk_frame)) if self.on_ground else 0
        pygame.draw.rect(surface, fur, (cx - 6, cy + 11, 4, 3))
        pygame.draw.ellipse(surface, paw, (cx - 7, cy + 13 + leg_offset, 5, 3))
        pygame.draw.rect(surface, fur, (cx + 2, cy + 11, 4, 3))
        pygame.draw.ellipse(surface, paw, (cx + 2, cy + 13 - leg_offset, 5, 3))

        # colita que se mueve
        wag = int(3 * math.sin(self.walk_frame * 1.4))
        tail_dir = -1 if not self.facing_right else 1
        pygame.draw.lines(surface, fur_dark, False, [
            (cx - tail_dir * 8, cy + 3),
            (cx - tail_dir * 12, cy - 1 + wag),
            (cx - tail_dir * 13, cy - 6 + wag),
        ], 2)

        if self.name:
            font = pygame.font.Font(None, 14)
            text = font.render(self.name, True, COLORS['text'])
            text_rect = text.get_rect(center=(cx, screen_rect.top - 6))
            surface.blit(text, text_rect)
