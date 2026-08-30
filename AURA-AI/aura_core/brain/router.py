import re
from typing import Optional
from aura_core.actions.system_control import get_time, get_date, open_application, set_volume, take_screenshot
from aura_core.actions.web_tools import open_website, google_search, play_music
from aura_core.brain.llm_agent import LLMBrain
from aura_core.memory.conversation import ConversationBuffer
from aura_core.memory.persistent_db import AuraDatabase

class IntentRouter:
    def __init__(self):
        self.llm_brain = LLMBrain()
        self.short_memory = ConversationBuffer(max_messages=10)
        self.persistent_db = AuraDatabase()

    def _handle_memory_commands(self, command: str) -> Optional[str]:
        cmd_lower = command.lower().strip()
        
        # 1. "remember that [key] is [value]" or "remember my [key] is [value]"
        remember_match = re.search(r"remember\s+(?:that\s+)?(?:my\s+)?(.+?)\s+is\s+(.+)", cmd_lower)
        if remember_match:
            key = remember_match.group(1).strip()
            val = remember_match.group(2).strip()
            self.persistent_db.save_fact(key, val)
            return f"Got it! I will remember that your {key} is {val}."

        # 2. "what is my [key]" or "what's my [key]"
        recall_match = re.search(r"what(?:'s|\s+is)\s+(?:my\s+)?(.+)", cmd_lower)
        if recall_match:
            key = recall_match.group(1).replace("?", "").strip()
            fact = self.persistent_db.get_fact(key)
            if fact:
                return f"Your {key} is {fact}."

        # 3. "forget my [key]" or "forget [key]"
        forget_match = re.search(r"forget\s+(?:my\s+)?(.+)", cmd_lower)
        if forget_match:
            key = forget_match.group(1).strip()
            deleted = self.persistent_db.delete_fact(key)
            if deleted:
                return f"I have forgotten your {key}."
            else:
                return f"I didn't have any record of your {key}."

        return None

    def route(self, command: str) -> str:
        if not command or not command.strip():
            return ""

        # Process command and determine response
        response = self._process_command(command)

        # Save query and response to memory
        self.persistent_db.save_chat_message("user", command)
        self.short_memory.add_user_message(command)
        
        self.persistent_db.save_chat_message("assistant", response)
        self.short_memory.add_assistant_message(response)

        return response

    def _process_command(self, raw_command: str) -> str:
        command = raw_command.lower().strip()

        # Check explicit memory commands
        mem_response = self._handle_memory_commands(raw_command)
        if mem_response:
            return mem_response

        # 1. Time & Date
        if "time" in command:
            return get_time()
        elif "date" in command:
            return get_date()
        
        # 2. Volume controls
        elif "volume up" in command or "increase volume" in command:
            return set_volume("up")
        elif "volume down" in command or "decrease volume" in command:
            return set_volume("down")
        elif "mute" in command and "unmute" not in command:
            return set_volume("mute")
        elif "unmute" in command:
            return set_volume("unmute")
            
        # 3. Screenshot
        elif "screenshot" in command or "capture screen" in command:
            return take_screenshot()
        
        # 4. Websites & Browser
        elif "open youtube" in command:
            return open_website("youtube")
        elif "open google" in command:
            return open_website("google")
        elif "open github" in command:
            return open_website("github")
        elif "open chatgpt" in command:
            return open_website("chatgpt")
        elif "open chrome" in command or "open browser" in command:
            return open_website("chrome")

        # 5. Play Music / YouTube Search (Catches "play ...", "play song ...", "play music ...")
        elif command.startswith("play") or "play music" in command or "play song" in command:
            song_query = command
            for prefix in ["play music by", "play music", "play songs by", "play song", "play songs", "play"]:
                if song_query.startswith(prefix):
                    song_query = song_query[len(prefix):].strip()
                    break
            
            song_query = song_query.replace("on youtube", "").replace("in youtube", "").strip()
            return play_music(song_query)
        
        # 6. Search
        elif "search for" in command or "google search" in command:
            query = command.replace("search for", "").replace("google search", "").strip()
            return google_search(query)
        
        # 7. Applications
        elif "open notepad" in command:
            return open_application("notepad")
        elif "open code" in command or "open vs code" in command:
            return open_application("code")
        
        # 8. Fallback to LLM Brain with short-term history and persistent user facts
        else:
            history = self.short_memory.get_messages()
            facts = self.persistent_db.get_all_facts()
            return self.llm_brain.ask(raw_command, conversation_history=history, user_facts=facts)