import threading
import speech_recognition as sr

class VoiceInputThread(threading.Thread):
    def __init__(self, question_store):
        super().__init__(daemon=True)
        self.question_store = question_store
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

    def run(self):
        with self.microphone as source:
            print("🎤 Adjusting for ambient noise...")
            self.recognizer.adjust_for_ambient_noise(source)

        while True:
            print("\n🎤 Speak your question...")
            with self.microphone as source:
                audio = self.recognizer.listen(source)

            try:
                text = self.recognizer.recognize_google(audio)
                print("🗣 You said:", text)
                self.question_store.set_question(text)
                print("✔ Voice question stored. Press 'a' to ask.")
            except sr.UnknownValueError:
                print("❌ Could not understand audio")
            except sr.RequestError as e:
                print("❌ Speech service error:", e)
