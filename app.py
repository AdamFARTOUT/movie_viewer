from flask import Flask, render_template, request, session, redirect, url_for, abort, g
import requests
from functools import wraps
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "Adam"
app.config['DATABASE'] = "users.db"

API_KEY = "b1f902a3"

# Authentication decorators
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user'):
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user') or session.get('user') != 'admin':
            abort(403)  # Forbidden access
        return f(*args, **kwargs)
    return decorated_function

# Database helper functions
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()

        # Drop table (facultatif, mais on le fait séparément)
        db.execute("DROP TABLE IF EXISTS users;")
        db.commit()

        # Create table
        db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            );
        """)
        db.commit()

        # Ajouter admin seulement s'il n'existe pas
        admin = db.execute("SELECT * FROM users WHERE username = 'admin'").fetchone()
        if not admin:
            hashed_pw = generate_password_hash('admin123')
            db.execute("""
                INSERT INTO users (username, email, password)
                VALUES (?, ?, ?)
            """, ('admin', 'admin@gmail.com', hashed_pw))
            db.commit()

# Routes
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()

        if user and check_password_hash(user[3], password):
            session["user"] = username
            return redirect("/")
        else:
            error = "Invalid credentials."
    return render_template("login.html", error=error)

@app.route("/register", methods=["GET", "POST"])
def register():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"], method='pbkdf2:sha256')

        try:
            db = get_db()
            db.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                      (username, email, password))
            db.commit()
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            error = "Username or email already exists."
    return render_template("registre.html", error=error)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/results", methods=["POST"])
def search():
    movie = request.form.get("movie")
    if not movie:
        return render_template("result.html", movies=[], error="Please enter a movie title.")

    url = f"https://www.omdbapi.com/?apikey={API_KEY}&s={movie}"
    response = requests.get(url)
    data = response.json()

    if data.get("Response") == "True":
        return render_template("result.html", movies=data["Search"])
    else:
        return render_template("result.html", movies=[], error=data.get("Error", "No results found."))

@app.route('/admin/users', methods=['GET', 'POST'])
@login_required
@admin_required
def manage_users():
    db = get_db()
    message = None
    
    if request.method == 'POST':
        # Handle user deletion
        if 'delete_id' in request.form:
            if request.form['delete_id'] != '1':  # Prevent deleting admin
                db.execute("DELETE FROM users WHERE id = ?", (request.form['delete_id'],))
                db.commit()
                message = "User deleted successfully"
            else:
                message = "Cannot delete admin user"
        
        # Handle user creation
        elif all(k in request.form for k in ['new_username', 'new_email', 'new_password']):
            try:
                hashed_pw = generate_password_hash(request.form['new_password'])
                db.execute(
                    "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                    (request.form['new_username'], request.form['new_email'], hashed_pw)
                )
                db.commit()
                message = "User created successfully"
            except sqlite3.IntegrityError:
                message = "Username/email already exists"
    
    users = db.execute("SELECT id, username, email, password FROM users").fetchall()
    return render_template('user_database.html', users=users, message=message)

@app.route("/movie/<imdb_id>")
def movie_details(imdb_id):
    url = f"https://www.omdbapi.com/?apikey={API_KEY}&i={imdb_id}&plot=full"
    response = requests.get(url)
    movie = response.json()
    return render_template("details.html", movie=movie)
@app.route("/debug/dbpath")
def debug_dbpath():
    import os
    db_path = os.path.abspath(app.config['DATABASE'])
    exists = "Exists" if os.path.exists(db_path) else "Does NOT exist"
    return f"Database path: {db_path} ({exists})"
if __name__ == "__main__":
    init_db()
    app.run(debug=True)