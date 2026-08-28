import os
from datetime import datetime
from flask import Flask, render_template, request, send_from_directory, redirect, url_for, session
from werkzeug.utils import secure_filename
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'mp3', 'wav', 'txt'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Google OAuth Setup (अपनी Google Client ID और Secret यहाँ डालें)
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id='YOUR_GOOGLE_CLIENT_ID',
    client_secret='YOUR_GOOGLE_CLIENT_SECRET',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)

user_histories = {}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    user = session.get('user')
    if not user:
        return render_template('index.html', user=None)
    
    email = user.get('email')
    history = user_histories.get(email, [])
    return render_template('index.html', user=user, history=history, success=False)

@app.route('/upload', methods=['POST'])
def upload():
    user = session.get('user')
    if not user:
        return redirect(url_for('index'))
    
    email = user.get('email')
    if email not in user_histories:
        user_histories[email] = []

    text_input = request.form.get('text_input', '')
    filename = None
    
    if 'media_file' in request.files:
        file = request.files['media_file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            upload_time = datetime.now().strftime('%Y-%m-%d %I:%M %p')
            user_histories[email].insert(0, {
                'filename': filename,
                'time': upload_time,
                'text': text_input if text_input else 'कोई टेक्स्ट नहीं'
            })
    
    return render_template('index.html', user=user, history=user_histories[email], success=True, filename=filename)

@app.route('/login')
def login():
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    token = google.authorize_access_token()
    resp = google.get('https://www.googleapis.com/oauth2/v2/userinfo')
    user_info = resp.json()
    session['user'] = user_info
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    
