import os
import pygame
from settings import (
    LOGICAL_WIDTH, LOGICAL_HEIGHT,
    DISPLAY_WIDTH, DISPLAY_HEIGHT, QUALITY_SCALES,
    FPS, TITLE, VERSION, COLORS,
)
from scenes.login_scene import LoginScene
from scenes.level_select_scene import LevelSelectScene
from scenes.game_scene import GameScene
from scenes.victory_scene import VictoryScene
from scenes.bonus_intro_scene import BonusIntroScene
from music import music_gen


class Game:
    def __init__(self):
        pygame.mixer.pre_init(22050, -16, 2, 512)
        pygame.init()
        pygame.display.set_caption(TITLE)
        self.gfx_quality = 'Alta'
        self.gfx_particles = True
        self.gfx_parallax = True
        self.gfx_clouds = True
        self.gfx_sparkles = True
        self.display_width, self.display_height = self._compute_display_size(self.gfx_quality)
        self.scale = self.display_width / LOGICAL_WIDTH
        self.screen = pygame.display.set_mode((self.display_width, self.display_height))
        self.canvas = pygame.Surface((LOGICAL_WIDTH, LOGICAL_HEIGHT))
        self.fullscreen = False
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'login'
        self.player_name = ""
        self.current_level = 1
        self.completed_levels = set()
        self.level_strawberries = {}
        self.music_track = 'fresa'
        self.music_volume = 0.45
        self.brightness = 0.95
        self._dim_overlay = pygame.Surface((LOGICAL_WIDTH, LOGICAL_HEIGHT))
        self._dim_overlay.fill((0, 0, 0))
        self._bright_overlay = pygame.Surface((LOGICAL_WIDTH, LOGICAL_HEIGHT))
        self._bright_overlay.fill((255, 255, 255))
        self._version_font = pygame.font.Font(None, 20)
        self._version_surf = self._version_font.render(f"v{VERSION}", True, COLORS['text_light'])

        self.scenes = {
            'login': LoginScene(self),
            'level_select': LevelSelectScene(self),
            'game': GameScene(self),
            'victory': VictoryScene(self),
            'bonus_intro': BonusIntroScene(self),
        }

    @staticmethod
    def _compute_display_size(quality='Alta'):
        """Best-fit window size so the whole logical canvas fits the monitor."""
        try:
            os.environ.setdefault('SDL_VIDEO_CENTERED', '1')
            desktop = pygame.display.get_desktop_sizes()
            monitor_w, monitor_h = desktop[0] if desktop else (0, 0)
        except Exception:
            monitor_w, monitor_h = 0, 0
        if monitor_w <= 0 or monitor_h <= 0:
            try:
                info = pygame.display.Info()
                monitor_w, monitor_h = info.current_w, info.current_h
            except Exception:
                monitor_w, monitor_h = 0, 0
        if monitor_w <= 0 or monitor_h <= 0:
            monitor_w, monitor_h = DISPLAY_WIDTH, DISPLAY_HEIGHT
        target = QUALITY_SCALES.get(quality, 2.0)
        scale = min(monitor_w / LOGICAL_WIDTH, monitor_h / LOGICAL_HEIGHT, target)
        return int(LOGICAL_WIDTH * scale), int(LOGICAL_HEIGHT * scale)

    def apply_graphics(self):
        """Recreate the window after a graphics setting change."""
        self.display_width, self.display_height = self._compute_display_size(self.gfx_quality)
        self.scale = self.display_width / LOGICAL_WIDTH
        size = (self.display_width, self.display_height)
        flags = pygame.FULLSCREEN if self.fullscreen else 0
        self.screen = pygame.display.set_mode(size, flags)

    def _toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            info = pygame.display.Info()
            size = (info.current_w, info.current_h)
            flags = pygame.FULLSCREEN
        else:
            size = (self.display_width, self.display_height)
            flags = 0
        self.screen = pygame.display.set_mode(size, flags)

    def change_state(self, new_state):
        self.state = new_state
        scene = self.scenes.get(new_state)
        if hasattr(scene, 'on_enter'):
            scene.on_enter()
        if new_state == 'game':
            scene.load_level(self.current_level)
            music_gen.set_volume(self.music_volume)
            music_gen.start_music(self.music_track)
        elif new_state in ('level_select', 'bonus_intro'):
            music_gen.set_volume(self.music_volume)
            music_gen.start_music(self.music_track)

    def _apply_brightness(self):
        if abs(self.brightness - 1.0) < 0.001:
            return
        if self.brightness < 1.0:
            overlay = self._dim_overlay
            alpha = int((1.0 - self.brightness) * 192)
        else:
            overlay = self._bright_overlay
            alpha = int((self.brightness - 1.0) * 90)
        overlay.set_alpha(alpha)
        self.canvas.blit(overlay, (0, 0))

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                    self._toggle_fullscreen()
                else:
                    scene = self.scenes.get(self.state)
                    if scene:
                        scene.handle_event(event)
            scene = self.scenes.get(self.state)
            if scene:
                scene.update(dt)
                scene.draw(self.canvas)
            self.canvas.blit(self._version_surf,
                             (LOGICAL_WIDTH - self._version_surf.get_width() - 8,
                              LOGICAL_HEIGHT - self._version_surf.get_height() - 6))
            self._apply_brightness()
            pygame.transform.scale(self.canvas, (self.display_width, self.display_height), self.screen)
            pygame.display.flip()
        music_gen.stop_music()
        pygame.quit()
