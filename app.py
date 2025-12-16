import os, sqlite3, uuid, hashlib, datetime
from flask import Flask, request, redirect, url_for, send_from_directory, abort, render_template
from werkzeug.utils import secure_filename

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
DB_PATH = os.path.join(BASE_DIR, 'files.db')

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "txt", "pdf", "zip", "dock"}
MAX_FILE_SIZE = 20 * 1024 * 1024

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def get_db():
    return sqlite3.connect(DB_PATH)

def init_db():
    with get_db() as db:
        db.execute("""
        CREATE TABLE IF NOT EXISTS files (
            id TEXT PRIMARY KEY,
            original_name TEXT,
            stored_name TEXT,
            password_hash TEXT,
            max_downloads INTEGER,
            downloads INTEGER DEFAULT 0,
            expires_at TEXT
        )
        """)

init_db()

def allowed_file(name):
    return '.' in name and name.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#не сам
def hash_password(p):
    return hashlib.sha256(p.encode()).hexdigest() if p else None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files.get('file')
        if not file or not allowed_file(file.filename): abort(400)

        fid = str(uuid.uuid4()) #не сам
        name = secure_filename(file.filename)
        stored = f"{fid}_{name}"
        file.save(os.path.join(UPLOAD_FOLDER, stored))

        expires = request.form.get('expires')
        expires_at = (datetime.datetime.utcnow() + datetime.timedelta(hours=int(expires))).isoformat() if expires else None

        with get_db() as db:
            db.execute("INSERT INTO files VALUES (?,?,?,?,?,0,?)", (
                fid, name, stored,
                hash_password(request.form.get('password')),
                request.form.get('limit'), expires_at
            ))

        return render_template('index.html', link=url_for('download', file_id=fid, _external=True))

    return render_template('index.html')

@app.route('/f/<file_id>', methods=['GET', 'POST'])
def download(file_id):
    with get_db() as db:
        row = db.execute("SELECT * FROM files WHERE id=?", (file_id,)).fetchone()

    if not row: abort(404)

    _, orig, stored, pwd, limit, count, exp = row
    if exp and datetime.datetime.utcnow() > datetime.datetime.fromisoformat(exp): abort(403)
    if limit and count >= int(limit): abort(403)

    if pwd:
        if request.method == 'POST':
            if hash_password(request.form.get('password')) != pwd: abort(403)
        else:
            return render_template('download.html')

    with get_db() as db:
        db.execute("UPDATE files SET downloads=downloads+1 WHERE id=?", (file_id,))

    return send_from_directory(UPLOAD_FOLDER, stored, as_attachment=True, download_name=orig)

if __name__ == '__main__':
    app.run(debug=True, host='192.168.1.13', port=5000)
