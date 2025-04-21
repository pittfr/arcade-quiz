import pygame

class GameState:
    def __init__(self, game):
        self.game = game
    
    def handle_events(self, events):
        pass
        
    def update(self):
        pass
        
    def draw(self, delta_time, screen):
        pass
        
    def enter(self):
        """called when this state becomes the active state"""
        pass
        
    def exit(self):
        """called when this state is no longer the active state"""
        pass