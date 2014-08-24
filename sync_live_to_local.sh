#!/bin/bash
source venv/bin/activate
fab -H kartoza2 get_live_db get_live_media
fab -H localhost restore_postgres_dump:changelog
python manage.py migrate --settings=core.settings.dev_timlinux
deactivate
