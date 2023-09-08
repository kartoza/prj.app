#--------- Generic stuff all our Dockerfiles should start with so we get caching ------------
# Note this base image is based on debian
FROM python:3.10 as prod
MAINTAINER Tim Sutton<tim@kartoza.com>

RUN  export DEBIAN_FRONTEND=noninteractive
ENV  DEBIAN_FRONTEND noninteractive
RUN  dpkg-divert --local --rename --add /sbin/initctl

# Pandoc needed to generate rst dumps, uic compressor needed for django-pipeline
RUN apt-get update -y && \
    apt-get -y install python3-gdal python3-geoip sudo curl rpl && \
    apt-get -y --force-yes install yui-compressor gettext && \
    apt-get -y --purge autoremove make libc-dev musl-dev g++ && \
    apt-get install -y nodejs npm && \
    npm install -g yuglify && \
    apt-get remove -y npm && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/* /root/.npm /root/.cache && \
    rm -rf ~/.cache/pip
RUN wget https://github.com/jgm/pandoc/releases/download/1.17.1/pandoc-1.17.1-2-amd64.deb
RUN dpkg -i pandoc-1.17.1-2-amd64.deb && rm pandoc-1.17.1-2-amd64.deb

# Added because of issue with building cryptography.io using pip
# This flag disabled rust build, but only for this particular version
# In the future, we may have to include rust toolchain in the Dockerfile
ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1

ADD deployment/docker/REQUIREMENTS.txt /REQUIREMENTS.txt
ADD deployment/docker/uwsgi.conf /uwsgi.conf
ADD django_project /home/web/django_project
RUN pip install --upgrade pip && pip install -r /REQUIREMENTS.txt
RUN pip install uwsgi


# Open port 8080 as we will be running our uwsgi socket on that
EXPOSE 8080

#USER www-data

WORKDIR /home/web/django_project
CMD ["uwsgi", "--ini", "/uwsgi.conf"]

FROM prod as dev

# This section taken on 2 July 2015 from
# https://docs.docker.com/examples/running_ssh_service/
# Sudo is needed by pycharm when it tries to pip install packages
RUN apt-get update && apt-get install -y openssh-server sudo
RUN mkdir /var/run/sshd
RUN echo 'root:docker' | chpasswd
RUN echo "PermitRootLogin yes" >> /etc/ssh/sshd_config


# SSH login fix. Otherwise user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile

# End of cut & paste section

ADD deployment/docker/REQUIREMENTS-dev.txt /REQUIREMENTS-dev.txt
RUN pip install --upgrade pip && pip install -r /REQUIREMENTS-dev.txt
ADD deployment/docker/bashrc /root/.bashrc

# --------------------------------------------------------
# Open ports as needed
# --------------------------------------------------------

# Open port 8080 as we will be running our django dev server on
EXPOSE 8080
# Open port 22 as we will be using a remote interpreter from pycharm
EXPOSE 22

CMD ["/usr/sbin/sshd", "-D"]
