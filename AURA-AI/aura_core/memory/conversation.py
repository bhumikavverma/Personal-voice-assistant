from typing import List, Dict

class ConversationBuffer:
    """
    Manages short-term conversation memory using a sliding window buffer.
    """
    def __init__(self, max_messages: int = 10):
        self.max_messages = max_messages
        self.history: List[Dict[str, str]] = []

    def add_user_message(self, content: str) -> None:
        """Add a user message to short-term memory."""
        self.history.append({"role": "user", "content": content})
        self._trim()

    def add_assistant_message(self, content: str) -> None:
        """Add an assistant response to short-term memory."""
        self.history.append({"role": "assistant", "content": content})
        self._trim()

    def get_messages(self) -> List[Dict[str, str]]:
        """Return the current context buffer as a list of message dicts."""
        return list(self.history)

    def clear(self) -> None:
        """Clear short-term memory."""
        self.history.clear()

    def _trim(self) -> None:
        """Keep only the last max_messages."""
        if len(self.history) > self.max_messages:
            self.history = self.history[-self.max_messages:]
