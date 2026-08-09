import sqlite3
from pathlib import Path


DB_PATH = Path(__file__).parent.parent.parent / "trip_planner.db"
def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS trips (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            first_day TEXT NOT NULL,
            last_day TEXT NOT NULL,
            description TEXT
        )
        ''')
        conn.commit()