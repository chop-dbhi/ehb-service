
FROM python:2.7.14

MAINTAINER Tyler Rivera <riverat2@email.chop.edu>

RUN apt-get update -qq --fix-missing
RUN apt-get install -y\
    build-essential\
    git-core\
    libldap2-dev\
    libpq-dev\
    libsasl2-dev\
    libssl-dev\
    libxml2-dev\
    libxslt1-dev\
    libffi-dev\
    openssl\
    python-dev\
    python-setuptools\
    wget\
    zlib1g-dev\
    postgresql-client

RUN pip install "Django==1.11.16"
RUN pip install uWSGI
RUN pip install "django-environ==0.4.1"

RUN pip install "djangorestframework==3.8.2"
RUN pip install psycopg2-binary==2.7.5
RUN pip install python-ldap
RUN pip install "pycrypto==2.3"
RUN pip install mock
RUN pip install django-redis-sessions
RUN pip install "tzlocal==1.5.1"

RUN mkdir /opt/app

ENV APP_NAME ehbservice
ENV APP_ENV test

ADD . /opt/app
ADD test.env_example /opt/app/test.env

WORKDIR /opt/app/

RUN pip install -r /opt/app/requirements.txt

CMD "/opt/app/scripts/run.sh"

EXPOSE 8000
