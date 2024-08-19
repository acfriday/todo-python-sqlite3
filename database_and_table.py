import sqlite3
import os

def database():
    db_path = "./todo_database.db"
    db_exists = os.path.exists(db_path)
    
    database_connection = sqlite3.connect(db_path)
    database_connection.row_factory = sqlite3.Row
    
    if db_exists:
        print("++ Connected to current database.")
    else:
        print("++ Creating new database.")
    
    # Check if the table exists before creating it
    cursor = database_connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='todo_items';")
    table_exists = cursor.fetchone() is not None
    
    if not table_exists:
        database_connection.execute("""
        CREATE TABLE IF NOT EXISTS todo_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL
        )
        """)
        print("++ Created the todo_items table in the todo_database.")

    return database_connection

if __name__ == "__main__":
    database()