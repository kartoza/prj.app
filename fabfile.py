#!/bin/python
# coding=utf-8
"""Fabfile for changelog app."""
# ~/fabfile.py
# A Fabric file for carrying out various administrative tasks.
# Tim Sutton, Jan 2013

# To use this script make sure you have fabric and fabtools.
# pip install fabric fabtools

import os
import getpass

# noinspection PyUnresolvedReferences,PyPackageRequirements
from fabric.api import (
    task, env, fastprint, cd, run, sudo, local, prompt, put, get)
from fabric.decorators import hosts
from fabric.contrib.files import exists
# noinspection PyUnresolvedReferences,PyPackageRequirements
from fabric.contrib.project import rsync_project
# noinspection PyUnresolvedReferences,PyPackageRequirements
from fabric.contrib.files import exists, sed
# noinspection PyUnresolvedReferences,PyPackageRequirements
from fabric.colors import red, blue, green
# noinspection PyUnresolvedReferences,PyPackageRequirements
from fabtools import require
# noinspection PyUnresolvedReferences,PyPackageRequirements
from fabtools.deb import update_index
# noinspection PyUnresolvedReferences,PyPackageRequirements
from fabtools.postgres import (
    database_exists,
    create_database,
    create_user,
    user_exists
)
# Don't remove even though its unused
# noinspection PyUnresolvedReferences,PyPackageRequirements
from fabtools.vagrant import vagrant

# noinspection PyUnresolvedReferences,PyPackageRequirements
from fabgis.dropbox import setup_dropbox, setup_dropbox_daemon
# noinspection PyUnresolvedReferences,PyPackageRequirements
from fabgis.django import setup_apache, build_pil, set_media_permissions
# noinspection PyUnresolvedReferences,PyPackageRequirements
from fabgis.git import update_git_checkout
# noinspection PyUnresolvedReferences,PyPackageRequirements
from fabgis.virtualenv import setup_venv
# noinspection PyUnresolvedReferences,PyPackageRequirements
from fabgis.common import setup_env, show_environment
# noinspection PyUnresolvedReferences,PyPackageRequirements
from fabgis.postgres import (
    create_user,
    get_postgres_dump,
    restore_postgres_dump,
    setup_postgis_2,
    create_postgis_2_template)


def get_vars():
    """Helper method to get standard deployment vars.

    :returns: A tuple containing the following:
        * base_path: Workspace dir e.g. ``/home/foo/python``
        * code_path: Project dir e.g. ``/home/foo/python/projecta``
        * git_url: Url for git checkout - use http for read only checkout
        * repo_alias: Name of checkout folder e.g. ``projecta``
        * site_name: Name for the web site e.g. ``projecta``

    :rtype: tuple
    """
    setup_env()
    site_name = 'projecta'
    base_path = '/home/web/'
    git_url = 'http://github.com/timlinux/projecta.git'
    repo_alias = 'projecta'
    code_path = os.path.abspath(os.path.join(base_path, repo_alias))
    return base_path, code_path, git_url, repo_alias, site_name


@task
def update_venv(code_path):
    """Update the virtual environment to ensure it has node etc. installed.

    :param code_path: Directory in which project is located.
    :type code_path: str

    e.g.::

        fab -H localhost update_venv:/home/timlinux/dev/python/projecta
    """
    setup_venv(code_path, requirements_file='REQUIREMENTS.txt')
    #yuglify needed by django-compress needs to have node installed which
    # is provided by virtual-node in the REQUIREMENTS file above,
    # but we still need to install yuglify manually since we cant add it
    # using REQUIREMENTS.
    # See also https://github.com/elbaschid/virtual-node
    # for more info on how virtualnode works
    with cd(code_path):
        run('venv/bin/npm -g install yuglify')
    build_pil(code_path)


@task
def setup_postgres_user():
    """Set up the postgresql instance."""
    create_user('wsgi', '')


@task
def upload_postgres_dump(dump_path):
    """Upload the dump found in dump_path and restore it to the server.

    .. note existing data on the server will be destroyed.

    :param dump_path: Local file containing dump to be restored.
    :type dump_path; str
    """
    restore_postgres_dump(
        'changelog',
        user='wsgi',
        ignore_permissions=True,
        file_name=dump_path)


@task
def update_apache(code_path):
    """Update the apache configuration prompting for github account info.

    .. note:: The config file is taken from the local system.

    :param code_path: Usually '/home/web/<site_name>'

    """
    git_url = 'https://api.github.com/repos/timlinux/projecta/issues'
    git_user = prompt(
        'Please enter the github user account that issues submitted via the\n'
        'web ui should be created as. This will be written into the apache\n'
        'configuration file under /etc/apache2/sites-available so you\n'
        'should take appropriate security measures.\nUser :\n')
    git_password = getpass.getpass()
    domain = 'changelog.kartoza.com'
    setup_apache(
        site_name='projecta',
        code_path=code_path,
        domain=domain,
        github_url=git_url,
        github_password=git_password,
        github_user=git_user)


@task
def deploy():
    """Initialise or update the git clone - you can safely rerun this.

    e.g. to update the server

    fab -H <host> deploy

    """
    # Ensure we have a mailserver setup for our domain
    # Note that you may have problems if you intend to run more than one
    # site from the same server
    setup_env()
    show_environment()
    setup_postgis_2()
    base_path, code_path, git_url, repo_alias, site_name = get_vars()

    fastprint('Checking out %s to %s as %s' % (git_url, base_path, repo_alias))
    update_git_checkout(base_path, git_url, repo_alias)
    update_index()
    require.postfix.server(site_name)
    update_apache(code_path)
    require.deb.package('python-dev')
    require.deb.package('libpq-dev')
    require.deb.package('libgeos-c1')
    require.deb.package('vim')
    require.deb.package('curl')
    require.deb.package('pandoc')
    update_venv(code_path)
    set_db_permissions()
    with cd(os.path.join(code_path, 'django_project')):
        run('../venv/bin/python manage.py syncdb --noinput ')
        run('../venv/bin/python manage.py migrate')
    # if we are testing under vagrant, deploy our local media and db
    #if 'vagrant' in env.fg.home:
    #    with cd(code_path):
    #        run('cp /vagrant/projecta.db .')
    #        run('touch django_project/core/wsgi.py')

    #sync_media_to_server()
    collectstatic()
    fastprint('*******************************************\n')
    fastprint(red(' Don\'t forget set ALLOWED_HOSTS in '))
    fastprint(' django_project/core/settings/prod.py')
    fastprint(' to the domain name for the site.')
    fastprint('*******************************************\n')


@hosts('kartoza3')
@task
def backup():
    """Make a local backup of the production instance."""
    get_live_media()  # should fetch from kartoza3
    get_private()  # should fetch from kartoza3
    get_live_db()  # should fetch from kartoza3

@hosts('kartoza3')
@task
def freshen():
    """Freshen the server with latest git copy and touch wsgi.

    .. note:: Preferred normal way of doing this is rather to use the
        sync_project_to_server task and not to checkout from git.

    """
    base_path, code_path, git_url, repo_alias, site_name = get_vars()
    git_url = 'http://github.com/timlinux/projecta.git'
    update_git_checkout(base_path, git_url, repo_alias)
    put_private()
    update_venv(code_path)
    update_migrations()
    with cd(os.path.join(code_path, 'django_project')):
        run('touch core/wsgi.py')
    collectstatic()

    fastprint('*******************************************\n')
    fastprint(red(' Don\'t forget set ALLOWED_HOSTS in \n'))
    fastprint(' django_project/core/settings/prod.py\n')
    fastprint(' to the domain name for the site.\n')
    fastprint('*******************************************\n')


# noinspection PyUnresolvedReferences
@task
def sync_media_to_server():
    """Sync media to server from local filesystem."""
    base_path, code_path, git_url, repo_alias, site_name = get_vars()
    remote_path = os.path.join(code_path, 'django_project', 'media')
    local_path = os.path.join(
        os.path.dirname(__file__), 'django_project', 'media/')
    rsync_project(
        remote_path,
        local_dir=local_path,
        exclude=['*.pyc', '*.py', '.DS_Store'])

    # Now our sqlite db
    remote_path = os.path.join(
        code_path, 'resources', 'sqlite', 'projecta.db')
    local_path = os.path.join(
        os.path.dirname(__file__), 'resources/sqlite/projecta.db')
    rsync_project(
        remote_path,
        local_dir=local_path,
        exclude=['*.pyc', '*.py', '.DS_Store'])
    set_media_permissions(code_path)
    set_db_permissions()


@task
def sync_project_to_server():
    """Synchronize project with webserver ignoring venv and sqlite db..
    This is a handy way to get your secret key to the server too...

    """
    base_path, code_path, git_url, repo_alias, site_name = get_vars()
    update_venv(code_path)
    #noinspection PyArgumentEqualDefault
    rsync_project(
        base_path,
        delete=False,
        exclude=[
            '*.pyc',
            '.git',
            '*.dmp',
            '.DS_Store',
            'projecta.db',
            'venv',
            'django_project/static'])
    update_migrations()
    with cd(os.path.join(code_path, 'django_project')):
        run('touch core/wsgi.py')
    set_media_permissions(code_path)
    set_db_permissions()
    update_migrations()
    collectstatic()
    fastprint(blue(
        'Your server is now in synchronised to your local project\n'))


@task
def server_to_debug_mode():
    """Put the server in debug mode (normally not recommended)."""
    base_path, code_path, git_url, repo_alias, site_name = get_vars()
    config_file = os.path.join(
        code_path, 'django_project', 'core', 'settings', 'project.py')
    sed(
        config_file,
        'DEBUG = TEMPLATE_DEBUG = False',
        'DEBUG = TEMPLATE_DEBUG = True')
    with cd(os.path.join(code_path, 'django_project')):
        run('touch core/wsgi.py')
    set_db_permissions()
    collectstatic()
    fastprint(red('Warning: your server is now in DEBUG mode!\n'))


@task
def server_to_production_mode():
    """Put the server in production mode (recommended)."""
    base_path, code_path, git_url, repo_alias, site_name = get_vars()
    config_file = os.path.join(
        code_path, 'django_project', 'core', 'settings', 'project.py')
    sed(
        config_file,
        'DEBUG = TEMPLATE_DEBUG = True',
        'DEBUG = TEMPLATE_DEBUG = False')
    with cd(os.path.join(code_path, 'django_project')):
        run('touch core/wsgi.py')
    set_db_permissions()
    collectstatic()
    fastprint(blue('Note: your server is now in PRODUCTION mode!\n'))


@task
def set_db_permissions():
    """Set the db so user wsgi has all permissions.
    """
    user = 'wsgi'
    dbname = 'changelog'
    if not user_exists(user):
        create_user(user, password='vagrant')
    if not database_exists(dbname):
        create_database(dbname, user)
    grant_sql = 'GRANT ALL ON schema public to %s;' % user
    # assumption is env.repo_alias is also database name
    run('psql %s -c "%s"' % (dbname, grant_sql))
    grant_sql = (
        'GRANT ALL ON ALL TABLES IN schema public to %s;' % user)
    # assumption is env.repo_alias is also database name
    run('psql %s -c "%s"' % (dbname, grant_sql))
    grant_sql = (
        'GRANT ALL ON ALL SEQUENCES IN schema public to %s;' % user)
    run('psql %s -c "%s"' % (dbname, grant_sql))


@hosts('kartoza3')
@task
def get_live_db():
    """Get the live db - will overwrite your local copy."""
    get_postgres_dump('changelog')


@hosts('kartoza3')
@task
def get_docker_live_db():
    """Get a copy of the db as deployed in docker on the remote host."""
    date = run('date +%d-%B-%Y')
    my_file = 'projecta-%s.dmp' % date
    ip = run("export PATH=$PATH:/home/timlinux/bin/docker-helpers/; dipall | grep projecta_db_1 | awk '{print $3}'")
    run(
        'export PGPASSWORD=docker; '
        'pg_dump -Fc -f /tmp/%s -h %s -U docker gis' % (my_file, ip))
    get('/tmp/%s' % my_file, my_file)

@hosts('kartoza3')
@task
def get_docker_live_media():
    """Get the live media - will overwrite your local copy."""
    local('rsync -ave ssh %s:/home/timlinux/production-sites/projecta/django_project/media deployment/media' % env['host_string'])


@hosts('kartoza3')
@task
def get_live_media():
    """Get the live media - will overwrite your local copy."""
    base_path, code_path, git_url, repo_alias, site_name = get_vars()
    path = '%s/django_project/media' % code_path
    local_path = os.path.join(
        os.path.dirname(__file__),'deployment', 'media')
    if not exists(local_path):
        run('mkdir -p %s' % local_path)
    local('rsync -ave ssh %s:%s/django_project/media/* %s'
          % (env['host_string'], code_path, local_path))


@task
def collectstatic():
    """Collect static using proper path for django-compressor / yuglify.

    .. note:: We are using python-node to run node in a virtual environment.
        Node is needed for yuglify, which is in turn needed by
        django-compressor which combines all js resources into a single file
        and all css into a single file. These are 'compiled' but yuglify.
        Yuglify does not appear in the path properly thus we explicitly
        ensure the path points to the node_modules dir before running
        collectstatic.

        All the above will prevent run time errors like:

        [Django] ERROR: Failed to submit message: u"ValueError: The file
        'css/contrib.css' could not be found with <pipeline.storage.
        PipelineCachedStorage object at 0x7f0df18b3ad0>."

    """
    command = ('PATH=$PATH:../node_modules/yuglify/bin/:../venv/bin/ '
               '../venv/bin/python manage.py collectstatic --noinput')
    base_path, code_path, git_url, repo_alias, site_name = get_vars()
    with cd(os.path.join(code_path, 'django_project')):
        run(command)


@task
def update_migrations():
    """Apply any pending south migrations.
    """
    command = '../venv/bin/python manage.py migrate'
    base_path, code_path, git_url, repo_alias, site_name = get_vars()
    with cd(os.path.join(code_path, 'django_project')):
        run(command)
        run('touch core/wsgi.py')
    fastprint(green('Note: your server is now has the latest SOUTH '
                    'migrations applied.\n'))


@task
def put_private():
    """Copy the private.py with site specific settings to the server."""

    base_path, code_path, git_url, repo_alias, site_name = get_vars()

    local_path = os.path.join(
        'django_project', 'core', 'settings', 'private.py')

    if not os.path.exists(local_path):
        fastprint(red('Please create your local copy of private.py\n'))
        fastprint(red('See README.md for more instructions.'))
        raise Exception('Could not copy local private settings to server')

    remote_path = os.path.join(code_path, local_path)

    put(local_path=local_path, remote_path=remote_path)


@hosts('kartoza3')
@task
def get_private():
    """Copy the private.py with site specific settings to the server."""

    base_path, code_path, git_url, repo_alias, site_name = get_vars()

    local_path = os.path.join(
        'django_project', 'core', 'settings', 'private.py')

    remote_path = os.path.join(code_path, local_path)

    if not exists(remote_path):
        fastprint(red('Please create your remove copy of private.py\n'))
        fastprint(red('See README.md for more instructions.'))
        raise Exception('Could not get remote private settings')

    get(remote_path=remote_path, local_path=local_path)

@task
def set_up_disqus(shortname):
    """Set up configuration for disqus.

    You can get shortname from http://disqus.com/admin/create/ and you must
    have disqus account to do it.
    """

    # Absolute filesystem path to the Django project directory:
    django_root = os.path.dirname(os.path.abspath(__file__))
    secret_file = os.path.join(
        django_root, 'django_project', 'core', 'settings', 'secret.py')
    with open(secret_file) as f:
        lines = f.readlines()

    # Update existing secret_file with new shortname
    with open(secret_file, 'w') as f:
        added = False
        added_line = "DISQUS_WEBSITE_SHORTNAME = " + repr(shortname) + "\n"
        for line in lines:
            if 'DISQUS_WEBSITE_SHORTNAME' in line:
                line = added_line
                added = True
            f.write(line)
        if not added:
            f.write(added_line)

@hosts('localhost')
@task
def restore_postgres_dump_locally():
    """Restore postgresql dump to local host db: changelog."""
    restore_postgres_dump(
        dbname='changelog',
        user='docker',
        password='docker')

