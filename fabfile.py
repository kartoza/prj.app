#!/bin/python
# ~/fabfile.py
# A Fabric file for carrying out various administrative tasks.
# Tim Sutton, Jan 2013

# To use this script make sure you have fabric and fabtools.
# pip install fabric fabtools

import os
import getpass

from fabric.api import task, env, fastprint, cd, run, sudo, local, prompt
from fabric.contrib.project import rsync_project
from fabric.contrib.files import exists, sed
from fabric.colors import red, blue, green
from fabtools import require
from fabtools.deb import update_index
# Don't remove even though its unused
# noinspection PyUnresolvedReferences
from fabtools.vagrant import vagrant

# noinspection PyUnresolvedReferences
from fabgis.dropbox import setup_dropbox, setup_dropbox_daemon
from fabgis.django import setup_apache, build_pil, set_media_permissions
from fabgis.git import update_git_checkout
from fabgis.virtualenv import setup_venv
from fabgis.common import setup_env, show_environment
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
        * code_path: Project dir e.g. ``/home/foo/python/visual_changelog``
        * git_url: Url for git checkout - use http for read only checkout
        * repo_alias: Name of checkout folder e.g. ``visual_changelog``
        * site_name: Name for the web site e.g. ``visual_changelog``

    :rtype: tuple
    """
    setup_env()
    site_name = 'visual_changelog'
    base_path = os.path.abspath(os.path.join(
        env.fg.home, 'dev', 'python'))
    git_url = 'http://github.com/timlinux/visual_changelog.git'
    repo_alias = 'visual_changelog'
    code_path = os.path.abspath(os.path.join(base_path, repo_alias))
    return base_path, code_path, git_url, repo_alias, site_name

@task
def update_venv(code_path):
    """Update the virtual environment to ensure it has node etc. installed.

    :param code_path: Directory in which project is located.
    :type code_path: str

    e.g.::

        fab -H localhost update_venv:/home/timlinux/dev/python/visual_changelog
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
        password='',
        ignore_permissions=True,
        file_name=dump_path)


@task
def update_apache():
    """Update the apache configuration prompting for github account info.

    .. note:: The config file is taken from the local system.

    """
    code_path = os.path.dirname(__file__)

    git_url = 'https://api.github.com/repos/timlinux/visual_changelog/issues'
    git_user = prompt(
        'Please enter the github user account that issues submitted via the\n'
        'web ui should be created as. This will be written into the apache\n'
        'configuration file under /etc/apache2/sites-available so you\n'
        'should take appropriate security measures.\nUser :\n')
    git_password = getpass.getpass()
    domain = 'changelog.linfiniti.com'
    setup_apache(
        site_name='visual_changelog',
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
    update_apache(code_path, site_name)
    require.deb.package('libpq-dev')
    require.deb.package('libgeos-c1')
    require.deb.package('vim')
    update_venv(code_path)
    with cd(os.path.join(code_path, 'django_project')):
        run('../venv/bin/python manage.py syncdb --noinput ')
        run('../venv/bin/python manage.py migrate')
    set_db_permissions()
    # if we are testing under vagrant, deploy our local media and db
    if 'vagrant' in env.fg.home:
        with cd(code_path):
            run('cp /vagrant/visual_changelog.db .')
            run('touch django_project/core/wsgi.py')

    sync_media_to_server()
    collectstatic()
    fastprint('*******************************************\n')
    fastprint(red(' Don\'t forget set ALLOWED_HOSTS in '))
    fastprint(' django_project/core/settings/prod.py')
    fastprint(' to the domain name for the site.')
    fastprint('*******************************************\n')


@task
def freshen():
    """Freshen the server with latest git copy and touch wsgi.

    .. note:: Preferred normal way of doing this is rather to use the
        sync_project_to_server task and not to checkout from git.

    """
    base_path, code_path, git_url, repo_alias, site_name = get_vars()
    git_url = 'http://github.com/timlinux/visual_changelog.git'
    update_git_checkout(base_path, git_url, repo_alias)
    with cd(os.path.join(code_path, 'django_project')):
        run('touch core/wsgi.py')
    collectstatic()

    fastprint('*******************************************\n')
    fastprint(red(' Don\'t forget set ALLOWED_HOSTS in \n'))
    fastprint(' django_project/core/settings/prod.py\n')
    fastprint(' to the domain name for the site.\n')
    fastprint('*******************************************\n')

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
        code_path, 'resources', 'sqlite', 'visual_changelog.db')
    local_path = os.path.join(
        os.path.dirname(__file__), 'resources/sqlite/visual_changelog.db')
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
    rsync_project(
        base_path,
        delete=False,
        exclude=[
            '*.pyc',
            '.git',
            '.DS_Store',
            'visual_changelog.db',
            'venv',
            'django_project/static'])
    with cd(os.path.join(code_path, 'django_project')):
        run('touch core/wsgi.py')
    set_media_permissions(code_path)
    set_db_permissions()
    collectstatic()
    fastprint(blue('Your server is now in synchronised to your local project'))

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
    fastprint(red('Warning: your server is now in DEBUG mode!'))

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
    fastprint(blue('Note: your server is now in PRODUCTION mode!'))


@task
def set_db_permissions():
    """Set the db so user wsgi has all permissions.
    """
    user = 'wsgi'
    dbname = 'changelog'
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


@task
def get_live_db():
    """Get the live db - will overwrite your local copy."""
    get_postgres_dump('changelog')

@task
def get_live_media():
    """Get the live media - will overwrite your local copy."""
    base_path, code_path, git_url, repo_alias, site_name = get_vars()
    path = '%s/django_project/media' % code_path
    if not exists(path):
        run('mkdir %s' % path)
    local('rsync -ave ssh %s:%s/django_project/media/* django_project/media/'
          % (env['host_string'], code_path))

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
    command = ('../venv/bin/python manage.py migrate changes')
    base_path, code_path, git_url, repo_alias, site_name = get_vars()
    with cd(os.path.join(code_path, 'django_project')):
        run(command)
        run('touch core/wsgi.py')
    fastprint(green('Note: your server is now has the latest SOUTH '
                    'migrations applied.'))
