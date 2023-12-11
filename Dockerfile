

FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /chatapp

WORKDIR /chatapp

ADD . /chatapp/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# CMD gunicorn core.wsgi:application --bind 0.0.0.0:$PORT
CMD daphne core.asgi:application --bind 0.0.0.0:$PORT