#!/bin/sh
cd ../../
docker build -t kartoza/projecta-uwsgi -f deployment/docker/Dockerfile .
