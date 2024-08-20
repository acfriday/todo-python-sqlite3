import sqlite3
import os

def init_database():
    """
    Initialize the database connection.
    If the database does not exist, it will be created.
    """
    db_path = "./todo_database.db"
    db_exists = os.path.exists(db_path)
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    if db_exists:
        print("++ Connected to current database.")
    else:
        print("++ Creating new database.")
    return connection

def init_table(db_connection):
    """
    Initialize the todo_items table in the database.
    If the table does not exist, it will be created.
    """
    with db_connection:
        cursor = db_connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='todo_items';")
        table_exists = cursor.fetchone() is not None
        if not table_exists:
            db_connection.execute("""
                CREATE TABLE IF NOT EXISTS todo_items
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL);
                """)
            print("++ Created the todo_items table in the todo_database.")

def build():
    """
    Build the database and initialize the table.
    Returns the database connection if successful, returns None otherwise.
    """
    try:
        db_connection = init_database()
    except Exception as e:
        print(f"Failed to create database: {e}")
        return None
    try:
        init_table(db_connection)
    except Exception as e:
        print(f"Failed to create database table: {e}")
        db_connection.close()
        return None
    return db_connection

if __name__ == "__main__":
    try:
        build()
    except Exception as e:
        print(f"Error running build function: {e}")