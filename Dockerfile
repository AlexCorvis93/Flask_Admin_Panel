
FROM python:3.8.10-slim-buster

WORKDIR /app

COPY ./requirements.txt /app
RUN pip install -r requirements.txt



ENV FLASK_APP=app.py
ENV FLASK_ENV="docker"
COPY . .
EXPOSE 5000


