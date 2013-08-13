
Visual Change Logger
====================

A simple app to allow community edited visual changelogs for software releases.

Some notes:
-----------

User authentication is via userena. I copied the userena templates into
accounts/templates and then used django-widget-tweaks to add extrac
bootstrap css to them so that the forms look nice.

To install do::

    virtualenv venv
    source venv/bin/activate
    pip install -r REQUIREMENTS-dev.txt
    cd django-project
    fab -H <hostname> deploy

Look in the fabfile.py for other available tasks if you do not wish to do a
full deployment.

I'm only using the sqlite backend so there should be no need to configure a
database.


Tim Sutton, August 2013
