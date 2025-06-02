from flask import Flask
from flask_mysqldb import MySQL



app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'ayman123456'
app.config['MYSQL_DB'] = 'flaskauthhub'

# Initialize MySQL
mysql = MySQL(app)

# Test route to confirm DB setup
@app.route('/')
def index():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT DATABASE();")
        db_name = cursor.fetchone()[0]
        cursor.close()
        return f"Connected to database: {db_name}"
    except Exception as e:
        return f"Database connection failed: {e}"

if __name__ == '__main__':
    app.run(debug=True)
