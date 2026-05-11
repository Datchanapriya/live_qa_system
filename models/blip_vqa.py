import torch
import cv2

from transformers import BlipProcessor, BlipForQuestionAnswering
from PIL import Image

class BLIPVQA:
    def __init__(self, device=None):
        """
        device: 'cuda' if GPU available else 'cpu'
        """
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")

        self.processor = BlipProcessor.from_pretrained(
            "Salesforce/blip-vqa-base"
        )
        self.model = BlipForQuestionAnswering.from_pretrained(
            "Salesforce/blip-vqa-base"
        ).to(self.device)

    def answer_question(self, frame, question):
        """
        frame: OpenCV image (BGR)
        question: string
        returns: answer string
        """

        # Resize frame to speed up BLIP
        small_frame = cv2.resize(frame, (320, 240))
        image = Image.fromarray(small_frame[:, :, ::-1])

        inputs = self.processor(
            image,
            question,
            return_tensors="pt"
        ).to(self.device)

        output = self.model.generate(**inputs)
        answer = self.processor.decode(
            output[0],
            skip_special_tokens=True
        )

        return answer
