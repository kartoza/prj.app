SHELL := /bin/bash

default: web

run: build web

deploy: run
	@echo
	@echo "--------------------------"
	@echo "Brining up fresh instance "
	@echo "--------------------------"
	@fig run -p projecta uwsgi python manage.py migrate
	#@run -p projecta uwsgi python manage.py collectstatic --noinput
	#We need to run collect static in the same context as the running
	# uwsgi container it seems so I use docker exec here
	@docker exec -t -i projecta_uwsgi_1 python manage.py collectstatic --noinput

rm:
	@echo
	@echo "--------------------------"
	@echo "Killing production instance!!! "
	@echo "--------------------------"
	@fig  -p projecta kill
	@fig  -p projecta rm

web:
	@echo
	@echo "--------------------------"
	@echo "Running in production mode"
	@echo "--------------------------"
	@fig  -p projecta up -d web
	@dipall

sentry:
	@echo
	@echo "--------------------------"
	@echo "Running sentry production mode"
	@echo "--------------------------"
	@fig  -p projecta up -d sentry
	@dipall


build:
	@echo
	@echo "--------------------------"
	@echo "Building in production mode"
	@echo "--------------------------"
	@fig  -p projecta build

migrate:
	@echo
	@echo "--------------------------"
	@echo "Running migrate static in production mode"
	@echo "--------------------------"
	@fig -p projecta run uwsgi python manage.py migrate

collectstatic:
	@echo
	@echo "--------------------------"
	@echo "Collecting static in production mode"
	@echo "--------------------------"
	#@fig -p projecta run uwsgi python manage.py collectstatic --noinput
	#We need to run collect static in the same context as the running
	# uwsgi container it seems so I use docker exec here
	@docker exec -t -i projecta_uwsgi_1 python manage.py collectstatic --noinput

kill:
	@echo
	@echo "--------------------------"
	@echo "Killing in production mode"
	@echo "--------------------------"
	@fig -p projecta kill

logs:
	@echo
	@echo "--------------------------"
	@echo "Showing uwsgi logs in production mode"
	@echo "--------------------------"
	@fig -p projecta logs uwsgi

nginxlogs:
	@echo
	@echo "--------------------------"
	@echo "Showing nginx logs in production mode"
	@echo "--------------------------"
	@fig -p projecta logs web

seed:
	@echo
	@echo "--------------------------"
	@echo "Seeding mapproxy in production mode"
	@echo "--------------------------"
	@fig -p projecta run mapproxy /usr/local/bin/mapproxy-seed -f /mapproxy/mapproxy.yaml /mapproxy/seed.yaml

shell:
	@echo
	@echo "--------------------------"
	@echo "Shelling in in production mode"
	@echo "--------------------------"
	@fig -p projecta run uwsgi /bin/bash

dbshell:
	@echo
	@echo "--------------------------"
	@echo "Shelling in in production database"
	@echo "--------------------------"
	@docker exec -t -i projecta_db_1 psql -U docker -h localhost gis

qgis:
	@echo
	@echo "--------------------------"
	@echo "Running QGIS desktop in production mode"
	@echo "Make sure you have started the services with make run first"
	@echo "--------------------------"
	@xhost +; docker run --rm --name="qgis-desktop-2-4" \
	-i -t \
	--link projecta_db_1:db \
	--link projecta_qgisserver_1:qgisserver \
	--link projecta_mapproxy_1:mapproxy \
	--volumes-from projecta_qgisserver_1 \
	-v ${HOME}:/home/$(USER) \
	-v /tmp/.X11-unix:/tmp/.X11-unix \
	-e DISPLAY=unix$(DISPLAY) \
	kartoza/qgis-desktop:latest; xhost -
