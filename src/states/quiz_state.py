import pygame
from states import GameState
from config import *
from ui import *

class QuizState(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.default_font = pygame.font.Font(DEFAULT_FONT_PATH, 64)

        self.scoreLabel = Label(
                            pos=(WINDOW_WIDTH // 2, 5),
                            text=" 0/20",
                            font=self.default_font,
                            text_color=WHITE,
                            anchor="midtop"
                            )
        
        self.imagePlaceHolderBox = pygame.Rect(0, 0, WINDOW_WIDTH // 2.5, WINDOW_HEIGHT // 2.5)
        self.imagePlaceHolderBox.midtop = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4)

        self.questionLabel = Label(
                                pos=(WINDOW_WIDTH // 2, 75),
                                text="is this a question??",
                                font=self.default_font,
                                anchor="midtop"
                                )

        # buttons

        b_border_radius = 10
        b_font = pygame.font.Font(DEFAULT_FONT_PATH, 30)
        b_dimensions = (WINDOW_WIDTH // 2.3, WINDOW_HEIGHT // 8)
        b_anchor = "midtop"

        self.option1Button = Button(
                                pos=(int(WINDOW_WIDTH * 0.275), int(WINDOW_HEIGHT * 0.70)),
                                text="option1",
                                border_radius=b_border_radius,
                                font=b_font,
                                bg_color=B_RED,
                                width=b_dimensions[0],
                                height=b_dimensions[1],
                                anchor=b_anchor,
                                key=button1Key
                                )
        
        self.option2Button = Button(
                                pos=(int(WINDOW_WIDTH * 0.725), int(WINDOW_HEIGHT * 0.70)),
                                text="option2",
                                border_radius=b_border_radius,
                                font=b_font,
                                bg_color=B_BLUE,
                                width=b_dimensions[0],
                                height=b_dimensions[1],
                                anchor=b_anchor,
                                key=button2Key
                                )
        
        self.option3Button = Button(
                                pos=(int(WINDOW_WIDTH * 0.275), int(WINDOW_HEIGHT * 0.85)),
                                text="option3",
                                border_radius=b_border_radius,
                                font=b_font,
                                bg_color=B_GREEN,
                                width=b_dimensions[0],
                                height=b_dimensions[1],
                                anchor=b_anchor,
                                key=button3Key
                                )
        self.option4Button = Button(
                                pos=(int(WINDOW_WIDTH * 0.725), int(WINDOW_HEIGHT * 0.85)),
                                text="option4",
                                border_radius=b_border_radius,
                                font=b_font,
                                bg_color=B_YELLOW,
                                width=b_dimensions[0],
                                height=b_dimensions[1],
                                anchor=b_anchor,
                                key=button4Key
                                )

        
    def handle_events(self, events):
        self.option1Button.update(events)
        self.option2Button.update(events)
        self.option3Button.update(events)
        self.option4Button.update(events)

    def update(self):
        pass

    def draw(self, delta_time, screen):
        self.game.screen.fill(BLUE)
        self.scoreLabel.draw(screen)

        self.questionLabel.draw(screen)

        pygame.draw.rect(screen, DARK_BLUE, self.imagePlaceHolderBox, 0, 10)

        self.option1Button.draw(screen)
        self.option2Button.draw(screen)
        self.option3Button.draw(screen)
        self.option4Button.draw(screen)