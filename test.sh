
DEBUG=1
SECRET_KEY="test"
DATABASE_URL=sqlite:///ehb_service.db

EMAIL_HOST=localhost
EMAIL_PORT=25
EMAIL_DOMAIN=example.com

EHB_USE_ENCRYPTION=0
EHB_KMS_SECRET="secretsecret"
EHB_CLIENT_KEY_SEED=1
EHB_GROUP_KEY_SEED=1

./bin/manage.py syncdb --noinput
./bin/manage.py migrate --noinput
./bin/manage.py test api core
