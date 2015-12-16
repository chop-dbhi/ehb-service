#!/bin/sh

cd /opt/app

python ./bin/manage.py syncdb --noinput
python ./bin/manage.py migrate --noinput
python ./bin/manage.py collectstatic --noinput

if [ "$(ls -A /opt/app)" ]; then
    if [ "$FORCE_SCRIPT_NAME" = "" ]; then
	exec /usr/local/bin/uwsgi --chdir /opt/app/ --die-on-term --http-socket 0.0.0.0:8000 -p 2 -b 32768 -T --master --max-requests 5000 --static-map $FORCE_SCRIPT_NAME/static=/opt/app/_site/static --static-map /static=/usr/local/lib/python2.7/site-packages/django/contrib/admin/static --module wsgi:application
    else
        exec /usr/local/bin/uwsgi --chdir /opt/app/ --die-on-term --uwsgi-socket 0.0.0.0:8000 -p 2 -b 32768 -T --master --max-requests 5000 --static-map $FORCE_SCRIPT_NAME/static=/opt/app/_site/static --static-map /static=/usr/local/lib/python2.7/site-packages/django/contrib/admin/static --module wsgi:application
    fi
fi
