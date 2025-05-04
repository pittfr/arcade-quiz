import pygame
from states import GameState
from config import *
from ui import *

class MenuState(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.default_font = pygame.font.Font(DEFAULT_FONT_PATH, 64)
        self.stateLabel = Label(pos=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2), font=self.default_font, visible=True, text="Menu state")

    def handle_events(self, events, delta_time):
        pass

    def update(self, delta_time):
        pass

    def draw(self, delta_time, screen):
        self.game.screen.fill(BLUE)
        self.stateLabel.draw(screen)