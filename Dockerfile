FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt --no-cache-dir
RUN pip3 install gunicorn==21.2.0
COPY . .
EXPOSE 8000
CMD ["gunicorn", "--config=gunicorn.conf.py", "app:app"]