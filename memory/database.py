import sqlite3
from pathlib import Path

# Store the database inside the memory folder
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "eduagent.db"


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()

    # Store performance statistics for each generation strategy
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS strategy_stats (
            strategy_id TEXT PRIMARY KEY,
            count INTEGER DEFAULT 0,
            total_reward REAL DEFAULT 0.0,
            average_reward REAL DEFAULT 0.0
        )
    """)

    connection.commit()
    connection.close()


if __name__ == "__main__":
    initialize_database()
    print("EduAgent database initialized successfully!")