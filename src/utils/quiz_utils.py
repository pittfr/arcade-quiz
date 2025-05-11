import random

def select_random_questions(all_questions, count=20, shuffle_options=True):
    if not all_questions:
        return []
        
    # use sample if we have enough questions, otherwise use all questions
    if len(all_questions) > count:
        selected = random.sample(all_questions, count)
    else:
        # shuffle a copy of all_questions
        selected = all_questions.copy()
        random.shuffle(selected)
    
    # normalize all question structures to ensure consistent keys
    normalized = []
    for q in selected:
        normalized_q = normalize_question_format(q)
        if shuffle_options:
            normalized_q = shuffle_question_options(normalized_q)
        normalized.append(normalized_q)
        
    return normalized

def normalize_question_format(question):
    # create a new dictionary with required keys
    normalized = {}
    
    if 'text' in question:
        normalized['text'] = question['text']
    elif 'question' in question:
        normalized['text'] = question['question']
    else:
        normalized['text'] = "Question text missing"
    
    if 'options' in question:
        normalized['options'] = question['options'].copy()
    else:
        normalized['options'] = ["Missing option A", "Missing option B", 
                                "Missing option C", "Missing option D"]
    
    if 'answer_index' in question:
        normalized['answer_index'] = question['answer_index']
    elif 'answer' in question and question['answer'].isdigit():
        normalized['answer_index'] = int(question['answer'])
    else:
        normalized['answer_index'] = 0
    
    if 'theme' in question:
        normalized['theme'] = question['theme']
    else:
        normalized['theme'] = 'default'
    return normalized

def shuffle_question_options(question):
    question = question.copy()
    
    correct_answer = question['options'][question['answer_index']]
    
    pairs = list(enumerate(question['options']))
    
    random.shuffle(pairs)
    
    question['options'] = [option for _, option in pairs]
    
    for i, option in enumerate(question['options']):
        if option == correct_answer:
            question['answer_index'] = i
            break
            
    return question

def get_fallback_question():
    return {
        'text': 'Failed to load questions. The answer is A',
        'options': ['A', 'B', 'C', 'D'],
        'answer_index': 0,
        'theme': 'default'
    }