import cv2

from video.camera import Camera
from models.yolo_detector import YOLODetector
from models.blip_vqa import BLIPVQA
from reasoning.engine import ReasoningEngine
from utils.ai_worker import AIWorker
from utils.question_store import QuestionStore
from utils.input_thread import InputThread
from utils.voice_input import VoiceInputThread


def draw_multiline_text(frame, text, x, y, line_height=25):
    words = text.split()
    line = ""
    y_offset = 0

    for word in words:
        test_line = line + word + " "
        if len(test_line) > 35:
            cv2.putText(
                frame,
                line,
                (x, y + y_offset),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )
            y_offset += line_height
            line = word + " "
        else:
            line = test_line

    if line:
        cv2.putText(
            frame,
            line,
            (x, y + y_offset),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )


def main():
    # ---------------- CAMERA ----------------
    camera = Camera()

    # ---------------- MODELS ----------------
    yolo = YOLODetector()
    blip = BLIPVQA()
    engine = ReasoningEngine(yolo, blip)

    # ---------------- AI WORKER ----------------
    ai_worker = AIWorker(engine)
    ai_worker.start()

    # ---------------- QUESTION INPUT ----------------
    question_store = QuestionStore()
    input_thread = InputThread(question_store)
    input_thread.start()
    voice_thread = VoiceInputThread(question_store)
    voice_thread.start()

    print("🎤 Voice input enabled (speak anytime)")
    print("\nINSTRUCTIONS:")
    print("• Type your question in the terminal and press ENTER")
    print("• Click on the camera window")
    print("• Press 'a' to ask the AI")
    print("• Press 'q' to quit\n")

    while True:
        ret, frame = camera.read()
        if not ret:
            break

        # Show answer if available
        if ai_worker.result:
            draw_multiline_text(
                frame,
                f"Answer: {ai_worker.result}",
                20,
                40
            )

        cv2.imshow("Live VQA System", frame)

        key = cv2.waitKey(1) & 0xFF

        # Ask AI
        if key == ord('a'):
            question = question_store.get_question()
            if question:
                ai_worker.ask(frame, question)
                ai_worker.result = None
            else:
                print("⚠ No question typed yet.")

        # Quit
        if key == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
