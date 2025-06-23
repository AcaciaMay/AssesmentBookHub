from flask import Flask, g, render_template, request, abort
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
            Title,
            Author,
            Genre,
            Subjects,
            Audience,
            Copies,
            "Image URL",
            Description,
            Availability
        FROM Books
        ORDER BY Title ASC;
    """
    books = query_db(query)
    return render_template("home.html", books=books)

@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("q", "").lower()
    sql = """
    SELECT 
        ROW_NUMBER() OVER (ORDER BY Title ASC) AS RowNum,
        Title,
        Author,
        Genre,
        Subjects,
        Audience,
        Copies,
        "Image URL",
        Description,
        Availability,
        ISBN
    FROM Books
    WHERE LOWER(Title) LIKE ? OR LOWER(Author) LIKE ?
    ORDER BY Title ASC;
"""
    like_query = f"%{query}%"
    results = query_db(sql, (like_query, like_query))
    return render_template("search_results.html", results=results, query=query)

@app.route("/book/<isbn>")
def book_detail(isbn):
    sql = """
    SELECT 
        Title,
        Author,
        Genre,
        Subjects,
        Audience,
        Copies,
        "Image URL",
        Description,
        Availability,
        Publishers, 
        ISBN
    FROM Books
    WHERE ISBN = ?
    """
    book = query_db(sql, (isbn,), one=True)
    if not book:
        abort(404)
    return render_template("book_detail.html", book=book)

@app.route("/book/isbn/<isbn>")
def book_by_isbn(isbn):
    sql = """
    SELECT Title, Author, Genre, Subjects, Audience, Copies, "Image URL", Description, Availability
    FROM Books
    WHERE ISBN = ?;
    """
    result = query_db(sql, [isbn], one=True)
    if result is None:
        return "Book not found", 404
    return render_template("book.html", book=result)

if __name__ == "__main__":
    app.run(debug=True)