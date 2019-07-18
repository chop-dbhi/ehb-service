FROM alpine:3.3

RUN apk add --update \
    bash \
    postgresql-dev \
    gcc \
    python3 \
    python3-dev \
    build-base \
    git \
    openldap-dev \
    linux-headers \
    pcre-dev \
    musl-dev \
    postgresql-dev \
    mailcap \
    vim \
  && rm -rf /var/cache/apk/* && \
  python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    rm -r /root/.cache &&\
    apk upgrade


ENV APP_NAME ehbservice
ENV APP_ENV test
RUN mkdir -p /opt/app/
ADD . /opt/app

RUN pip3 install -r /opt/app/requirements.txt

ADD test.env_example /opt/app/test.env

WORKDIR /opt/app/

RUN pip install -r /opt/app/requirements.txt

CMD "/opt/app/scripts/run.sh"

EXPOSE 8000
