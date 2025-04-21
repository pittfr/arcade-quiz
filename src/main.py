import pygame
from game import Game
from config import *

def main():
    try:
        pygame.init()
    except pygame.error as e:
        print(f"failed to initialize pygame: {e}")
        exit(1)
    
    game = Game()

    game.run()

    pygame.quit()

if __name__ == "__main__":
    main()