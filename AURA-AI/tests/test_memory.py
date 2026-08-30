import sys
import os
import unittest
from unittest.mock import MagicMock

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from aura_core.memory.conversation import ConversationBuffer
from aura_core.memory.persistent_db import AuraDatabase
from aura_core.brain.router import IntentRouter

class TestMemorySystem(unittest.TestCase):
    def setUp(self):
        self.db = AuraDatabase(db_path=":memory:")
        self.buffer = ConversationBuffer(max_messages=4)

    def test_conversation_buffer_sliding_window(self):
        self.buffer.add_user_message("Hello 1")
        self.buffer.add_assistant_message("Hi 1")
        self.buffer.add_user_message("Hello 2")
        self.buffer.add_assistant_message("Hi 2")
        self.buffer.add_user_message("Hello 3")

        messages = self.buffer.get_messages()
        self.assertEqual(len(messages), 4)
        self.assertEqual(messages[0]["content"], "Hi 1")
        self.assertEqual(messages[-1]["content"], "Hello 3")

    def test_persistent_user_facts(self):
        self.db.save_fact("name", "Rahul")
        self.db.save_fact("favorite color", "Blue")

        self.assertEqual(self.db.get_fact("name"), "Rahul")
        self.assertEqual(self.db.get_fact("favorite color"), "Blue")

        all_facts = self.db.get_all_facts()
        self.assertIn("name", all_facts)
        self.assertIn("favorite color", all_facts)

        deleted = self.db.delete_fact("favorite color")
        self.assertTrue(deleted)
        self.assertIsNone(self.db.get_fact("favorite color"))

    def test_chat_history_logging(self):
        self.db.save_chat_message("user", "What is the time?")
        self.db.save_chat_message("assistant", "It is 5:00 PM.")

        recent = self.db.get_recent_chats(limit=10)
        self.assertEqual(len(recent), 2)
        self.assertEqual(recent[0]["role"], "user")
        self.assertEqual(recent[0]["content"], "What is the time?")
        self.assertEqual(recent[1]["role"], "assistant")

    def test_router_memory_commands(self):
        router = IntentRouter()
        # Replace DB with in-memory DB for test
        router.persistent_db = AuraDatabase(db_path=":memory:")
        router.llm_brain.ask = MagicMock(return_value="LLM Response")

        # Test storing fact
        res1 = router.route("Remember that my name is Rahul")
        self.assertIn("rahul", res1.lower())

        # Test recalling fact
        res2 = router.route("What is my name?")
        self.assertEqual(res2, "Your name is rahul.")

        # Test forgetting fact
        res3 = router.route("Forget my name")
        self.assertIn("forgotten", res3.lower())

        # Test after forgetting
        res4 = router.route("What is my name?")
        # Should fallback to LLM since fact is forgotten
        self.assertEqual(res4, "LLM Response")

if __name__ == "__main__":
    unittest.main()
