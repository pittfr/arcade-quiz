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
        self.pressioneBotao_font = pygame.font.Font(DEFAULT_FONT_PATH, 50)
        self.credits_font = pygame.font.Font(DEFAULT_FONT_PATH, 30)

        self.foregroundOpacity = 0

        self.miguelistaImage = Image(
                            pos=(WINDOW_WIDTH // 2, int(WINDOW_HEIGHT * 0.1)),
                            image_path=IMAGES_PATH + "miguelista.png",
                            scale=0
        )

        self.quizLabel = Label(
                            pos=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3.0),
                            font=self.default_font,
                            visible=True,
                            text="QUIZ",
                            opacity=0
                            )

        self.informaticaLabel = Label(
                            pos=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2.1),
                            font=self.default_font,
                            visible=True,
                            text="INFORMÁTICA",
                            opacity=0
                            )
        
        self.fireImage = Image(
                            pos=(WINDOW_WIDTH // 2, int(WINDOW_HEIGHT * 0.70)),
                            image_path=(IMAGES_PATH + "firecsm.png"),
                            scale=0.3,
                            opacity=0,
                            )
        
        fireDimensions = self.fireImage.getDimensions()

        self.fireBoxBaseDimensions = (fireDimensions[0] * 3.5, fireDimensions[1] * 1.3)

        self.fireBox = pygame.Rect(0, 0, 0, 0)
        self.fireBox.center = (WINDOW_WIDTH // 2, int(WINDOW_HEIGHT * 0.70))
        self.fireBoxRadius = 75

        self.pressioneBotaoLabel = Label(
                            pos=(WINDOW_WIDTH // 2, int(WINDOW_HEIGHT * 0.9)),
                            text="Pressione um botão para começar",
                            font=self.pressioneBotao_font
        )

        self.creditsLabel = Label(
                                pos=(WINDOW_WIDTH - 10, WINDOW_HEIGHT - 10),
                                text="David Pitt (11.º F) @ 2025",
                                font=self.credits_font,
                                anchor="bottomright",
                                opacity=0
                                )

        # create animations

        self.miguelistaImage_animation = Animation(0, .4, 1.0, 1.0)

        self.quizLabel_animation = Animation(0, 255, 0.5, 2.0)
        self.informaticaLabel_animation = Animation(0, 255, 0.5, 1.75)
        self.fireBox_animation = Animation(0.0, 1.0, 0.5, 2.25)
        self.fireImage_animation = Animation(0, 255, 0.5, 2.75)
        
        self.pressioneBotaoLabel_animation = Animation(0, 255, 1)

        self.creditsLabel_animation = Animation(0, 255, 0.5, 1.25)

        self.foreground_animation = Animation(0, 255, 0.5)

        self.current_events = []

    def handle_events(self, events, delta_time):
        self.current_events = events
        for event in events:
            if event.type == pygame.KEYDOWN:
                if self.pressioneBotaoLabel_animation.is_complete:
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

            # miguelista image animation
            miguelista_scale = self.miguelistaImage_animation.update(delta_time)
            self.miguelistaImage.setScale(miguelista_scale)

            # pressione botao label animation
            if self.fireImage_animation.is_complete:
                pressione_botao_opacity = int(self.pressioneBotaoLabel_animation.update(delta_time))
                self.pressioneBotaoLabel.setOpacity(pressione_botao_opacity)

            # credits label animation
            credits_opacity = int(self.creditsLabel_animation.update(delta_time))
            self.creditsLabel.setOpacity(credits_opacity)

    def enter(self):
        self.startingQuiz = False

        # reset all animations when entering the state
        self.miguelistaImage_animation.reset()
        self.informaticaLabel_animation.reset()
        self.quizLabel_animation.reset()
        self.fireBox_animation.reset()
        self.fireImage_animation.reset()
        self.pressioneBotaoLabel_animation.reset()
        self.creditsLabel_animation.reset()
        self.foreground_animation.reset()

        # reset UI elements
        self.informaticaLabel.setOpacity(0)
        self.quizLabel.setOpacity(0)
        self.fireBox.width = 0
        self.fireBox.height = 0
        self.fireBox.center = (WINDOW_WIDTH // 2, int(WINDOW_HEIGHT * 0.70))
        self.fireImage.setOpacity(0)
        self.miguelistaImage.setScale(0)
        self.pressioneBotaoLabel.setOpacity(0)
        self.creditsLabel.setOpacity(0)
        self.foregroundOpacity = 0

    def draw(self, delta_time, screen):
        self.game.screen.fill(DARK_BLUE)

        self.quizLabel.draw(screen)
        self.informaticaLabel.draw(screen)

        pygame.draw.rect(screen, DARKER_BLUE, self.fireBox, 0, self.fireBoxRadius)

        self.fireImage.draw(screen)

        if self.miguelistaImage.scale > 0:
            self.miguelistaImage.draw(screen)

        self.pressioneBotaoLabel.draw(screen)

        self.creditsLabel.draw(screen)

        if self.foregroundOpacity > 0:
            foreground_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
            foreground_color = (*DARK_BLUE[:3], self.foregroundOpacity)
            foreground_surface.fill(foreground_color)
            screen.blit(foreground_surface, (0, 0))
        # pygame.draw.rect(screen, BLUE, self.foregroundRect)