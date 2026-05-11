import cv2
from datetime import datetime

class VideoRecorder:
    def __init__(self, frame_width, frame_height, fps=20):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"recording_{timestamp}.mp4"

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.writer = cv2.VideoWriter(
            filename,
            fourcc,
            fps,
            (frame_width, frame_height)
        )

    def write(self, frame):
        self.writer.write(frame)

    def release(self):
        self.writer.release()
