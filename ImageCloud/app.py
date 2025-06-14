from flask import Flask, request, send_file, abort, redirect, url_for
import os
import requests
from io import BytesIO
from PIL import Image
import mimetypes
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'static/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

uploaded_files = []

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
        ''' + ''.join(
            f'<li><a href="/image?url=http://localhost:5000/static/{filename}">{filename}</a></li>'
            for filename in uploaded_files
        ) + '''
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

@app.route('/image', methods=['GET'])
def load_image():
    url = request.args.get('url')
    if not url:
        return 'URL 参数缺失', 400

    try:
        response = requests.get(url)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))

        img_io = BytesIO()
        img.save(img_io, img.format)
        img_io.seek(0)
        return send_file(img_io, mimetype=img.get_format_mimetype())
    except Exception as e:
        return f"无法加载图片: {str(e)}", 400

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(host='0.0.0.0', port=5000)
