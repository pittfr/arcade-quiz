import pygame
from states import GameState
from config import *
from ui import *
from utils.animation import Animation

class StartingState(GameState):
    def __init__(self, game):
        super().__init__(game)

        self.startingQuiz = False

        self.default_font = pygame.font.Font(DEFAULT_FONT_PATH, 80)

        self.foregroundOpacity = 0

        self.miguelistaImage = Image(
            pos=(WINDOW_WIDTH // 2, int(WINDOW_HEIGHT * 0.3)),
            image_path=IMAGES_PATH + "miguelista.png",
            scale=0
        )

        self.pressioneBotaoLabel = Label(
            pos=(WINDOW_WIDTH // 2, int(WINDOW_HEIGHT * 0.7)),
            text="Pressione um botão para começar",
            font=self.default_font
        )

        # create animations

        self.miguelistaImage_animation = Animation(0, 1, 1.0, 1.0)
        self.pressioneBotaoLabel_animation = Animation(0, 255, 1)

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
            # miguelista image animation
            miguelista_scale = self.miguelistaImage_animation.update(delta_time)
            self.miguelistaImage.setScale(miguelista_scale)

            # pressione botao label animation
            if self.miguelistaImage_animation.is_complete:
                pressione_botao_opacity = int(self.pressioneBotaoLabel_animation.update(delta_time))
                self.pressioneBotaoLabel.setOpacity(pressione_botao_opacity)

    def enter(self):
        self.startingQuiz = False

        # reset all animations when entering the state
        self.miguelistaImage_animation.reset()
        self.pressioneBotaoLabel_animation.reset()
        self.foreground_animation.reset()

        # reset UI elements
        self.miguelistaImage.setScale(0)
        self.pressioneBotaoLabel.setOpacity(0)
        self.foregroundOpacity = 0

    def draw(self, delta_time, screen):
        self.game.screen.fill(BLUE)

        if self.miguelistaImage.scale > 0:
            self.miguelistaImage.draw(screen)

        if self.pressioneBotaoLabel.opacity > 0:
            self.pressioneBotaoLabel.draw(screen)

        if self.foregroundOpacity > 0:
            foreground_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
            foreground_color = (*BLUE[:3], self.foregroundOpacity)
            foreground_surface.fill(foreground_color)
            screen.blit(foreground_surface, (0, 0))
        # pygame.draw.rect(screen, BLUE, self.foregroundRect)