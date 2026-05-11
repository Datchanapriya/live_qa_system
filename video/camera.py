import cv2

class Camera:
    def __init__(self, cam_id=0, width=640, height=480):
        """
        cam_id = 0 means default webcam
        width, height = resolution
        """
        self.cap = cv2.VideoCapture(cam_id)

        # Set resolution
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        if not self.cap.isOpened():
            raise RuntimeError("Cannot open camera")

    def read(self):
        """
        Returns:
        ret   -> True if frame is read correctly
        frame -> image (numpy array)
        """
        return self.cap.read()

    def release(self):
        """Release the camera resource"""
        self.cap.release()
