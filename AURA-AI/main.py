import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from aura_core.voice_engine.speaker import Speaker
from aura_core.voice_engine.listener import Listener
from aura_core.brain.router import IntentRouter

def main():
    speaker = Speaker()
    listener = Listener()
    router = IntentRouter()
    
    speaker.speak("AURA Phase 5 with Dual Memory Architecture is online.")
    
    while True:
        user_input = listener.listen()
        
        if not user_input:
            continue
            
        if "exit" in user_input or "quit" in user_input or "stop" in user_input:
            speaker.speak("Goodbye! Have a great day.")
            break
            
        # Route the command or send to LLM
        response = router.route(user_input)
        
        if response:
            speaker.speak(response)

if __name__ == "__main__":
    main()