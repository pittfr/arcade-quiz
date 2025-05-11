import json
import random
import os
import pygame
from config import IMAGES_PATH

class QuizManager:
    def __init__(self, questions_file_path):
        self.questions = []
        self.all_questions = []  # store all available questions
        self.current_index = 0
        self.score = 0
        self.total_questions = 20
        self.questions_file_path = questions_file_path  # store the path for later reloading
        
        # map of theme folders and their available image counts
        self.theme_images = self._load_theme_images()
        
        # image cache
        self.image_cache = {}
        
        # theme image dictionary
        self.theme_image_dict = {}
        
        # preload all images and organize them by theme
        self._preload_all_images()
        
        # load questions
        self.loadQuestions(questions_file_path)
    
    def _load_theme_images(self):
        """load available images for each theme folder"""
        theme_images = {}
        
        try:
            # check if the images directory exists
            if not os.path.exists(IMAGES_PATH):
                print(f"warning: images path {IMAGES_PATH} does not exist")
                return theme_images
                
            # get all theme folders in the images directory
            theme_folders = [f for f in os.listdir(IMAGES_PATH) 
                             if os.path.isdir(os.path.join(IMAGES_PATH, f))]
            
            # count the numbered images
            for theme_folder in theme_folders:
                folder_path = os.path.join(IMAGES_PATH, theme_folder)
                
                # find the highest numbered image in the format
                image_count = 0
                for i in range(1, 21):  # assume maximum of 20 images per theme
                    if os.path.exists(os.path.join(folder_path, f"{i}.jpg")):
                        image_count = i
                    else:
                        break
                
                # store the count of images for this theme
                if image_count > 0:
                    theme_images[theme_folder] = image_count
                    print(f"found {image_count} images for theme '{theme_folder}'")
        
        except Exception as e:
            print(f"error loading theme images: {e}")
        
        return theme_images
    
    def _preload_all_images(self):
        """preload all possible theme images into memory"""
        
        # load the placeholder image
        placeholder_path = os.path.join(IMAGES_PATH, "placeholder.png")
        try:
            self.image_cache[placeholder_path] = pygame.image.load(placeholder_path).convert_alpha()
        except Exception as e:
            print(f"error loading placeholder image: {e}")
            # create a blank surface as placeholder if loading fails
            self.image_cache[placeholder_path] = pygame.Surface((300, 200))
            self.image_cache[placeholder_path].fill((255, 0, 255))
        
        # create the theme dictionary with placeholder
        self.theme_image_dict["default"] = [self.image_cache[placeholder_path]]
        
        # load all images from each theme folder
        for theme, count in self.theme_images.items():
            self.theme_image_dict[theme] = []
            for i in range(1, count + 1):
                img_path = os.path.join(IMAGES_PATH, theme, f"{i}.jpg")
                try:
                    img = pygame.image.load(img_path)
                    if img.get_alpha():
                        img = img.convert_alpha()
                    else:
                        img = img.convert()
                    self.image_cache[img_path] = img
                    self.theme_image_dict[theme].append(img)
                except Exception as e:
                    print(f"error loading image {img_path}: {e}")
                    # use placeholder for failed loads
                    self.image_cache[img_path] = self.image_cache[placeholder_path]
                    self.theme_image_dict[theme].append(self.image_cache[placeholder_path])
        
        print(f"preloaded {len(self.image_cache)} images into {len(self.theme_image_dict)} themes")
    
    def _get_random_image_for_theme(self, theme):
        """get a random image for the given theme"""
        # check if theme exists in the theme image dictionary
        if theme in self.theme_image_dict and len(self.theme_image_dict[theme]) > 0:
            # select a random image from this theme
            return random.choice(self.theme_image_dict[theme])
        
        # if theme doesn't exist or has no images return placeholder
        return self.theme_image_dict["default"][0]
    
    def get_cached_image(self, image_or_path):
        """get an image from the cache or return the image if it's already a surface"""
        # if already a pygame Surface, just return it
        if isinstance(image_or_path, pygame.Surface):
            return image_or_path
            
        if image_or_path in self.image_cache:
            return self.image_cache[image_or_path]
        
        # if image somehow isnt in cache load it now
        placeholder_path = os.path.join(IMAGES_PATH, "placeholder.png")
        try:
            img = pygame.image.load(image_or_path)
            self.image_cache[image_or_path] = img
            return img
        except Exception:
            return self.image_cache[placeholder_path]
        
    def loadQuestions(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                self.all_questions = data.get('questions', [])
                
                # select random questions for this session
                self._selectRandomQuestions()
                
        except Exception as e:
            print(f"error loading questions: {e}")
            # provide at least one default question if loading fails
            self.all_questions = [{
                'question': 'Failed to load questions. The answer is A',
                'options': ['A', 'B', 'C', 'D'],
                'answer': '0',
                'theme': 'default'
            }]
            self._selectRandomQuestions()

    def _selectRandomQuestions(self):
        """select a random set of questions from all available questions"""
        if len(self.all_questions) > self.total_questions:
            selected_questions = random.sample(self.all_questions, self.total_questions)
        else:
            selected_questions = self.all_questions.copy()
            random.shuffle(selected_questions)
        
        # process each question
        self.questions = []
        for q in selected_questions:
            # convert answer from string to integer
            original_answer_index = int(q.get('answer', 0))
            
            # get the options and the correct answer
            options = q.get('options', ['', '', '', ''])
            correct_answer = options[original_answer_index]
            
            option_pairs = [(option, i == original_answer_index) for i, option in enumerate(options)]
            
            # shuffle the pairs
            random.shuffle(option_pairs)
            
            # extract the shuffled options and find the new index of the correct answer
            shuffled_options = [pair[0] for pair in option_pairs]
            new_answer_index = [i for i, pair in enumerate(option_pairs) if pair[1]][0]
            
            # get a random image based on the question's theme
            theme = q.get('theme', 'default')
            image = self._get_random_image_for_theme(theme)
            
            self.questions.append({
                'text': q.get('question', ''),
                'options': shuffled_options,
                'answer_index': new_answer_index,
                'image': image,
                'theme': theme
            })
        
        # update total questions in case we have fewer than requested
        self.total_questions = len(self.questions)
    
    def getCurrentQuestion(self):
        if 0 <= self.current_index < len(self.questions):
            return self.questions[self.current_index]
        return None
    
    def checkAnswer(self, selected_index):
        if 0 <= self.current_index < len(self.questions):
            correct = selected_index == self.questions[self.current_index]['answer_index']
            return correct
        return False
    
    def nextQuestion(self):
        self.current_index += 1
        if self.current_index >= len(self.questions):
            return False  # no more questions
        return True  # more questions available
        
    def reset(self):
        """Reset the quiz with new random questions"""
        self.current_index = 0
        self.score = 0
        
        # select a new set of random questions
        self._selectRandomQuestions()