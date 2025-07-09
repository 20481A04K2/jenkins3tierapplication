from flask import Flask, request, send_file
import mysql.connector
import os

app = Flask(__name__)

# Cloud SQL connection config
db_config = {
    'user': os.environ.get("vamsi"),
    'password': os.environ.get("Svamsi79955"),
    'host': os.environ.get("34.81.37.59"),
    'database': os.environ.get("jenkins"),
    'port': 3306
}

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    email = request.form.get('email')

    # Save to Cloud SQL
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
    conn.commit()
    cursor.close()
    conn.close()

    return f"Thank you, {name}!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
