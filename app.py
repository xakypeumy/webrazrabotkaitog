from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os
from werkzeug.utils import secure_filename

connection = sqlite3.connect('fileshare.db', check_same_thread=False)
cursor = connection.cursor()
try:
    cursor.execute('BEGIN')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    filename TEXT NOT NULL,
    file_path TEXT NOT NULL,
    file_size INTEGER NOT NULL,
    file_type TEXT NOT NULL,
    upload_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    expires_at DATETIME,
    password_protected BOOLEAN DEFAULT FALSE,
    downloads_count INTEGER DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES Users(id)
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Links (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_id INTEGER NOT NULL,
    link_token VARCHAR(64) UNIQUE NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (file_id) REFERENCES Files(file_id)
    )
    ''')
    cursor.execute('COMMIT')
except:
    cursor.execute('ROLLBACK')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'Uploads'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024

# папка для загрузки
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ('jpg', 'jpeg', 'gif', 'png', 'txt', 'pdf', 'gif')

if __name__ == '__main__':
    app.run(debug=True, host='192.168.1.13', port=5000)