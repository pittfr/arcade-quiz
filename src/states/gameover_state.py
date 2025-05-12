import pygame
from states import GameState
from config import *
from ui import *
from utils import ease_in_out
from utils.animation import Animation

class GameoverState(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.scoreLabel_font = pygame.font.Font(DEFAULT_FONT_PATH, 80)
        self.default_font = pygame.font.Font(DEFAULT_FONT_PATH, 130)
        
        self.circleRadius = 0
        self.foregroundOpacity = 0

        self.fireImage = Image(
                            pos=(int(WINDOW_WIDTH * 0.5), int(WINDOW_HEIGHT * 0.275)),
                            image_path=(IMAGES_PATH + "firecsm.png"),
                            scale=0.5
                            )
        
        self.scoreLabel = Label(
                            pos=(int(WINDOW_WIDTH * 0.5), int(WINDOW_HEIGHT * 0.45)),
                            text="Pontuação",
                            font=self.scoreLabel_font,
                            text_color=DARK_BLUE,
                            opacity=0
                            )
        
        self.scoreValueLabel = Label(
                            pos=(int(WINDOW_WIDTH * 0.5), int(WINDOW_HEIGHT * 0.575)),
                            text="20/20",
                            font=self.default_font,
                            text_color=DARK_BLUE,
                            opacity=0
                            )
        
        self.foregroundRect = pygame.Rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
        
        self.transitioning = False
        
        # create animations
        self.circle_animation = Animation(0, 300, 0.5, 1.0)
        self.fire_animation = Animation(0, 255, 0.5, 1.75)
        self.scoreLabel_animation = Animation(0, 255, 0.5, 2.0)
        self.scoreValue_animation = Animation(0, 255, 0.5, 2.25)

        self.foreground_animation = Animation(0, 255, 0.5)
        self.auto_transition_timer = 0

    def handle_events(self, events, delta_time):
        self.current_events = events
        for event in events:
            if event.type == pygame.KEYDOWN:
                if self.scoreValue_animation.is_complete and not self.transitioning:
                    self.transitioning = True
                    self.foreground_animation.reset()

    def update(self, delta_time):
        # update animations and apply their values
        self.circleRadius = self.circle_animation.update(delta_time)
        
        fire_opacity = int(self.fire_animation.update(delta_time))
        self.fireImage.setOpacity(fire_opacity)
        
        scoreLabel_opacity = int(self.scoreLabel_animation.update(delta_time))
        self.scoreLabel.setOpacity(scoreLabel_opacity)

        scoreValue_opacity = int(self.scoreValue_animation.update(delta_time))
        self.scoreValueLabel.setOpacity(scoreValue_opacity)

        if self.scoreValue_animation.is_complete and not self.transitioning:
            self.auto_transition_timer += delta_time
            if self.auto_transition_timer >= 5.0:
                self.transitioning = True
                self.foreground_animation.reset()

        if self.transitioning:
            self.foregroundOpacity = int(self.foreground_animation.update(delta_time))
            
            if self.foreground_animation.is_complete and self.foregroundOpacity >= 255:
                self.game.stateManager.changeState("starting")

    def enter(self):
        # convert score to string to ensure setText can handle it properly
        if hasattr(self.game, 'score'):
            score_text = f" {self.game.score}/20" if self.game.score < 10 else f"{self.game.score}/20"
        else:
            score_text = " 0/20"  # default if score is not set
            
        self.scoreValueLabel.setText(score_text)
        
        self.transitioning = False
        self.auto_transition_timer = 0
        
        # reset all animations when entering the state
        self.fire_animation.reset()
        self.circle_animation.reset()
        self.scoreLabel_animation.reset()
        self.scoreValue_animation.reset()
        self.foreground_animation.reset()        
        
        # reset UI elements
        self.circleRadius = 0
        self.fireImage.setOpacity(0)
        self.scoreLabel.setOpacity(0)
        self.scoreValueLabel.setOpacity(0)
        self.foregroundOpacity = 0


    def draw(self, delta_time, screen):
        self.game.screen.fill(BLUE)
        
        pygame.draw.circle(screen, WHITE, (int(WINDOW_WIDTH * 0.5), int(WINDOW_HEIGHT * 0.45)), int(self.circleRadius))

        self.scoreLabel.draw(screen)

        self.scoreValueLabel.draw(screen)

        self.fireImage.draw(screen)

        if self.foregroundOpacity > 0:
            foreground_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
            foreground_color = (*BLUE[:3], self.foregroundOpacity)
            foreground_surface.fill(foreground_color)
            screen.blit(foreground_surface, (0, 0))
        # pygame.draw.rect(screen, BLUE, self.foregroundRect)