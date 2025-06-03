from flask import Flask
from flask_mysqldb import MySQL
from flask import request
import pymysql

pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'ayman123456'
app.config['MYSQL_DB'] = 'flaskauthhub'



mysql = MySQL(app)

@app.route('/')
def index():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users;")
        data = cursor.fetchall()
        return f"Data: {data}"
    except Exception as e:
        return f"Error: {e}"

if __name__ == '__main__':
    app.run(debug=True)
