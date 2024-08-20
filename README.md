# Todo Web App

This project is a Todo app implemented in Flask using SQLite3. It allows users to perform create, read, update, and delete (CRUD) operations on the database.

## SQLite Database Structure

The database consists of a single table named `task_items` with the following columns:

- `id`: An integer that serves as the primary key for our table.
- `task`: A text field that stores the user's desired task in the database.

```py
db_connection.execute("""
CREATE TABLE IF NOT EXISTS todo_items(
id INTEGER PRIMARY KEY AUTOINCREMENT,
task TEXT NOT NULL)
""");
```

## Functions

The database includes the following main functions:

- `init_database()`: Builds and returns a connection to the SQLite3 database.
```py
def init_database():
    db_path = "./todo_database.db"
    db_exists = os.path.exists(db_path)
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    if db_exists:
        print("++ Connected to current database.")
    else:
        print("++ Creating new database.")
    return connection
```

- `init_table()`: Creates the `task_items` table in the todo database.
```py
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
                CREATE TABLE IF NOT EXISTS todo_items(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL)
                """);
            print("++ Created the todo_items table in the todo_database.")
```

## Flask Application Structure

The Flask app consists of multiple functions that build routes for performing CRUD actions on the integrated sqlite3 database.

- `main()`: Triggers the Flask app to run and defines its configuration.
```py
def main():
    try:
        app = run()
    except Exception as e:
        print(f"Error loading Flask app: {e}")
    try:
        app.run(debug=True, host="127.0.0.1", port=8080)
    except Exception as e:
        print(f"Error configuring Flask app: {e}")
```

- `run()`: Defines the Flask apps functionality and manage database connections and operations.
```py
def run():
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
```

## Requirements
Flask==3.0.3

## Usage

To run the program, simply execute the `app.py` script. a database will be created in the current working directory and the Flask app will be reachable from `127.0.0.1:8080` in a web browser.

```
> py ./app.py
```

**Homepage**

![image](https://github.com/user-attachments/assets/ecce39d7-2f8a-4471-a683-e61711615e84)

**Adding a task**

![image](https://github.com/user-attachments/assets/4db958b9-db0e-4001-b35b-5962eb873f99)

**Updating a task**

![image](https://github.com/user-attachments/assets/2bbd584a-962c-4a7e-9b0d-463c90f85904)

![image](https://github.com/user-attachments/assets/6302ded9-0567-4d2f-bf5e-54a3bcc2cf5b)

**Deleting a task**

![image](https://github.com/user-attachments/assets/a4907dcc-5570-478c-b0ae-557edae33173)

![image](https://github.com/user-attachments/assets/06c33de9-c450-4c7a-b25a-f39c4e91d030)

## Deploy via Docker Compose

Running `docker compose up --detach` at the command line starts the container in the background. The app can be reached in a web browser at `127.0.0.1:8080`

```
> docker compose up --detach
```