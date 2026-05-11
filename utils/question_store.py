import threading

class QuestionStore:
    def __init__(self):
        self.question = ""
        self.lock = threading.Lock()

    def set_question(self, q):
        with self.lock:
            self.question = q

    def get_question(self):
        with self.lock:
            return self.question
