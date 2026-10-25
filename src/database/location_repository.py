from src.database.db import get_connection
import sqlite3

def db_add_location(trip_id, name, latitude, longitude, address=None):
    with get_connection() as conn:
        cursor = conn.cursor()
        conn.execute("INSERT INTO locations (trip_id, name, latitude, longitude, address) VALUES (?, ?, ?, ?, ?)", (trip_id, name, latitude, longitude, address))
        conn.commit()
        return cursor.lastrowid

def db_delete_location(location_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM locations WHERE id = ?", (location_id,))
        conn.commit()

def get_locations_by_trip_id(trip_id):
    with get_connection() as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM locations WHERE trip_id = ?", (trip_id,))
        rows = cursor.fetchall()
        result = []
        for row in rows:
            result.append({
                "id": row["id"],
                "trip_id": row["trip_id"],
                "name": row["name"],
                "lat": row["latitude"],
                "lng": row["longitude"],
                "address": row["address"]
            })
        return result