# Developer Documentation

**Note:** This documentation is intentionally generic so that it can
be copy-pasted between projects - do not put project specific details here.

## Application architecture under docker

The following diagram provides and overview of the core architecture
components (Database, uwsgi server, web server):

![dockerdjangoarchitecture - new page 1](https://cloud.githubusercontent.com/assets/178003/5024388/750b85c8-6b12-11e4-97b0-c73b2d07e539.png)


The blue box is there to provide a means to develop on the same environment
as you deploy and would not be relevant for server side deployments.
Everything is managed using docker containers, with pycharm
making ssh connections into the developer container and using the
python interpreter found therein.

**Note:** You don't need to use this architecture, you can deploy as a standard
django app using virtualenv and locally installed postgis, nginx etc.

## Setup pycharm to work with a remove docker development environment

### Build and run your dev docker image

This image extends the production one, adding ssh to it. You must
have built the production one first!

```
make dev
```

### Create a remote interpreter in pycharm

Open the project in pycharm then do:

* File -> Settings
* Project Interpreter
* Click on the gear icon next to project interpreter
* Add remote...

Now use these credentials:

* SSH Credentials (tick)
* Host: localhost
* Port: (use the ssh port specified in the fig-dev.yml file)
* User name: root
* Auth type: password (and tick 'save password')
* Password: docker
* Python interpreter path: ``/usr/local/bin/python``

When prompted about host authenticity, click Yes

In settings, django support:

* tick to enable django support.
* Set django project root to the path on your host that holds django code e.g.
  ``<path to code base>/django_project``
* Set the settings option to your setting profile e.g.
  ``core/settings/dev_docker.py``
* manage script (leave default)


### Create the django run configuration

* Run -> Edit configurations
* Click the green + icon in the top left corner
* Choose ``Django server`` from the popup list

Now set these options:

* **Name:** Django Server
* **Host:** 0.0.0.0
* **Port:** (use the http port specified in the fig-dev.yml file)
* **Additional options:** ``--settings=core.settings.dev_docker``
* **Environment vars:** Leave as default unless you need to add something to the env
* **Python interpreter:** Ensure it is set you your remote interpreter (should be
  set to that by default)
* **Interpreter options:** Leave blank
* **Path mappings:** Here you need to indicate path equivalency between your host
  filesystem and the filesystem in the remote (docker) host. Click the ellipsis
  and add a run that points to your git checkout on your local host and the
  /home/web directory in the docker host. e.g.
  * **Local path:** <path to your git repo>/django_project
  * **Remote path:** /home/web/django_project
* click OK to save your run configuration

Now you can run the server using the green triangle next to the Django server
label in the run configurations pull down. Debug will also work and you will be
able to step through views etc as you work.


## Developer FAQ

**Q**: I get ``ImportError: Could not import settings core.settings.dev_docker``
when starting the server.

**A:** ``django_project/core/settings/secret.py is either corrupt or you don't
have permissions to read it as the user you are running ``runserver`` as. A
common cause of this is if you are running the server in both production
mode and developer mode on the same host. Simply remove the file or change
ownership permissions so that you can read/write it.


