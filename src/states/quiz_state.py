import pygame
from states import GameState
from config import *
from ui import *
from quiz_manager import QuizManager

class QuizState(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.progress_font = pygame.font.Font(DEFAULT_FONT_PATH, 60)
        self.default_font = pygame.font.Font(DEFAULT_FONT_PATH, 75)
        
        # create quiz manager
        self.quiz_manager = QuizManager(QUESTIONS_PATH)
        
        # timer for showing feedback
        self.feedback_timer = 0
        self.showing_feedback = False
        
        # store original button colors for resetting
        self.original_button_colors = {
            'option1': B_RED,
            'option2': B_BLUE,
            'option3': B_YELLOW,
            'option4': B_GREEN  
        }
        
        # feedback colors
        self.correct_color = (50, 200, 50)    # green for correct answers
        self.incorrect_color = (200, 50, 50)  # red for incorrect answers
        
        # UI Elements
        self.progressLabel = Label(
                            pos=(WINDOW_WIDTH // 2, 20),
                            text=f" 0/{self.quiz_manager.total_questions}",
                            font=self.progress_font,
                            text_color=WHITE,
                            anchor="midtop"
                            )
        
        self.imagePlaceHolderBox = pygame.Rect(0, 0, WINDOW_WIDTH // 2.5, WINDOW_HEIGHT // 2.5)
        self.imagePlaceHolderBox.midtop = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4)

        self.questionImage = None
        
        self.questionLabel = Label(
                                pos=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 8),
                                text="",
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
                                text="",
                                border_radius=b_border_radius,
                                font=b_font,
                                bg_color=B_RED,
                                width=b_dimensions[0],
                                height=b_dimensions[1],
                                anchor=b_anchor,
                                key=button1Key,
                                action=lambda: self._check_answer(0)
                                )
        
        self.option2Button = Button(
                                pos=(int(WINDOW_WIDTH * 0.725), int(WINDOW_HEIGHT * 0.70)),
                                text="",
                                border_radius=b_border_radius,
                                font=b_font,
                                bg_color=B_BLUE,
                                width=b_dimensions[0],
                                height=b_dimensions[1],
                                anchor=b_anchor,
                                key=button2Key,
                                action=lambda: self._check_answer(1)
                                )
        
        self.option3Button = Button(
                                pos=(int(WINDOW_WIDTH * 0.275), int(WINDOW_HEIGHT * 0.85)),
                                text="",
                                border_radius=b_border_radius,
                                font=b_font,
                                bg_color=B_GREEN,
                                width=b_dimensions[0],
                                height=b_dimensions[1],
                                anchor=b_anchor,
                                key=button3Key,
                                action=lambda: self._check_answer(2)
                                )
        
        self.option4Button = Button(
                                pos=(int(WINDOW_WIDTH * 0.725), int(WINDOW_HEIGHT * 0.85)),
                                text="",
                                border_radius=b_border_radius,
                                font=b_font,
                                bg_color=B_YELLOW,
                                width=b_dimensions[0],
                                height=b_dimensions[1],
                                anchor=b_anchor,
                                key=button4Key,
                                action=lambda: self._check_answer(3)
                                )
        
        # store buttons in a list for easier access
        self.option_buttons = [
            self.option1Button, 
            self.option2Button, 
            self.option3Button, 
            self.option4Button
        ]

    def _load_current_question(self):
        question = self.quiz_manager.getCurrentQuestion()
        
        if not question:
            # no more questions, go to game over
            self.game.stateManager.changeState("gameover")
            return
        
        # update UI with question data
        self.questionLabel.setText(question['text'])
        
        # update options
        self.option1Button.setText(question['options'][0])
        self.option2Button.setText(question['options'][1])
        self.option3Button.setText(question['options'][2])
        self.option4Button.setText(question['options'][3])
        
        # reset button colors
        self._reset_button_colors()
        
        # load question image if available
        if question['image_path']:
            try:
                self.questionImage = pygame.image.load(question['image_path']).convert_alpha()
                # scale to fit placeholder
                self.questionImage = pygame.transform.scale(
                    self.questionImage, 
                    (self.imagePlaceHolderBox.width - 20, self.imagePlaceHolderBox.height - 20)
                )
            except:
                self.questionImage = None
        else:
            self.questionImage = None
        
        # update progress display
        self.progressLabel.setText(f" {self.quiz_manager.current_index + 1}/{self.quiz_manager.total_questions}")
        
        # reset feedback
        self.showing_feedback = False
                
    def _check_answer(self, selected_index):
        if self.showing_feedback:
            return
        
        correct = self.quiz_manager.checkAnswer(selected_index)

        if correct:
            self.game.score += 1

        correct_answer_index = self.quiz_manager.getCurrentQuestion()['answer_index']

        # set button colors based on correctness
        for i, button in enumerate(self.option_buttons):
            if i == correct_answer_index:
                # highlight the correct answer in green
                button.setBgColor(self.correct_color)
            elif i != correct_answer_index:
                # if this is the selected answer and it's wrong, make it red
                button.setBgColor(self.incorrect_color)
        

        # update progress display
        self.progressLabel.setText(f" {self.quiz_manager.current_index + 1}/{self.quiz_manager.total_questions}")
        
        # start feedback timer
        self.feedback_timer = 2.0  # show feedback for 2 seconds
        self.showing_feedback = True
    
    def _reset_button_colors(self):
        """reset all button colors to their original values"""
        self.option1Button.setBgColor(self.original_button_colors['option1'])
        self.option2Button.setBgColor(self.original_button_colors['option2'])
        self.option3Button.setBgColor(self.original_button_colors['option3'])
        self.option4Button.setBgColor(self.original_button_colors['option4'])
        
    def _next_question(self):
        # reset all button key states
        for button in self.option_buttons:
            button.resetKeyState()

        if self.quiz_manager.nextQuestion():
            self._load_current_question()
        else:
            # end of quiz
            self.game.stateManager.changeState("gameover")
        
    def handle_events(self, events, delta_time):
        # process button clicks only if not showing feedback
        for button in self.option_buttons:
            button.update(events, delta_time, self.showing_feedback)
        
    def update(self, delta_time):
        # update feedback timer
        if self.showing_feedback and self.feedback_timer > 0:
            self.feedback_timer -= 1/FRAMERATE
            if self.feedback_timer <= 0:
                self._next_question()

    def draw(self, delta_time, screen):
        self.game.screen.fill(BLUE)
        
        # draw progress
        self.progressLabel.draw(screen)
        
        # draw question
        self.questionLabel.draw(screen)

        # draw image placeholder box
        pygame.draw.rect(screen, DARK_BLUE, self.imagePlaceHolderBox, 0, 10)
        
        # draw question image if available
        if self.questionImage:
            image_rect = self.questionImage.get_rect(center=self.imagePlaceHolderBox.center)
            screen.blit(self.questionImage, image_rect)
        
        # draw option buttons
        for button in self.option_buttons:
            button.draw(screen)
            
        # add feedback text
        if self.showing_feedback:
            pass
                
    def enter(self):
        # reset quiz when entering this state
        self.quiz_manager.reset()
        self._load_current_question()
        self.showing_feedback = False
        # reset the game score when starting a new quiz
        self.game.score = 0