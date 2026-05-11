import threading
import queue


class AIWorker(threading.Thread):
    def __init__(self, engine):
        super().__init__(daemon=True)
        self.engine = engine
        self.task_queue = queue.Queue()
        self.result = None
        self.last_question = None

    def run(self):
        while True:
            frame, question = self.task_queue.get()
            self.result = self.engine.answer(frame, question)
            self.task_queue.task_done()

    def ask(self, frame, question):
        if question != self.last_question and self.task_queue.empty():
            self.last_question = question
            self.task_queue.put((frame.copy(), question))
