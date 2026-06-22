import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)

# --- Database setup function ---
def init_db():
    conn = sqlite3.connect("data.db")      # this will create data.db file if it doesn't exist
    cur = conn.cursor()
    # create table if it doesn't exist
    cur.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# call it once when app starts
init_db()

@app.route("/", methods=["GET", "POST"])
def home():
    message = ""
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")

        # save to database
        conn = sqlite3.connect("data.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO contacts (name, email) VALUES (?, ?)", (name, email))
        conn.commit()
        conn.close()

        message = "Data saved successfully!"

    return render_template("home.html", msg=message)
@app.route("/view")
def view_data():
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM contacts")
    rows = cur.fetchall()
    conn.close()
    return render_template("view.html", data=rows)


if __name__ == "__main__":
    app.run(debug=True)
