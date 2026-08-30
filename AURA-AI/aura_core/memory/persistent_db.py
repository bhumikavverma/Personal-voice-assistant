import os
import sqlite3
from typing import List, Dict, Optional

class AuraDatabase:
    """
    SQLite persistent storage for AURA chat history and user facts/preferences.
    """
    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
            db_dir = os.path.join(base_dir, "database")
            os.makedirs(db_dir, exist_ok=True)
            db_path = os.path.join(db_dir, "aura_memory.db")
        
        self.db_path = db_path
        self._conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self._init_db()

    def _init_db(self):
        """Create database tables if they do not exist."""
        cursor = self._conn.cursor()
        
        # Chat history table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                role TEXT NOT NULL,
                content TEXT NOT NULL
            )
        """)
        
        # User facts table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_facts (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        self._conn.commit()

    def save_chat_message(self, role: str, content: str) -> None:
        """Save a chat message to history."""
        cursor = self._conn.cursor()
        cursor.execute(
            "INSERT INTO chat_history (role, content) VALUES (?, ?)",
            (role, content)
        )
        self._conn.commit()

    def get_recent_chats(self, limit: int = 20) -> List[Dict[str, str]]:
        """Retrieve recent chat history."""
        cursor = self._conn.cursor()
        cursor.execute(
            "SELECT role, content, timestamp FROM chat_history ORDER BY id DESC LIMIT ?",
            (limit,)
        )
        rows = cursor.fetchall()
        # Return in chronological order
        return [
            {"role": row[0], "content": row[1], "timestamp": row[2]}
            for row in reversed(rows)
        ]

    def save_fact(self, key: str, value: str) -> None:
        """Save or update a user fact/preference (key converted to lowercase)."""
        key_clean = key.strip().lower()
        cursor = self._conn.cursor()
        cursor.execute("""
            INSERT INTO user_facts (key, value, updated_at) 
            VALUES (?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(key) DO UPDATE SET 
                value = excluded.value,
                updated_at = CURRENT_TIMESTAMP
        """, (key_clean, value.strip()))
        self._conn.commit()

    def get_fact(self, key: str) -> Optional[str]:
        """Get a specific fact by key."""
        key_clean = key.strip().lower()
        cursor = self._conn.cursor()
        cursor.execute("SELECT value FROM user_facts WHERE key = ?", (key_clean,))
        row = cursor.fetchone()
        return row[0] if row else None

    def get_all_facts(self) -> Dict[str, str]:
        """Retrieve all stored user facts."""
        cursor = self._conn.cursor()
        cursor.execute("SELECT key, value FROM user_facts")
        rows = cursor.fetchall()
        return {row[0]: row[1] for row in rows}

    def delete_fact(self, key: str) -> bool:
        """Delete a fact by key."""
        key_clean = key.strip().lower()
        cursor = self._conn.cursor()
        cursor.execute("DELETE FROM user_facts WHERE key = ?", (key_clean,))
        deleted = cursor.rowcount > 0
        self._conn.commit()
        return deleted

    def close(self):
        """Close database connection."""
        if self._conn:
            self._conn.close()
