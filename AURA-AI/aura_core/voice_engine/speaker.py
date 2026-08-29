import pyttsx3

class Speaker:
    def __init__(self, rate: int = 175, volume: float = 1.0):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', rate)
        self.engine.setProperty('volume', volume)
        
        # Available voices check
        voices = self.engine.getProperty('voices')
        if voices:
            for voice in voices:
                if "zira" in voice.name.lower() or "female" in voice.name.lower():
                    self.engine.setProperty('voice', voice.id)
                    break

    def speak(self, text: str):
        if not text:
            return
        print(f"\n[AURA]: {text}")
        self.engine.say(text)
        self.engine.runAndWait()