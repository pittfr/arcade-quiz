import pygame
from states import GameState
from config import *
from ui import *
from utils import ease_in_out

class GameoverState(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.default_font = pygame.font.Font(DEFAULT_FONT_PATH, 64)
        
        self.logoPath = "assets/images/logo.png"
        self.logoImage = Image(
                            pos=(10, 10),
                            image_path=self.logoPath,
                            scale=0.1,
                            anchor="topleft",
                            opacity=0
                            )
        
        self.logoOpacity = 0
        self.targetLogoOpacity = 255

        self.circleRadius = 0
        self.targetCircleRadius = 250

        self.circle_animation_delay = 1.5
        self.circle_delay_timer = 0
        self.circle_animation_progress = 0
        self.circle_animation_duration = 4
        
        self.logo_animation_progress = 0
        self.logo_animation_duration = 3

    def handle_events(self, events, delta_time):
        pass

    def update(self, delta_time):
        if 0 <= self.logo_animation_progress <= 1:
            self.logo_animation_progress += delta_time / self.logo_animation_duration
            self.logo_animation_progress = min(self.logo_animation_progress, 1)

            logo_eased_progress = ease_in_out(self.logo_animation_progress)
            self.logoOpacity = int(self.targetLogoOpacity * logo_eased_progress)
            self.logoImage.setOpacity(self.logoOpacity)
        else:
            if self.logoOpacity != self.targetLogoOpacity:
                self.logoOpacity = self.targetLogoOpacity
                self.logoImage.setOpacity(self.logoOpacity)

        if self.circle_delay_timer < self.circle_animation_delay:
            # count down the delay timer
            self.circle_delay_timer += delta_time
        else:
            # once delay is over, start the animation
            if 0 <= self.circle_animation_progress <= 1:
                self.circle_animation_progress += delta_time / self.circle_animation_duration
                self.circle_animation_progress = min(self.circle_animation_progress, 1)

                eased_progress = ease_in_out(self.circle_animation_progress)
                self.circleRadius = self.targetCircleRadius * eased_progress
            else:
                if self.circleRadius != self.targetCircleRadius:
                    self.circleRadius = self.targetCircleRadius

    def enter(self):
        self.logo_animation_progress = 0
        self.circle_animation_progress = 0

        self.circle_delay_timer = 0
        self.circleRadius = 0

        self.logoOpacity = 0
        self.logoImage.setOpacity(0)

    def draw(self, delta_time, screen):
        self.game.screen.fill(BLUE)
        
        self.logoImage.draw(screen)

        pygame.draw.circle(screen, WHITE, (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2), self.circleRadius)