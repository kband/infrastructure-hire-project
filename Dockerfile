FROM python:3.7-alpine

COPY requirements.txt /

RUN pip install -r /requirements.txt

COPY app/ app/

WORKDIR /app

CMD [ "gunicorn", \
    "--access-logfile", "-", \
    "--bind", "0.0.0.0:8080", \
    "--access-logformat", "%({X-Forwarded-For}i)s %(l)s %(u)s %(t)s \"%(r)s\" %(s)s %(b)s \"%(f)s\" \"%(a)s\" %(L)s", \
    "wsgi:app" \
    ]