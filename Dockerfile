FROM python:3.6-alpine

RUN adduser -D microblog

WORKDIR /home/microblog

COPY requirements.txt requirements.txt
# RUN apk add --no-cache --virtual .pynacl_deps build-base python3-dev libffi-dev
RUN python -m venv env
RUN env/bin/pip install --upgrade pip
RUN env/bin/pip install --upgrade setuptools wheel
RUN env/bin/pip install -r requirements.txt
RUN env/bin/pip install gunicorn pymysql

COPY app app
COPY migrations migrations
COPY microblog.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP microblog.py

RUN chown -R microblog:microblog ./
USER microblog

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]