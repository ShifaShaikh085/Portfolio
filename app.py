# app.py
from flask import Flask, render_template, request, redirect, url_for, session

import pymysql

app = Flask(__name__)
app.secret_key = "FaizaanShifa0831"  # Required for session

# Database connection helper
def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        port=3306,
        password='root@123',  # use your actual password
        database='portfolio',
        cursorclass=pymysql.cursors.DictCursor
    )

# Home route
@app.route("/")
def index():
    return render_template("index.html")

# Contact form submission route
@app.route("/contact", methods=["POST"])
def contact():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO contacts (name, email, message) VALUES (%s, %s, %s)", (name, email, message))
    conn.commit()
    conn.close()

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

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM admin WHERE username=%s AND password=%s", (username, password))
        admin = cursor.fetchone()
        conn.close()

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

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contacts ORDER BY id DESC")
    messages = cursor.fetchall()
    conn.close()
    return render_template("admin.html", messages=messages)



@app.route("/logout")
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('login'))


# Run the app
if __name__ == "__main__":
    app.run(debug=True)
