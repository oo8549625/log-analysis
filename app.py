import gzip
import io
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

def log_handler(hits_list):
    status_code_counts_by_host_uri = {}
    
    for hit in hits_list:
        host = hit['_source']['host']
        uri = hit['_source']['request_uri']
        status_code = hit['_source']['status']
        
        if host not in status_code_counts_by_host_uri:
            status_code_counts_by_host_uri[host] = {}
        
        if uri not in status_code_counts_by_host_uri[host]:
            status_code_counts_by_host_uri[host][uri] = {}
        
        status_code_counts_by_host_uri[host][uri][status_code] = status_code_counts_by_host_uri[host][uri].get(status_code, 0) + 1

    return status_code_counts_by_host_uri

def tg_send(data):
    for host, uri_counts in data.items():
        print(f"域名 {host}:")
        for uri, status_code_counts in uri_counts.items():
            print(f"  請求URI {uri}:")
            for status_code, count in status_code_counts.items():
                print(f"    狀態碼 {status_code}: {count} 次訪問")

@app.route('/')
def home():
    return "log-analysis"

@app.route('/api/v1/log/write', methods=['POST'])
def receive_json():
    content_encoding = request.headers.get('content-encoding', '')
    if content_encoding == 'gzip':
        buf = io.BytesIO(request.data)
        gf = gzip.GzipFile(fileobj=buf)
        content = gf.read().decode('UTF-8')
    else:
        content = request.json

    hits_list = json.loads("[" + content.get('context_hits') + "]")
    tg_send(log_handler(hits_list))
    return jsonify({"message": "JSON received", "data": content})

if __name__ == '__main__':
    app.run()