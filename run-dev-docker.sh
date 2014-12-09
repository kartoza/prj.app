#!/bin/sh

# Run the postgis instance - the image must already
# have the projecta postgis db restored to it.
docker kill projecta-postgis
docker rm projecta-postgis
docker run --name="projecta-postgis" \
     --hostname="projecta-postgis" \
     --restart="always" \
     -d -t \
     kartoza/projecta-postgis /start-postgis.sh

# Run the projecta development environment
# See https://github.com/kartoza/projecta/wiki/Development-environment-in-docker
# for more info
docker kill projecta-django
docker rm projecta-django
docker run --name="projecta-django" \
    --hostname="projecta-django" \
    --link projecta-postgis:projecta-postgis \
    -p 8001:22 -p 8000:8000 \
    -v `pwd`/django_project:/home/web/projecta/django_project \
    --restart="always" \
    -d -t \
    kartoza/projecta-django
