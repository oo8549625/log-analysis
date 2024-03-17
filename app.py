import gzip
import io
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "log-analysis"

@app.route('/receive_json', methods=['POST'])
def receive_json():
    content_encoding = request.headers.get('content-encoding', '')
    if content_encoding == 'gzip':
        buf = io.BytesIO(request.data)
        gf = gzip.GzipFile(fileobj=buf)
        content = gf.read().decode('UTF-8')
    else:
        content = request.json

    print(content)
    return jsonify({"message": "JSON received", "data": content})

if __name__ == '__main__':
    app.run()
