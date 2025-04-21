import pygame
from states import GameState
from config import *
from ui import *

class StartingState(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.default_font = pygame.font.Font(DEFAULT_FONT_PATH, 64)
        self.stateLabel = Label(pos=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2), font=self.default_font, visible=True, text="Starting state")

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.game.stateManager.changeState("menu")

    def update(self):
        pass

    def draw(self, delta_time, screen):
        self.game.screen.fill((214, 229, 190))
        self.stateLabel.draw(screen)