FROM python:3.9.5-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY ./requirements.txt /app
RUN pip install -r requirements.txt


COPY . .
EXPOSE 5000

CMD ('python', 'app.py', 'run', '-h', '0.0.0.0')


