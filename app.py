from flask import Flask, g, render_template
import sqlite3

DATABASE = 'database.db'
app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.route("/")
def home():
    query = """
        SELECT 
            ROW_NUMBER() OVER (ORDER BY Title ASC) AS RowNum,
            *
        FROM Books
        ORDER BY Title ASC;
    """
    books = query_db(query)  # or however you're fetching from the database
    return render_template("home.html", books=books)

@app.route("/book/<int:book_id>")
def book(book_id):
    sql = """
    SELECT BookID, Title, Author, Genre, Subjects, Audience, Copies, "Image URL", Description, Availability
    FROM Books
    WHERE BookID = ?;
    """
    result = query_db(sql, [book_id], one=True)
    if result is None:
        return "Book not found", 404
    return render_template("book.html", book=result)

if __name__ == "__main__":
    app.run(debug=True)