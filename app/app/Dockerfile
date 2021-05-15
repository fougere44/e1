FROM python:3.7.2-stretch

ENV FLASK_APP run.py

WORKDIR /app

COPY run.py gunicorn-cfg.py requirements.txt config.py .env ./
COPY app app

ADD . /app

RUN pip install -r requirements.txt

#CMD ['uwsgi', "app.ini"]

EXPOSE 5005
CMD ["gunicorn", "--config", "gunicorn-cfg.py", "run:app"]