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
python interpreter found therein. Newer versions of PyCharm have 'native' docker support
but after testing we opted to continue to use the ssh method described here. You may want to
test when new versions of PyCharm come out in case they have improved the direct docker support.

**Note:** You don't need to use this architecture, you can deploy as a standard
django app using virtualenv and locally installed postgis, nginx etc.

## Setup pycharm to work with a remove docker development environment

### Build and run your dev docker image

This image extends the production one, adding ssh to it. You must
have built the production one first by following the "Quick Installation Guide"!
When it's done, you can continue with this command:

Linux and MacOS:

```
cp docker-compose.override.example.yml docker-compose.override.yml
make build-devweb
make devweb
```

In case you don't get some not installed packages, you can run this 
repeatable steps:

1. Close PyCharm
2. `make kill` or `docker-compose -p projecta kill`
3. `make rm` or `docker-compose -p projecta rm`
4. `make build`
5. `make build-devweb`
6. `make devweb`
7. start PyCharm

> If you're not using remote interpreter in PyCharm, skip step `7` and run: `make devweb-runserver` to runserver in devweb container

Windows:

```
copy docker-compose.override.example.yml docker-compose.override.yml
make-devbuild.bat
make-devweb.bat
```


> Run test before you commit your modified files:
>
> `make test`
>
> or you can run test individually:
>
> `make flake8`
>
> `make coverage'

### Create a remote interpreter in pycharm

Open the project in pycharm then do:

* File -> Settings
* Project Interpreter
* Click on the gear icon next to project interpreter
* Add remote...

Now use these credentials:

* SSH Credentials (tick)
* Host: localhost
* Port: (use the ssh port specified in the docker-compose.yml file)
* User name: root
* Auth type: password (and tick 'save password')
* Password: docker
* Python interpreter path: ``/usr/local/bin/python``

When prompted about host authenticity, click Yes.
After the python interpreter is set, set its path mapping:

  * **Local path:** `<path to your git repo>/django_project`
  * **Remote path:** `/home/web/django_project`

After that you should see something like this:
   `<Project root>/django_project→/home/web/django_project`

In settings, django support:

* tick to enable django support.
* Set django project root to the path on your host that holds django code e.g.
  ``<path to code base>/django_project``
* Set the settings option to your setting profile e.g.
  ``core/settings/dev_docker.py``. If you need to use custom settings, copy
  this file e.g. ``dev_docker_tim.py`` and place your modifications in your
  personalised copy. The first import of your custom file should import from
  dev_docker.

* manage script (leave default)


### Create the django run configuration

* Run -> Edit configurations
* Click the `+` icon in the top left corner
* Choose ``Django server`` from the popup list

Now set these options:

* **Name:** Django Server
* **Host:** 0.0.0.0
* **Port:** (use the http port specified in the docker-compose.yml file, e.g. 8080)
* **Run browser** If checked, it will open the url after you click run. You should be able to access the running projecta on 0.0.0.0:61202 (the port that mapped to 8080)
* **Additional options:** ``--settings=core.settings.dev_docker``
* **Run browser:** Optionally set this to your IP address (MacOS/Linux) or your specific IP address (Windows) followed by the port forward address for port 8080 specified in your ``docker-compose.yml`` file. For example: ``http://0.0.0.0:61202``.
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

I made a general overview screencast describing this process here:

[![YouTube Screencast](http://img.youtube.com/vi/n-wwp17MqhU/0.jpg)](https://www.youtube.com/watch?v=n-wwp17MqhU "YouTube Screencast")


## Running Tests

Tim write stuff here....


## Setup Github OAuth
To configure OAuth application on Github, go to [https://github.com/settings/developers](https://github.com/settings/developers) and click on your project or create a new project at [https://github.com/settings/applications/new](https://github.com/settings/applications/new)

It is mandatory to fill out Application Name, Homepage URL, and Authorization callback URL:
- **Application Name**: changelog.kartoza.com
- **Homepage URL**: https://changelog.kartoza.com
- **Authorization callback URL**: https://changelog.kartoza.com/accounts/github/login/callback/ 

  ![image (1)](https://user-images.githubusercontent.com/40058076/103614680-2a4dd580-4f64-11eb-8dca-0466f17a5849.png)



Click the `Update application` button and generate Client secret by click on `Generate a new client secret` button.

![image (3)](https://user-images.githubusercontent.com/40058076/103614687-2d48c600-4f64-11eb-85b7-f6145db9f139.png)



Now you have `Client ID` and `Client Secret`

![image (2)](https://user-images.githubusercontent.com/40058076/103614683-2b7f0280-4f64-11eb-9010-ddbc378bafe8.png)



Go to django admin site: Home > Sites > Sites, and click on `Add Site` button:
- **Domain name**: changelog.kartoza.com
- **Display name**: changelog.kartoza.com

  ![doc_001](https://user-images.githubusercontent.com/40058076/103616775-04c2cb00-4f68-11eb-9fd3-0eef6569f92c.png)



Go to django admin site: Home > Social Accounts > Social applications and `Add social application` button:
- **Provider**: Github
- **Name**: https://changelog.kartoza.com
- **Client id**: your `Client ID`
- **Secret key**: your `Client secret`
- **Choosen sites**: changelog.kartoza.com

  ![doc_002](https://user-images.githubusercontent.com/40058076/103617160-b530cf00-4f68-11eb-9d97-0dfbcf4e6536.png)



Go to your website, login with Github and you'll be redirected to the Github authorize page.

![image (4)](https://user-images.githubusercontent.com/40058076/103614651-17d39c00-4f64-11eb-97b7-6181133e4c86.png)


## Developer FAQ

**Q**: I get ``ImportError: Could not import settings core.settings.dev_docker``
when starting the server.

**A:** ``django_project/core/settings/secret.py is either corrupt or you don't
have permissions to read it as the user you are running ``runserver`` as. A
common cause of this is if you are running the server in both production
mode and developer mode on the same host. Simply remove the file or change
ownership permissions so that you can read/write it.
