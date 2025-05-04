import pygame
from config import *
from states import *
del GameState

class Game:
    def __init__(self):
        self.windowRes = (WINDOW_WIDTH, WINDOW_HEIGHT)
        self.screen = pygame.display.set_mode(self.windowRes)
        pygame.display.set_caption("CSMIGUEL Sabe+")

        self.clock = pygame.time.Clock()
        self.running = True

        self.stateManager = StateManager(self)

        self.stateManager.addState("starting", StartingState(self))
        self.stateManager.addState("menu", MenuState(self))
        self.stateManager.addState("quiz", QuizState(self))
        self.stateManager.addState("gameover", GameoverState(self))

        self.stateManager.changeState("starting")

        self.score = 0

    def handleEvents(self):
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
        
        self.stateManager.handleEvents(events)

    def update(self):
        self.stateManager.update()

    def draw(self, delta_time):
        
        self.stateManager.draw(delta_time, self.screen)

        pygame.display.flip()
        pygame.time.Clock().tick(FRAMERATE)

    def run(self):
        while self.running:
            delta_time = self.clock.tick(FRAMERATE) / 1000.0

            self.handleEvents()

            self.update()
            self.draw(delta_time)
