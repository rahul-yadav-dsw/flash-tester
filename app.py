from flask import Flask, request, session, jsonify
import fastwsgi
import socket
from mysql.connector import pooling
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed to use sessions

# Database connection settings
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_HOST_READER = os.getenv('DB_HOST_READER', 'localhost')
DB_PORT = os.getenv('DB_PORT', '3306')
DB_NAME = os.getenv('DB_NAME', 'flaskdb')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')

# Create a connection pool with a 30-second idle timeout and session reset
connection_pool = pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=20,          # Set max pool size to 20
    pool_reset_session=True, # Reset session state for each reused connection
    connection_timeout=30,  # Set idle connection timeout to 30 seconds
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)

# Function to get a connection from the pool for writing
def get_db_connection():
    return connection_pool.get_connection()

# Function to get a connection from the pool for reading
def get_db_connection_reader():
    return connection_pool.get_connection()

# Create the table if it doesn't exist
def init_db():
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS requests (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    lang VARCHAR(50),
                    hostname VARCHAR(100)
                )
            ''')
        conn.commit()

# Route for health check
@app.route('/health', methods=['GET'])
def health():
    return 'OK'

# Route for readiness check
@app.route('/ready', methods=['GET'])
def ready():
    return 'OK'

# Route for hello world, saves data to the database
@app.route('/helloworld', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        session['lang'] = request.form.get('lang')

    lang = session.get('lang', 'not set')
    hostname = socket.gethostname()

    # Insert the request data into the database
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO requests (lang, hostname) VALUES (%s, %s)",
                (lang, hostname)
            )
        conn.commit()

    return f"Language: {lang}, Hostname: {hostname}"

# Route to retrieve requests from the database
@app.route('/requests', methods=['GET'])
def get_requests():
    with get_db_connection_reader() as conn:
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM requests")
            rows = cursor.fetchall()

    return jsonify(rows)

if __name__ == '__main__':
    init_db()
    fastwsgi.run(wsgi_app=app, host='0.0.0.0', port=8080)
