import random

class question_pool():
    def __init__(self, question_methods, name):
        self.name = name

        if callable(question_methods):
            self.question_methods = [question_methods]
            return
        self.question_methods = question_methods

    def get_question(self):
        function_to_question = list(self.question_methods)[random.randint(0, len(self.question_methods)-1)]
        
        question, answer = function_to_question()

        return [question, answer]