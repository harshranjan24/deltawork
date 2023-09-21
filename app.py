from flask import Flask, render_template, request, redirect, session, url_for, flash
import pyodbc
import hashlib

app = Flask(__name__)
app.secret_key = "b'\xc8a\xc1v\xb7>[8k\x93(\x9dCQ\xec'"

# Database connection
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=sqldb-deltawork.database.windows.net;'
                      'Database=sqldb-its-deltawork;'
                      'UID=harsh;'
                      'PWD=H@r$HR2/\/J@N;')

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_password))
    user = cursor.fetchone()
    cursor.close()

    if user:
        session['user_id'] = user.id
        flash('Login successful!', 'success')
        return redirect(url_for('dashboard'))
    else:
        flash('Login failed. Please check your username and password.', 'error')
        return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        return 'Welcome to the dashboard!'
    else:
        flash('You need to log in first.', 'error')
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
