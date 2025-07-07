# app.py
from flask import Flask, render_template, request, redirect, url_for, session
import datetime
import sqlite3

app = Flask(__name__)
app.secret_key = "FaizaanShifa0831"  # Required for session


from pymongo import MongoClient

def get_db_connection():
    # Replace with your actual connection string
    MONGO_URI = (
        "mongodb+srv://shaikhshifu15:3HUDrVwTMzirR1mx"
        "@portfolio.qnfwjlx.mongodb.net/portfolio_db"
        "?retryWrites=true&w=majority"
        "&appName=portfolio"
        "&tlsInsecure=true"
    )

    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    return client['portfolio_db']

# Home route
@app.route("/")
def index():
    return render_template("index.html")

# Contact form submission route



@app.route("/contact", methods=["POST"])
def contact():
    name    = request.form['name']
    email   = request.form['email']
    message = request.form['message']

    db = get_db_connection()
    contacts = db['contacts']  # your collection name
    contacts.insert_one({
        "name": name,
        "email": email,
        "message": message
    })

    return render_template("index.html", success=True)


# Admin panel route
# @app.route("/admin")
# def admin():
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM contacts ORDER BY id DESC")
#     messages = cursor.fetchall()
#     conn.close()
#     return render_template("admin.html", messages=messages)







@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        db = get_db_connection()
        admin_coll = db['admin']  # your admin collection
        # find_one returns a dict-like object or None
        admin = admin_coll.find_one({
            "username": username,
            "password": password
        })

        if admin:
            session['admin_logged_in'] = True
            return redirect(url_for('admin'))
        else:
            return render_template("login.html", error="Invalid username or password.")

    return render_template("login.html")




@app.route("/admin")
def admin():
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))

    db = get_db_connection()
    contacts = list(db['contacts']
                    .find()
                    .sort("created_at", -1))  # newest first

    return render_template("admin.html", messages=contacts)




@app.route("/logout")
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('login'))


# Run the app
if __name__ == "__main__":
    app.run(debug=True)
