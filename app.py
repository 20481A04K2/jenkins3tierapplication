from flask import Flask, request, send_file
import mysql.connector

app = Flask(__name__)

# Cloud SQL connection config (hardcoded correctly)
db_config = {
    'user': 'vamsi',
    'password': 'Svamsi79955',
    'host': '34.81.37.59',
    'database': 'jenkins',
    'port': 3306
}

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    email = request.form.get('email')

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
        conn.commit()
        cursor.close()
        conn.close()

        return f"Thank you, {name}!"
    except Exception as e:
        return f"Internal Server Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
