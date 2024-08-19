import sqlite3
from flask import Flask, render_template, request, url_for, redirect, g
from database_and_table import database

app = Flask(__name__)

def get_database():
    if "db" not in g:
        print("\n++ Connecting...")
        g.db = database()
    return g.db

@app.teardown_appcontext
def close_database(exception):
    db = g.pop('db', None)
    if db is not None:
        print("++ Database operations complete, closing connection.\n")
        db.close()

@app.route('/')
def index():
    db = get_database()
    # Perform database operations
    return "Database connected!"



if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=8080)