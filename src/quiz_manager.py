import random
import os
import pygame
from config import IMAGES_PATH
from utils.file_utils import load_json_file
from utils.image_utils import load_image, preload_images_by_theme, get_random_image_for_theme
from utils.quiz_utils import select_random_questions, get_fallback_question

class QuizManager:
    def __init__(self, questions_file_path):
        self.questions = []
        self.all_questions = []  # store all available questions
        self.current_index = 0
        self.score = 0
        self.total_questions = 10
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
        placeholder_path = os.path.join(IMAGES_PATH, "placeholder.png")
        self.image_cache, self.theme_image_dict = preload_images_by_theme(
            self.theme_images, 
            IMAGES_PATH, 
            placeholder_path
        )
        print(f"preloaded {len(self.image_cache)} images into {len(self.theme_image_dict)} themes")
    
    def _get_random_image_for_theme(self, theme):
        """get a random image for the given theme"""
        return get_random_image_for_theme(self.theme_image_dict, theme)
    
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
        data = load_json_file(file_path)
        if data:
            self.all_questions = data.get('questions', [])
            self._selectRandomQuestions()
        else:
            # Use fallback question
            self.all_questions = [get_fallback_question()]
            self._selectRandomQuestions()

    def _selectRandomQuestions(self):
        """select a random set of questions from all available questions"""
        self.questions = select_random_questions(self.all_questions, self.total_questions)
        self.current_index = 0
        self.score = 0
    
    def getCurrentQuestion(self):
        if not self.questions or self.current_index >= len(self.questions):
            return None

        question = self.questions[self.current_index]
        
        if 'image' not in question and 'theme' in question:
            theme = question['theme']

            image = self._get_random_image_for_theme(theme)
            question['image'] = image
        
        return question
    
    def checkAnswer(self, selected_index):
        if not self.questions or self.current_index >= len(self.questions):
            return False
        
        correct_index = self.questions[self.current_index]['answer_index']
        return selected_index == correct_index
    
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