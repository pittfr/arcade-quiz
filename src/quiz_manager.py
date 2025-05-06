import json
import random

class QuizManager:
    def __init__(self, questions_file_path):
        self.questions = []
        self.current_index = 0
        self.score = 0
        self.total_questions = 20
        self.loadQuestions(questions_file_path)
        
    def loadQuestions(self, file_path):
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                all_questions = data.get('questions', [])
                
                # shuffle questions and take only the required number
                random.shuffle(all_questions)
                selected_questions = all_questions[:self.total_questions]
                
                # process each question
                for q in selected_questions:
                    # convert answer from string to integer
                    original_answer_index = int(q.get('answer', 0))
                    
                    # get the options and the correct answer
                    options = q.get('options', ['', '', '', ''])
                    correct_answer = options[original_answer_index]
                    
                    # create pairs of (option, is_correct)
                    option_pairs = [(option, i == original_answer_index) for i, option in enumerate(options)]
                    
                    # shuffle the pairs
                    random.shuffle(option_pairs)
                    
                    # extract the shuffled options and find the new index of the correct answer
                    shuffled_options = [pair[0] for pair in option_pairs]
                    new_answer_index = [i for i, pair in enumerate(option_pairs) if pair[1]][0]
                    
                    self.questions.append({
                        'text': q.get('question', ''),
                        'options': shuffled_options,
                        'answer_index': new_answer_index,
                        'image_path': q.get('image_path', None)
                    })
                
                # update total questions in case we have fewer than requested
                self.total_questions = len(self.questions)
                
        except Exception as e:
            print(f"error loading questions: {e}")
            # provide at least one default question if loading fails
            self.questions = [{
                'text': 'failed to load questions. the answer is A',
                'options': ['A', 'B', 'C', 'D'],
                'answer_index': 0,
                'image_path': None
            }]
            self.total_questions = len(self.questions)
    
    def getCurrentQuestion(self):
        if 0 <= self.current_index < len(self.questions):
            return self.questions[self.current_index]
        return None
    
    def checkAnswer(self, selected_index):
        if 0 <= self.current_index < len(self.questions):
            correct = selected_index == self.questions[self.current_index]['answer_index']
            if correct:
                self.score += 1
            return correct
        return False
    
    def nextQuestion(self):
        self.current_index += 1
        if self.current_index >= len(self.questions):
            return False  # no more questions
        return True  # more questions available
        
    def reset(self):
        self.current_index = 0
        self.score = 0
        random.shuffle(self.questions)