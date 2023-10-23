FROM python:3.10.10

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir --upgrade -r requirements.txt

COPY . .

ENTRYPOINT gunicorn -w 1 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:5000 app:app

# docker build -t fastapi .
# docker run -p 5000:5000 fastapi