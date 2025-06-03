from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from flask_bcrypt import Bcrypt

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL Config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'ayman123456'
app.config['MYSQL_DB'] = 'flaskauthhub'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Initialize MySQL, Bcrypt, and LoginManager
mysql = MySQL(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Dummy User model
class User(UserMixin):
    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash

@login_manager.user_loader
def load_user(user_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    if user:
        return User(user['id'], user['username'], user['password'])
    return None

# --- Routes ---

@app.route('/')
def home():
    return '''
    Welcome to FlaskAuthHub1!
    <p><a href="/login">Login</a></p>
    <p><a href="/register">Register</a></p>
    '''

@app.route('/testdb')
def test_db():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT 1')
        cursor.close()
        return "✅ MySQL connection successful!"
    except Exception as e:
        return f"❌ MySQL connection failed: {e}"

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Validate input
        if not username or not password:
            flash('Username and password are required.', 'danger')
            return redirect(url_for('register'))

        # Hash the password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Insert user into the database
        try:
            cursor = mysql.connection.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
            mysql.connection.commit()
            cursor.close()
            flash('Registration successful. You can now log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f'Error during registration: {e}', 'danger')
            return redirect(url_for('register'))

    return render_template('register.html')  # Correct relative path

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password_input = request.form['password']

        # Validate input
        if not username or not password_input:
            flash('Username and password are required.', 'danger')
            return redirect(url_for('login'))

        # Fetch user from the database
        try:
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
            cursor.close()

            # Check password and log in the user
            if user and bcrypt.check_password_hash(user['password'], password_input):
                user_obj = User(user['id'], user['username'], user['password'])
                login_user(user_obj)
                flash('Login successful!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Login failed. Check your credentials.', 'danger')
        except Exception as e:
            flash(f'Error during login: {e}', 'danger')

    return render_template('login.html')  # Correct relative path

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')  # Correct relative path

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# Run app
if __name__ == '__main__':
    app.run(debug=True)