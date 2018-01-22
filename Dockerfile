FROM python:3.6-alpine

RUN apk add --no-cache \
      bash \
      build-base \
      ca-certificates \
      cyrus-sasl-dev \
      openssl-dev \
      wget

RUN pip install gunicorn

WORKDIR /opt

ARG BRANCH=master
ARG URL=https://github.com/vvgelder/pillbox/archive/$BRANCH.tar.gz
RUN wget -q -O - "${URL}" | tar xz \
  && mv pillbox* pillbox

WORKDIR /opt/pillbox
RUN pip install -r requirements.txt

COPY docker/local_settings.py /opt/pillbox/local_settings.py
COPY docker/gunicorn_config.py /opt/pillbox
