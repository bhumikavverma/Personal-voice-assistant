import sys
import os
import unittest
from unittest.mock import patch

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from aura_core.brain.router import IntentRouter
from aura_core.memory.persistent_db import AuraDatabase

class TestRouterActions(unittest.TestCase):
    def setUp(self):
        self.router = IntentRouter()
        self.router.persistent_db = AuraDatabase(db_path=":memory:")

    @patch("webbrowser.open")
    def test_open_chrome(self, mock_web_open):
        res = self.router.route("open chrome")
        self.assertEqual(res, "Opening Chrome")
        mock_web_open.assert_called_with("https://www.google.com")

    @patch("webbrowser.open")
    def test_play_music(self, mock_web_open):
        res = self.router.route("play believer")
        self.assertIn("Playing believer on YouTube", res)
        mock_web_open.assert_called()

    @patch("webbrowser.open")
    def test_play_songs_by_artist(self, mock_web_open):
        res = self.router.route("play songs by Arijit Singh")
        self.assertIn("arijit singh", res.lower())
        self.assertIn("on youtube", res.lower())
        mock_web_open.assert_called()

    def test_llm_missing_api_key_fallback(self):
        self.router.llm_brain.client = None
        res = self.router.route("tell me a random science fact")
        self.assertIn("GROQ_API_KEY is not configured", res)

if __name__ == "__main__":
    unittest.main()
