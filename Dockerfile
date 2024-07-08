FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# RUN mkdir /chatapp

WORKDIR /chatapp


RUN apt-get update \
    && apt-get install -y gcc python3-dev musl-dev libmagic1 libffi-dev netcat-traditional \
    && pip install Pillow

# Install dependencies
COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ADD . /chatapp/

# CMD gunicorn core.wsgi:application --bind 0.0.0.0:$PORT
# CMD daphne core.asgi:application
CMD daphne -b 0.0.0.0 core.asgi:application