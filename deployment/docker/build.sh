#!/bin/sh
pushd ../../
docker build -t kartoza/projecta-uwsgi -f deployment/docker/Dockerfile --target prod .
popd
