from flask import Flask, request, render_template
import mysql.connector
import os

app = Flask(__name__)

# Cloud SQL connection
db_config = {
    'user': os.environ.get("DB_USER"),
    'password': os.environ.get("DB_PASS"),
    'host': os.environ.get("DB_HOST"),  # e.g., 127.0.0.1 or Cloud SQL IP
    'database': os.environ.get("DB_NAME"),
    'port': 3306
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    email = request.form.get('email')

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
    conn.commit()
    cursor.close()
    conn.close()
    return f"Thank you, {name}!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
