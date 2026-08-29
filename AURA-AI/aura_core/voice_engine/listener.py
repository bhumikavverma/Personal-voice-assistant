import speech_recognition as sr

class Listener:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8  # Sentence break detection

    def listen(self) -> str:
        with sr.Microphone() as source:
            print("\n[Listening... Speak now]")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.6)
            try:
                audio = self.recognizer.listen(source, timeout=6, phrase_time_limit=10)
                print("[Recognizing...]")
                query = self.recognizer.recognize_google(audio, language="en-IN")
                print(f"[User]: {query}")
                return query.strip().lower()
            except sr.WaitTimeoutError:
                return ""
            except sr.UnknownValueError:
                return ""
            except sr.RequestError:
                print("[Error]: Network connectivity error with Google STT.")
                return ""