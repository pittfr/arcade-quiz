import pygame
from config import *
from states import *
del GameState

class Game:
    def __init__(self):
        self.windowRes = (WINDOW_WIDTH, WINDOW_HEIGHT)
        self.screen = pygame.display.set_mode(self.windowRes)
        pygame.display.set_caption("QUIZ INFORMÁTICA")

        self.clock = pygame.time.Clock()
        self.running = True

        self.stateManager = StateManager(self)

        self.stateManager.addState("starting", StartingState(self))
        self.stateManager.addState("quiz", QuizState(self))
        self.stateManager.addState("gameover", GameoverState(self))

        self.stateManager.changeState("starting")

        self.score = 0

    def handleEvents(self, dt):
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
        
        self.stateManager.handleEvents(events, dt)

    def update(self, dt):
        self.stateManager.update(dt)

    def draw(self, dt):
        
        self.stateManager.draw(dt, self.screen)

        pygame.display.flip()
        pygame.time.Clock().tick(FRAMERATE)

    def run(self):
        clock = pygame.time.Clock()

        while self.running:

            dt = clock.tick(FRAMERATE) / 1000.0  
            
            self.handleEvents(dt)
            
            self.update(dt)
            
            self.draw(dt)
            
            pygame.display.flip()
