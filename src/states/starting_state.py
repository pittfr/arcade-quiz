import pygame
from states import GameState
from config import *
from ui import *
from utils.animation import Animation

class StartingState(GameState):
    def __init__(self, game):
        super().__init__(game)

        self.startingQuiz = False

        self.default_font = pygame.font.Font(DEFAULT_FONT_PATH, 120)

        self.foregroundOpacity = 0

        self.quizLabel = Label(
                            pos=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2.3),
                            font=self.default_font,
                            visible=True,
                            text="QUIZ",
                            opacity=0
                            )

        self.informaticaLabel = Label(
                            pos=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 1.75),
                            font=self.default_font,
                            visible=True,
                            text="INFORMÁTICA",
                            opacity=0
                            )
        
        self.fireImage = Image(
                            pos=(WINDOW_WIDTH // 2, WINDOW_HEIGHT// 3.5),
                            image_path="assets/images/firecsm.png",
                            scale=0.3,
                            opacity=0,
                            )
        
        fireDimensions = self.fireImage.getDimensions()

        self.fireBoxBaseDimensions = (fireDimensions[0] * 3.5, fireDimensions[1] * 1.3)

        self.fireBox = pygame.Rect(0, 0, 0, 0)
        self.fireBox.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT// 3.5)
        self.fireBoxRadius = 75

        # create animations

        self.quizLabel_animation = Animation(0, 255, 4.0, 3.0)
        self.informaticaLabel_animation = Animation(0, 255, 4.0, 5.5)
        self.fireBox_animation = Animation(0.0, 1.0, 3.5, 8.0)
        self.fireImage_animation = Animation(0, 255, 4.0, 10.5)


        self.foreground_animation = Animation(0, 255, 4.0)

        self.current_events = []

    def handle_events(self, events, delta_time):
        self.current_events = events
        for event in events:
            if event.type == pygame.KEYDOWN:
                if self.fireImage_animation.is_complete:
                    self.startingQuiz = True

    def update(self, delta_time):
        if self.startingQuiz:
            self.foregroundOpacity = int(self.foreground_animation.update(delta_time))

            if self.foreground_animation.is_complete and self.foregroundOpacity >= 255:
                self.game.stateManager.changeState("quiz")
        else:
            # fire box animation
            scale_factor = self.fireBox_animation.update(delta_time)
            
            new_width = int(self.fireBoxBaseDimensions[0] * scale_factor)
            new_height = int(self.fireBoxBaseDimensions[1] * scale_factor)
            
            center = self.fireBox.center
            
            self.fireBox.width = new_width
            self.fireBox.height = new_height
            
            self.fireBox.center = center

            # fire image animation
            fire_opacity = int(self.fireImage_animation.update(delta_time))
            self.fireImage.setOpacity(fire_opacity)

            # quiz label animation
            quiz_opacity = int(self.quizLabel_animation.update(delta_time))
            self.quizLabel.setOpacity(quiz_opacity)

            # informatica label animation
            informatica_opacity = int(self.informaticaLabel_animation.update(delta_time))
            self.informaticaLabel.setOpacity(informatica_opacity)

    def enter(self):
        self.startingQuiz = False

        # reset all animations when entering the state
        self.informaticaLabel_animation.reset()
        self.quizLabel_animation.reset()
        self.fireBox_animation.reset()
        self.fireImage_animation.reset()
        self.foreground_animation.reset()

        # reset UI elements
        self.informaticaLabel.setOpacity(0)
        self.quizLabel.setOpacity(0)
        self.fireBox.width = 0
        self.fireBox.height = 0
        self.fireBox.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3.5)
        self.fireImage.setOpacity(0)
        self.foregroundOpacity = 0

    def draw(self, delta_time, screen):
        self.game.screen.fill(BLUE)

        self.quizLabel.draw(screen)
        self.informaticaLabel.draw(screen)

        pygame.draw.rect(screen, DARK_BLUE, self.fireBox, 0, self.fireBoxRadius)

        self.fireImage.draw(screen)

        if self.foregroundOpacity > 0:
            foreground_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
            foreground_color = (*BLUE[:3], self.foregroundOpacity)
            foreground_surface.fill(foreground_color)
            screen.blit(foreground_surface, (0, 0))
        # pygame.draw.rect(screen, BLUE, self.foregroundRect)