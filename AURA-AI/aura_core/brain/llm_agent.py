import os
from typing import List, Dict, Optional
from dotenv import load_dotenv
from groq import Groq

class LLMBrain:
    def __init__(self):
        self.env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))
        self.base_system_prompt = (
            "You are AURA, an advanced, witty, and concise personal AI voice assistant. "
            "Keep your answers short, conversational, and direct, as they will be spoken out loud."
        )
        self.client = None
        self._init_client()

    def _init_client(self):
        """Loads .env file and initializes Groq client if key is valid."""
        load_dotenv(dotenv_path=self.env_path, override=True)
        api_key = os.getenv("GROQ_API_KEY")
        
        if api_key and api_key.strip() and not api_key.startswith("your_"):
            try:
                self.client = Groq(api_key=api_key.strip())
            except Exception:
                self.client = None
        else:
            self.client = None

    def ask(self, query: str, conversation_history: Optional[List[Dict[str, str]]] = None, user_facts: Optional[Dict[str, str]] = None) -> str:
        """
        Queries Groq LLM with system prompt, persistent user facts, and short-term conversation memory.
        """
        # Re-check client in case .env was updated
        if not self.client:
            self._init_client()

        if not self.client:
            return "GROQ_API_KEY is not configured in your .env file. Please add your Groq API key to the .env file."

        try:
            system_content = self.base_system_prompt
            
            # Inject persistent user facts if present
            if user_facts:
                facts_str = "\n".join([f"- {k}: {v}" for k, v in user_facts.items()])
                system_content += f"\n\nKnown facts about the user:\n{facts_str}"
            
            messages = [{"role": "system", "content": system_content}]
            
            # Append short-term conversation context buffer
            if conversation_history:
                messages.extend(conversation_history)
            
            # Append latest query if not already in context
            if not conversation_history or (conversation_history[-1].get("content") != query):
                messages.append({"role": "user", "content": query})

            chat_completion = self.client.chat.completions.create(
                messages=messages,
                model="llama-3.3-70b-versatile",
                temperature=0.7,
                max_tokens=150
            )
            return chat_completion.choices[0].message.content.strip()
        except Exception as e:
            return f"I encountered an error connecting to my brain: {str(e)}"