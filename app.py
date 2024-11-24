from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database setup
DB_NAME = "expenses.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                description TEXT,
                amount REAL
            )
        ''')
    print("Database initialized.")

# Routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add", methods=["POST"])
def add_expense():
    date = request.form["date"]
    description = request.form["description"]
    amount = request.form["amount"]

    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("INSERT INTO expenses (date, description, amount) VALUES (?, ?, ?)",
                     (date, description, amount))
    return redirect(url_for("view_expenses"))

@app.route("/view")
def view_expenses():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.execute("SELECT id, date, description, amount FROM expenses")
        expenses = cursor.fetchall()
    return render_template("view_expenses.html", expenses=expenses)

@app.route("/delete/<int:expense_id>")
def delete_expense(expense_id):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    return redirect(url_for("view_expenses"))

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=8080)
