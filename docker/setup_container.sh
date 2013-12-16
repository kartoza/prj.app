#!/bin/bash

# Why not use a dockerfile for everything?
# Because I prefer to set up the container using fabgis. And we want to
# avoid 42 layer limit.

# Add the docker group if it doesn't already exist.
sudo groupadd docker

# Add the connected user "${USERNAME}" to the docker group.
# Change the user name to match your preferred user.
# You may have to logout and log back in again for
# this to take effect.
sudo gpasswd -a ${USERNAME} docker

# Restart the docker daemon.
sudo service docker restart

# Ready to use container for postgis
sudo mkdir -p /var/docker/volumes/postgres_data
sudo docker pull helmi03/docker-postgis
sudo docker run -d \
    -v /var/docker/volumes/postgres_data:/var/lib/postgresql \
    -name postgis \
    helmi03/docker-postgis
POSTGIS_IP=$(sudo docker inspect postgis | grep IPAddress | grep -o "[0-9\.]*")

# Setup dir for storing docker shared volume for apt-cache
sudo mkdir -p /var/docker/volumes/apt-cache/
cp ~/.ssh/id_dsa.pub .
sudo docker build -t linfiniti/projecta .
sudo docker run -d \
    -v /var/docker/volumes/apt-cache/:/var/cache \
    -t linfiniti/projecta \
    -name "projecta" \
    supervisord -n
ssh root@localhost -p 7222 "chown -R wsgi.wsgi /home/web"
PROJECTA_IP=$(sudo docker inspect projecta | grep IPAddress | grep -o "[0-9\.]*")


cd ..
fab -H root@$PROJECTA_IP:7222 deploy
