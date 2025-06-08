from flask import Flask, request, send_file, abort, redirect, url_for
import os
import requests
from io import BytesIO
from PIL import Image
import mimetypes
from werkzeug.utils import secure_filename
import socket
import random

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

uploaded_files = []

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_mimetype(file_path):
    mime = mimetypes.guess_type(file_path)[0]
    if mime is None:
        try:
            with Image.open(file_path) as img:
                mime = img.get_format_mimetype()
        except Exception:
            mime = 'application/octet-stream'
    return mime

def find_free_port_in_range(start_port, end_port):
    while True:
        port = random.randint(start_port, end_port)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('0.0.0.0', port))
        s.close()
        return port 

@app.route('/')
def index():
    return '''
    <h1>图片上传</h1>
    <form method="post" enctype="multipart/form-data" action="/upload">
      <input type="file" name="file">
      <input type="submit" value="上传">
    </form>
    <h2>已上传的图片</h2>
    <ul>
    ''' + ''.join(f'<li><a href="/image/{filename}">{filename}</a></li>' for filename in uploaded_files) + '''
    </ul>
    '''

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return '未找到文件部分', 400
    file = request.files['file']

    if file.filename == '':
        return '未选择文件', 400
    if file and allowed_file(file.filename):

        filename = secure_filename(file.filename)
        ext = filename.rsplit('.', 1)[1].lower()

        unique_filename = f"{len(uploaded_files)}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)

        file.save(filepath)
        uploaded_files.append(unique_filename)

        return redirect(url_for('index'))
    else:
        return '文件类型不支持', 400

@app.route('/image/<filename>', methods=['GET'])
def load_image(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(filepath):
        mime = get_mimetype(filepath)
        return send_file(filepath, mimetype=mime)
    else:
        return '文件未找到', 404

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    port = find_free_port_in_range(5001, 6000)
    app.run(host='0.0.0.0', port=port)
