from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('library.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    books = conn.execute('SELECT * FROM books').fetchall()
    conn.close()
    return render_template('index.html', books=books)

# Определение класса User 
class User(UserMixin): 
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password_hash = password 

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Flask-Login требует эти методы
    def get_id(self):
        return str(self.id) 

# Настройка login_manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Название функции-представления для страницы входа

@login_manager.user_loader
def load_user(user_id):
    # Здесь вам нужно реализовать загрузку пользователя из базы данных по его id
    # Например:
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    if user:
        return User(user['id'], user['username'], user['password']) 
    return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Здесь вам нужно реализовать проверку учетных данных пользователя
        # Например:
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()

        if user and user.check_password(password): 
            login_user(user)
            flash('Logged in successfully.')
            return redirect(url_for('index'))  # Или на другую страницу после входа
        else:
            flash('Invalid username or password.')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)