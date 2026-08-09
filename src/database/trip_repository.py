from src.database.db import get_connection
import sqlite3

def db_add_trip(name, first_day, last_day, description):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO trips (name, first_day, last_day, description) VALUES (?, ?, ?, ?)", (name, first_day, last_day, description))
        conn.commit()
        return cursor.lastrowid

def db_delete_trip(trip_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM trips WHERE id = ?", (trip_id,))
        conn.commit()

def get_all_trips():
    with get_connection() as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM trips")
        rows = cursor.fetchall()
        return rows

def get_trip_by_id(trip_id):
    with get_connection() as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM trips WHERE id = ?", (trip_id,))
        row = cursor.fetchone()
        return row

'''
add_trip("a", "01.01.1999", "01.01.1999", "")
add_trip("b", "03.01.1999", "03.01.1999", "")
add_trip("c", "02.01.1999", "02.01.1999", "")
add_trip("d", "03.01.1998", "03.01.1998", "")
'''