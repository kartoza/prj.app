FROM ubuntu:latest
MAINTAINER tim@linfiniti.com
RUN  export DEBIAN_FRONTEND=noninteractive
ENV  DEBIAN_FRONTEND noninteractive
RUN  dpkg-divert --local --rename --add /sbin/initctl
RUN  ln -s /bin/true /sbin/initctl
RUN echo "deb http://archive.ubuntu.com/ubuntu precise main universe" > /etc/apt/sources.list
RUN apt-get update
# Set up apt-cacher - make sure to use a shared volume for the cache in the
# container when you run it. See:
# https://gist.github.com/fairchild/7309068
RUN apt-get update && apt-get install -y apt-cacher-ng
# Run it temporarily in daemon mode while running this build process
RUN apt-cacher-ng
RUN echo "Acquire::http { Proxy \"http://192.168.1.12:3142\"; };"| tee -a /etc/apt/apt.conf.d/01proxy
RUN apt-get upgrade -y
RUN apt-get install -y --force-yes openssh-server apache2 supervisor lsb-release sudo
# Set the root password to 'projecta'
RUN echo "root:projecta" | chpasswd
RUN mkdir -p /var/run/sshd
RUN mkdir -p /var/log/supervisor
ADD supervisor-ssh.conf /etc/supervisor/conf.d/supervisor-ssh.conf
ADD supervisor-apt-cacher.conf /etc/supervisor/conf.d/supervisor-apt-cacher.conf
ADD supervisor-apache.conf /etc/supervisor/conf.d/supervisor-apache.conf
RUN mkdir ~/.ssh
RUN chmod og-rwX ~/.ssh
ADD id_dsa.pub ~/.ssh/authorized_keys
# Change apt-cache setup to use shared volume
# Todo: Make this generic
RUN echo "Acquire::http { Proxy \"http://192.168.1.12:3142\"; };"| tee -a /etc/apt/apt.conf.d/01proxy
CMD ["/usr/bin/supervisord -n"]
