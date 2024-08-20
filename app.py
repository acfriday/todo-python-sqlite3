from flask import Flask, render_template, request, url_for, redirect, g
from database import build

def run():
    '''
    Create a Flask application for a todo list.
    Includes routes for displaying, inserting, deleting, and editing tasks.
    Manages database connections and operations.
    '''
    app = Flask(__name__)

    def get_database():
        if "db" not in g:
            print("\n++ Connecting...")
            g.db = build()
        return g.db

    @app.teardown_appcontext
    def close_database(exception):
        db = g.pop('db', None)
        if db is not None:
            print("++ Database operations complete, closing connection.\n")
            db.close()

    @app.route("/", methods=["GET"])
    def index():
        if request.method == "GET":
            try:
                db = get_database()
                cursor = db.cursor()
                cursor.execute("SELECT * FROM todo_items")
                todos = cursor.fetchall()
                return render_template("index.html", task_list=todos)
            except Exception as e:
                print(f"Error fetching homepage: {e}")
        return render_template("index.html")

    @app.route("/insert-task", methods=["POST"])
    def insert():
        if request.method == "POST":
            try:
                response = request.form["task"]
                db = get_database()
                cursor = db.cursor()
                cursor.execute("INSERT INTO todo_items (task) VALUES (?)", [response])
                db.commit()
                return redirect(url_for("index"))
            except Exception as e:
                db.rollback()
                print(f"Error inserting task: {e}")
        return render_template("index.html")

    @app.route("/delete-task/<int:id>", methods=["GET"])
    def delete(id):
        if request.method == "GET":
            try:
                db = get_database()
                cursor = db.cursor()
                cursor.execute("DELETE FROM todo_items WHERE id = ?",[id])
                db.commit()
                return redirect(url_for("index"))
            except Exception as e:
                print(f"Error deleting tasks: {e}")
        return render_template("index.html")

    @app.route("/edit-task/<int:id>", methods=["GET", "POST"])
    def edit(id):
        if request.method == "POST":
            try:
                db = get_database()
                new_task = request.form["task"]
                cursor = db.cursor()
                cursor.execute("UPDATE todo_items SET task = ? WHERE id = ?", [new_task, id])
                db.commit()
                return redirect(url_for("index"))
            except Exception as e:
                db.rollback()
                print(f"Error updating task: {e}")
        else:
            try:
                db = get_database()
                cursor = db.cursor()
                cursor.execute("SELECT * FROM todo_items WHERE id = ?", [id])
                task = cursor.fetchone()
                return render_template("edit.html", task=task)
            except Exception as e:
                print(f"Error fetching task for editing: {e}")
        return redirect(url_for("index"))
    return app

def main():
    '''
    Execute the Flask application and handle any loading or configuration errors that may occur.
    '''
    try:
        app = run()
    except Exception as e:
        print(f"Error loading Flask app: {e}")
    try:
        app.run(debug=True, host="0.0.0.0", port=8080)
    except Exception as e:
        print(f"Error configuring Flask app: {e}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error running main function: {e}")