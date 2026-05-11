class ReasoningEngine:
    def __init__(self, yolo_detector, blip_vqa):
        self.yolo = yolo_detector
        self.blip = blip_vqa

    def answer(self, frame, question):
        question_lower = question.lower()

        # ---------------- YOLO QUESTIONS (COUNTING) ----------------
        if any(k in question_lower for k in
               ["how many", "count", "number of", "people", "objects"]):

            objects = self.yolo.detect_objects(frame)

            if not objects:
                return "I do not see any recognizable objects."

            response = []
            for obj, count in objects.items():
                response.append(f"{count} {obj}(s)")

            return "I see " + ", ".join(response)

        # ---------------- BLIP QUESTIONS (DESCRIPTION) ----------------
        else:
            if any(k in question_lower for k in
                   ["describe", "doing", "happening", "scene"]):

                objects = self.yolo.detect_objects(frame)
                blip_answer = self.blip.answer_question(frame, question)

                if objects:
                    obj_summary = ", ".join(
                        [f"{count} {obj}" for obj, count in objects.items()]
                    )
                    return f"I see {obj_summary}. The scene shows {blip_answer}."
                else:
                    return blip_answer

            else:
                return "This question does not require visual description."
