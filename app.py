from flask import Flask, render_template, request, redirect, url_for
import pyodbc

app = Flask(__name__)

# Create a connection to the MSSQL database
conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=sqldb-deltawork.database.windows.net;DATABASE=sqldb-its-deltawork;UID=harsh;PWD=H@r$HR2/\/J@N')

# Define a function to authenticate a user
def authenticate(username, password):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()
    cursor.close()
    return user

# Define a route for the login page
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = authenticate(username, password)
        if user:
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid username or password.')

    return render_template('login.html')

# Define a route for the index page
@app.route('/index')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
