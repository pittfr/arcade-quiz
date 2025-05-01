import pygame
from states import GameState
from config import *
from ui import *

class StartingState(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.default_font = pygame.font.Font(DEFAULT_FONT_PATH, 90)
        self.start_font = pygame.font.Font(DEFAULT_FONT_PATH, 50)

        self.quizLabel = Label(
                            pos=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4),
                            font=self.default_font,
                            visible=True,
                            text="QUIZ"
                            )

        self.informaticaLabel = Label(
                            pos=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2.60),
                            font=self.default_font,
                            visible=True,
                            text="INFORMÁTICA"
                            )
        
        self.startLabel = Label(
                            pos=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 1.5),
                            font=self.start_font,
                            visible=True,
                            text="START!"
                            )
        
        self.startBox = pygame.Rect(0, 0, WINDOW_WIDTH // 4, WINDOW_HEIGHT // 8)
        self.startBox.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 1.5)

        self.fireImage = Image(
                            pos=(WINDOW_WIDTH // 2, WINDOW_HEIGHT// 8),
                            image_path="assets/images/firecsm.png",
                            scale=0.2
                            )
        
        fireDimensions = self.fireImage.getDimensions()

        self.fireBox = pygame.Rect(0, 0, fireDimensions[0] * 3.5, fireDimensions[1] * 1.3)
        self.fireBox.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT// 8)

        self.current_events = []

    def handle_events(self, events):
        self.current_events = events
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.game.stateManager.changeState("menu")

    def update(self):
        pass

    def draw(self, delta_time, screen):
        self.game.screen.fill(BLUE)

        self.quizLabel.draw(screen)
        self.informaticaLabel.draw(screen)

        pygame.draw.rect(screen, DARK_BLUE, self.startBox, 0, 30)

        self.startLabel.draw(screen)

        pygame.draw.rect(screen, DARK_BLUE, self.fireBox, 0, 50)

        self.fireImage.draw(screen)
