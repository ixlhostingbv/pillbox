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
ARG URL=https://github.com/digitalocean/netbox/archive/$BRANCH.tar.gz
RUN wget -q -O - "${URL}" | tar xz \
  && mv netbox* netbox

WORKDIR /opt/netbox
RUN pip install -r requirements.txt
