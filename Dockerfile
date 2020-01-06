FROM python:3.7-alpine

RUN apk add openssl

COPY requirements.txt /

RUN pip install -r /requirements.txt

COPY app/ app/

WORKDIR /app

RUN openssl req -x509 -newkey rsa:2048 -nodes -out cert.pem -keyout key.pem -days 3650 \
     -subj "/C=NZ/ST=North Island/L=Wellington/O=NLS Systems./OU=DEVOP/CN=localhost"

CMD [ "gunicorn", \
    "--certfile", "cert.pem", \
    "--keyfile", "key.pem", \
    "--workers=4", \
    "--timeout=120", \
    "--access-logfile", "-", \
    "--bind", "0.0.0.0:8080", \
    "--access-logformat", "%({X-Forwarded-For}i)s %(l)s %(u)s %(t)s \"%(r)s\" %(s)s %(b)s \"%(f)s\" \"%(a)s\" %(L)s", \
    "wsgi:app" \
    ]