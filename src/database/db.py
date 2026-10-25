import sqlite3
from pathlib import Path


DB_PATH = Path(__file__).parent.parent.parent / "trip_planner.db"
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

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

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS locations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            trip_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            latitude REAL,
            longitude REAL,
            address TEXT,
            FOREIGN KEY(trip_id) REFERENCES trips(id) ON DELETE CASCADE
        )
        ''')
        conn.commit()