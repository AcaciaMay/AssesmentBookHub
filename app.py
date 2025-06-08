from flask import Flask, g, render_template, request
import sqlite3

DATABASE = 'database.db'
app = Flask(__name__)

books = [
"The Handmaid's Tale",
"1984",
"Brave New World",
"The Food Lab"
]

app.route('/')
def home():
    return render_template('home.html')

app.route('/search') 
def search():
    query = request.args.get('q', '').lower()
    results = [book for book in books if query in book.lower()]
    return render_template('search_results.html', results=results, query=query)

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