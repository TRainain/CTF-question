from flask import Flask, request, jsonify
import datetime
from secret import mix, check

app = Flask(__name__)
log_path = "text.txt"

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html lang="zh">
    <head>
        <meta charset="UTF-8">
        <title>日志记录</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            .container { width: 80%; margin: auto; }
            textarea { width: 100%; height: 100px; margin-bottom: 10px; }
            button { padding: 10px 20px; font-size: 16px; }
            #logDisplay { width: 100%; background-color: #f9f9f9; border: 1px solid #ccc; margin-top: 20px; padding: 10px; height: 200px; overflow-y: scroll; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>日志记录器</h1>
            <textarea id="logInput" placeholder="在此输入日志..."></textarea>
            <button onclick="addLog()">添加日志</button>
            <div id="logDisplay"></div>
        </div>
        <script>
            function addLog() {
                var log = document.getElementById('logInput').value.trim();
                if (log) {
                    fetch('/add_log', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ log: log })
                    })
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById('logDisplay').innerText += data.log + '\\n';
                        document.getElementById('logInput').value = '';
                    });
                }
            }
        </script>
    </body>
    </html>
    '''

class logtext():
    def __init__(self):
        self.time = ""
        self.log = ""
        pass

@app.route('/add_log', methods=['POST'])
def add_log():
    data = request.get_json()
    if check(data):
        return "Hacker!!!"
    log = data['log']
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    full_log = f"{timestamp}: {log}\n"
    mix(data, logtext())
    with open('text.txt', 'a') as f:
        f.write(full_log)
    return jsonify({'log': full_log})


@app.route('/see_log', methods=['GET'])
def see_log():
    return open(log_path, "r").read()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
