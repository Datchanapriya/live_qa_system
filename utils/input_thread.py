import threading

class InputThread(threading.Thread):
    def __init__(self, question_store):
        super().__init__(daemon=True)
        self.question_store = question_store

    def run(self):
        while True:
            q = input("\nType your question: ")
            self.question_store.set_question(q)
            print("Question updated. Press 'a' to ask.")
