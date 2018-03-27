#--------- Generic stuff all our Dockerfiles should start with so we get caching ------------
# Note this base image is based on debian
FROM python:3.6
MAINTAINER Dimas Ciputra<dimas@kartoza.com>

RUN export DEBIAN_FRONTEND=noninteractive
ENV DEBIAN_FRONTEND noninteractive
RUN dpkg-divert --local --rename --add /sbin/initctl

RUN apt-get update -y

RUN apt-get install -y python3-pip \
    python-gdal \
    python-geoip \
    python3-setuptools

ADD REQUIREMENTS.txt /REQUIREMENTS.txt
RUN pip install -r /REQUIREMENTS.txt
RUN pip install uwsgi

ADD uwsgi.conf /uwsgi.conf

# Open port 8080 as we will be running our uwsgi socket on that
EXPOSE 8080

#USER www-data
WORKDIR /home/web/django_project

CMD ["uwsgi", "--ini", "/uwsgi.conf"]
