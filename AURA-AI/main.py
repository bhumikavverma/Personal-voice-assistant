from aura_core.voice_engine.speaker import Speaker
from aura_core.voice_engine.listener import Listener

def main():
    speaker = Speaker()
    listener = Listener()
    
    speaker.speak("Hello! I am AURA, your personal assistant. How can I help you?")
    
    while True:
        user_input = listener.listen()
        
        if not user_input:
            continue
            
        if "exit" in user_input or "quit" in user_input or "stop" in user_input:
            speaker.speak("Goodbye! Have a great day.")
            break
            
        # Echo response for testing Phase 1
        speaker.speak(f"You said: {user_input}")

if __name__ == "__main__":
    main()
