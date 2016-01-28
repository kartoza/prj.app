# Managing your docker deployed site

**Note:** This documentation is intentionally generic so that it can
be copy-pasted between projects - do not put project specific details here.

This document explains how to do various sysadmin related tasks when your
site has been deployed under docker. Three deployment modes are supported:

* **production**: no debug etc is enabled, has its own discrete database. Configure
  your production environment in core.settings.prod_docker - this
  DJANGO_SETTINGS_MODULE is used when running in production mode.
* **development**: Configure your development environment in core.settings.dev_docker -
  this DJANGO_SETTINGS_MODULE is used when running in production mode. Please see
  README-dev.md for more information on setting up a developer environment.

**Note:** We really recommend that you use docker 1.8 or greatr so that you
  can take advantage of the exec command as well as other newer features.

## Build your docker images and run them

### Production

You can simply run the provided Makefile commands and it will build and deploy the docker
images for you in **production mode**.

```
cd deployment
make build
make run
make migrate migrate
make collectstatic
```

#### Using make

Using the make commands is probably simpler - the following make commands are
provided for production:


* **run** - builds then runs db and uwsgi services
* **web** - run django uwsgi instance (will bring up db too if needed)
* **collectstatic** - collect static in production instance
* **migrate** - run django migrations in production instance
* **build** - build production containers
* **deploy** - run db, web, wait 20 seconds, collect static and do migrations
* **rm** - completely remove staging from your system (use with caution)

e.g. ``make web``

#### Arbitrary commands

Running arbitrary management commands is easy (assuming you have docker >= 1.3)
e.g.:

```
docker exec foo_web_1 /usr/local/bin/python /home/web/django_project/manage.py --help
```

**Note:** rm should not destroy any data since it only removes containers
and not host volumes for db and django. All commands should be non-destructive
to existing data - though **smart people make backups before changing things**.


## Setup nginx reverse proxy

You should create a new nginx virtual host - please see
``*-nginx.conf`` in the deployment directory of the source for an example.

Simply add the example file (symlinking is best) to your ``/etc/nginx/sites-enabled/`` directory
and then modify the contents to match your domain. Then use

```
sudo nginx -t
```

To verify that your configuration is correct and then reload / restart nginx
e.g.

```
sudo /etc/init.d/nginx restart
```

# Configuration options

You can configure the base port used and various other options like the
image organisation namespace and postgis user/pass by editing the ``docker-compose.yml``
files.
