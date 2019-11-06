#!/bin/bash
export APP_ENV=test
export DEBUG=1
export SECRET_KEY="test"
export DATABASE_URL=sqlite:///ehb_service.db
export ALLOWED_HOSTS=localhost
export REDIS_HOST=
export REDIS_PORT=

export EMAIL_HOST=localhost
export EMAIL_PORT=25
export EMAIL_DOMAIN=example.com

export EHB_USE_ENCRYPTION=1
export EHB_KMS_SECRET=ZAXxDHJAqyMfVR3sLjydxjjhgkgyZM7J
export EHB_CLIENT_KEY_SEED=782399698
export EHB_GROUP_KEY_SEED=477397326

export LDAP_DEBUG=0
export LDAP_PREBINDDN=
export LDAP_SEARCHDN=
export LDAP_SEARCH_FILTER=
export LDAP_SERVER_URI=
export LDAP_PREBINDPW=

./bin/manage.py syncdb --noinput
./bin/manage.py migrate --noinput
./bin/manage.py test api core
