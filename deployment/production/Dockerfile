#--------- Generic stuff all our Dockerfiles should start with so we get caching ------------
# Note this base image is based on debian
FROM kartoza/django-base:3.7
MAINTAINER Tim Sutton<tim@kartoza.com>

#RUN  ln -s /bin/true /sbin/initctl

# Pandoc needed to generate rst dumps, uic compressor needed for django-pipeline
RUN apt-get update -y; apt-get -y --force-yes install yui-compressor gettext
RUN wget https://github.com/jgm/pandoc/releases/download/1.17.1/pandoc-1.17.1-2-amd64.deb
RUN dpkg -i pandoc-1.17.1-2-amd64.deb && rm pandoc-1.17.1-2-amd64.deb

ARG BRANCH_TAG=develop
RUN mkdir -p /usr/src; mkdir -p /home/web && \
            git clone --depth=1 git://github.com/kartoza/prj.app.git --branch ${BRANCH_TAG} /usr/src/projecta/ && \
            rm -rf /home/web/django_project && \
	        ln -s /usr/src/projecta/django_project /home/web/django_project

RUN cd /usr/src/projecta/deployment/docker && \
	pip install -r REQUIREMENTS.txt && \
	pip install uwsgi && \
	rm -rf /uwsgi.conf && \
	ln -s ${PWD}/uwsgi.conf /uwsgi.conf

# Open port 8080 as we will be running our uwsgi socket on that
EXPOSE 8080

#USER www-data

WORKDIR /home/web/django_project
CMD ["uwsgi", "--ini", "/uwsgi.conf"]
