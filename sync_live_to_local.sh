#!/bin/bash
source venv/bin/activate
fab -H linfiniti3 get_live_db get_live_media
fab -H localhost restore_postgres_dump:changelog
deactivate
