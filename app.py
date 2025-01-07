from flask import Flask, request, jsonify
from flask import render_template
import sqlite3

app = Flask(__name__)

# Database setup
DATABASE = 'tourists.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tourists (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            country TEXT NOT NULL,
            preferences TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit_form():
    try:
        # Get form data
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        country = request.form['country']
        preferences = request.form['preferences']

        # Insert data into the database
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO tourists (name, email, phone, country, preferences)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, email, phone, country, preferences))
        conn.commit()
        conn.close()

        # Return a success message
        return '''
            <h1>Success!</h1>
            <p>Your information has been successfully submitted.</p>
            <a href="/">Go Back to Home</a>
        '''
    except Exception as e:
        # Return an error message
        return f"An error occurred: {e}"

@app.route('/view', methods=['GET'])
def view_tourists():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tourists')
    rows = cursor.fetchall()
    conn.close()

    return jsonify(rows)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=8080)
