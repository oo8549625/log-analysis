import gzip
import io
import os
import json
import asyncio
import csv
import fcntl
import telegram
from flask import Flask, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

def log_handler(hits_list: object) -> object:
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

def acquire_lock(lock_file):
    """
    獲取文件所
    """
    try:
        lock_fd = open(lock_file, 'w')
        fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        return lock_fd
    except IOError:
        print("無法獲取鎖，請檢查是否有其他進程正在使用該文件。")
        return None
    
def release_lock(lock_fd):
    """
    釋放文件鎖
    """
    fcntl.flock(lock_fd, fcntl.LOCK_UN)
    lock_fd.close()

async def tg_send(ip: str, date: str, total: str, link: str, data: object) -> None:
    bot = telegram.Bot(os.getenv("TELEGRAM_TOKEN"))

    date_obj_utc = datetime.strptime(date[:-1], "%Y-%m-%dT%H:%M:%S.%f")
    date_obj_8 = date_obj_utc + timedelta(hours=8)
    date_str_8 = date_obj_8.strftime("%Y-%m-%d %H:%M:%S.%f")

    domains_dir = "domains"
    os.makedirs(domains_dir, exist_ok=True)
    message = f'異常IP: <code>{ip}</code>\n時間: {date_str_8[:-7]}\n訪問總次數: {total}\n連結: <a href="{link}">link</a>\n'

    for host, uri_counts in data.items():
        message += f"域名: {host}\n"
        file_path = f"{domains_dir}/{ip}-{host}.csv"
        lock_fd = acquire_lock(file_path)
        if lock_fd:
            try:
                csv_writer = csv.writer(lock_fd)
                csv_writer.writerow(["URI", "CODE", "COUNT"])
                for uri, status_code_counts in uri_counts.items():
                    file_message = [uri]
                    for status_code, count in status_code_counts.items():
                        file_message.append(status_code)
                        file_message.append(count)
                    csv_writer.writerow(file_message)
            finally:
                release_lock(lock_fd)

    await bot.sendMessage(chat_id=os.getenv("CHAT_ID"), text=message, parse_mode='html')
    for host in data.keys():
        document = open(f"{domains_dir}/{ip}-{host}.csv", 'rb')
        await bot.send_document(chat_id=os.getenv("CHAT_ID"), document=document)


@app.route('/')
def home():
    return "log-analysis"

@app.route('/api/v1/log/write', methods=['POST'])
def receive_json():
    content_encoding = request.headers.get('content-encoding', '')
    if content_encoding == 'gzip':
        buf = io.BytesIO(request.data)
        gf = gzip.GzipFile(fileobj=buf)
        content = json.loads(gf.read().decode('UTF-8'))
    else:
        content = request.json

    hits_list = json.loads("[" + content.get('context_hits') + "]")
    asyncio.run(tg_send(content.get('alert_id'), content.get('context_date'), content.get('context_value'), content.get('context_link'), log_handler(hits_list)))
    return jsonify({"message": "JSON received", "data": content})

if __name__ == '__main__':
    app.run()