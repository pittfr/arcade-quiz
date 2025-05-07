import pygame
from states import GameState
from config import *
from ui import *
from utils.animation import Animation
from quiz_manager import QuizManager


class QuizState(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.progress_font = pygame.font.Font(DEFAULT_FONT_PATH, 60)
        self.default_font = pygame.font.Font(DEFAULT_FONT_PATH, 70)
        
        self.isQuizOver = False

        self.foregroundOpacity = 0

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
                            pos=(WINDOW_WIDTH // 2, -100),
                            text=f" 0/{self.quiz_manager.total_questions}",
                            font=self.progress_font,
                            text_color=WHITE,
                            anchor="midtop"
                            )
        
        # image dimensions
        image_width = WINDOW_WIDTH // 3
        image_height = WINDOW_HEIGHT // 3
        
        # create question image object
        self.questionImage = Image(
            pos=(int(WINDOW_WIDTH * 0.5), int(WINDOW_HEIGHT * 0.5) + int(WINDOW_HEIGHT * 0.02)),
            image_path=(IMAGES_PATH + "placeholder.png"),  # default image path
            fixed_width=image_width,
            fixed_height=image_height,
            preserve_aspect_ratio=True,
            anchor="center",
            border_radius=10
        )
        
        self.questionLabel = Label(
                                pos=(int(WINDOW_WIDTH * 0.5), int(WINDOW_HEIGHT * 0.1)),
                                text="",
                                font=self.default_font,
                                anchor="midtop",
                                max_width=WINDOW_WIDTH - int(WINDOW_WIDTH * 0.1)
                                )

        # buttons
        b_border_radius = 10
        b_font = pygame.font.Font(DEFAULT_FONT_PATH, 30)
        b_dimensions = (WINDOW_WIDTH // 2.3, WINDOW_HEIGHT // 8)
        b_anchor = "midtop"

        self.targetYB1 = (int(WINDOW_WIDTH * 0.275), int(WINDOW_HEIGHT * 0.70))
        self.targetYB2 = (int(WINDOW_WIDTH * 0.725), int(WINDOW_HEIGHT * 0.70))
        self.targetYB3 = (int(WINDOW_WIDTH * 0.275), int(WINDOW_HEIGHT * 0.85))
        self.targetYB4 = (int(WINDOW_WIDTH * 0.725), int(WINDOW_HEIGHT * 0.85))

        self.buttonStartYOffset = 1000

        self.option1Button = Button(
                                pos=((self.targetYB1[0]), (self.targetYB1[1] + self.buttonStartYOffset)),
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
                                pos=((self.targetYB2[0]), (self.targetYB2[1] + self.buttonStartYOffset)),
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
                                pos=((self.targetYB3[0]), (self.targetYB3[1] + self.buttonStartYOffset)),
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
                                pos=((self.targetYB4[0]), (self.targetYB4[1] + self.buttonStartYOffset)),
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

        # create animations

        self.progressLabel_animation = Animation(-200, 20, 3.0, 2.0)

        self.questionLabel_animation = Animation(0, 255, 4.0, 8.5)
        self.questionImage_animation = Animation(0, 255, 4.0, 10.5)

        self.button1_animation = Animation(self.targetYB1[1] + self.buttonStartYOffset, self.targetYB1[1], 4.0, 2.5)
        self.button2_animation = Animation(self.targetYB2[1] + self.buttonStartYOffset, self.targetYB2[1], 4.0, 3.0)
        self.button3_animation = Animation(self.targetYB3[1] + self.buttonStartYOffset, self.targetYB3[1], 4.0, 3.5)
        self.button4_animation = Animation(self.targetYB4[1] + self.buttonStartYOffset, self.targetYB4[1], 4.0, 4.0)

        self.foreground_animation = Animation(0, 255, 4.0)

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
                self.questionImage.setPath(question['image_path'], animate=True)
        else:
            # set to a default placeholder image
            self.questionImage.setPath(IMAGES_PATH + "placeholder.png", animate=True)
        
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
            self.isQuizOver = True
        
    def handle_events(self, events, delta_time):
        # process button clicks
        for button in self.option_buttons:
            button.update(events, delta_time, self.showing_feedback, not self.questionImage_animation.is_complete)
        
    def update(self, delta_time):
        # update the image animation
        self.questionImage.update()
        
        # update feedback timer
        if self.showing_feedback and self.feedback_timer > 0:
            self.feedback_timer -= 1/FRAMERATE
            if self.feedback_timer <= 0:
                self._next_question()

        if self.isQuizOver:
            self.foregroundOpacity = int(self.foreground_animation.update(delta_time))

            if self.foreground_animation.is_complete and self.foregroundOpacity >= 255:
                self.game.stateManager.changeState("gameover")

        else:
            # progress label animation
            progressLabelY = int(self.progressLabel_animation.update(delta_time))
            self.progressLabel.setPosition((WINDOW_WIDTH // 2, progressLabelY))

            # question label animation
            questionLabelOpacity = int(self.questionLabel_animation.update(delta_time))
            self.questionLabel.setOpacity(questionLabelOpacity)
            
            # question image animation
            questionImageOpacity = int(self.questionImage_animation.update(delta_time))
            self.questionImage.setOpacity(questionImageOpacity)

            # button animations
            button1Y = int(self.button1_animation.update(delta_time))
            self.option1Button.setPosition((self.targetYB1[0], button1Y))

            button2Y = int(self.button2_animation.update(delta_time))
            self.option2Button.setPosition((self.targetYB2[0], button2Y))

            button3Y = int(self.button3_animation.update(delta_time))
            self.option3Button.setPosition((self.targetYB3[0], button3Y))

            button4Y = int(self.button4_animation.update(delta_time))
            self.option4Button.setPosition((self.targetYB4[0], button4Y))

    def enter(self):
        # reset quiz when entering this state
        self.quiz_manager.reset()
        self._load_current_question()
        self.showing_feedback = False
        self.isQuizOver = False
        # reset the game score when starting a new quiz
        self.game.score = 0

        # reset all animations when entering the state
        self.progressLabel_animation.reset()
        self.questionLabel_animation.reset()
        self.questionImage_animation.reset()

        self.button1_animation.reset()
        self.button2_animation.reset()
        self.button3_animation.reset()
        self.button4_animation.reset()

        self.foreground_animation.reset()

        # reset UI elements
        self.progressLabel.setPosition((WINDOW_WIDTH // 2, self.progressLabel_animation.start_value))
        self.questionLabel.setOpacity(self.questionLabel_animation.start_value)
        self.questionImage.setOpacity(self.questionImage_animation.start_value)

        self.option1Button.setPosition((self.targetYB1[0], self.targetYB1[1] + self.buttonStartYOffset))
        self.option2Button.setPosition((self.targetYB2[0], self.targetYB2[1] + self.buttonStartYOffset))
        self.option3Button.setPosition((self.targetYB3[0], self.targetYB3[1] + self.buttonStartYOffset))
        self.option4Button.setPosition((self.targetYB4[0], self.targetYB4[1] + self.buttonStartYOffset))

        self.foregroundOpacity = 0

    def draw(self, delta_time, screen):
        self.game.screen.fill(BLUE)
        
        # draw progress
        self.progressLabel.draw(screen)
        
        # draw question
        self.questionLabel.draw(screen)

        # draw the question image
        self.questionImage.draw(screen)
        
        # draw option buttons
        for button in self.option_buttons:
            button.draw(screen)

        if self.foregroundOpacity > 0:
            foreground_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
            foreground_color = (*BLUE[:3], self.foregroundOpacity)
            foreground_surface.fill(foreground_color)
            screen.blit(foreground_surface, (0, 0))
        # pygame.draw.rect(screen, BLUE, self.foregroundRect)