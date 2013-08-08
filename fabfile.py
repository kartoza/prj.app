#!/bin/python
# ~/fabfile.py
# A Fabric file for carrying out various administrative tasks.
# Tim Sutton, Jan 2013

# To use this script make sure you have fabric and fabtools.
# pip install fabric fabtools

import os
from fabric.api import task, env, fastprint, cd, run, settings
from fabtools import require
from fabtools.deb import update_index
# Don't remove even though its unused
# noinspection PyUnresolvedReferences
from fabtools.vagrant import vagrant

# noinspection PyUnresolvedReferences
from fabgis.dropbox import setup_dropbox, setup_dropbox_daemon
from fabgis.django import setup_apache, build_pil
from fabgis.utilities import update_git_checkout, setup_venv
from fabgis.common import setup_env, show_environment

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
    site_name = 'visual_changelog'
    base_path = os.path.abspath(os.path.join(
        env.fg.home, 'dev', 'python'))
    git_url = 'http://github.com/timlinux/visual_changelog.git'
    repo_alias = 'visual_changelog'
    fastprint('Checking out %s to %s as %s' % (git_url, base_path, repo_alias))
    update_git_checkout(base_path, git_url, repo_alias)
    code_path = os.path.abspath(os.path.join(base_path, repo_alias))
    update_index()
    require.postfix.server(site_name)
    setup_apache(site_name, code_path=code_path)
    require.deb.package('libpq-dev')
    require.deb.package('libgeos-c1')
    require.deb.package('vim')
    setup_venv(code_path, requirements_file='REQUIREMENTS.txt')
    build_pil(code_path)
    with cd(os.path.join(code_path, 'django_project')):
        run('../venv/bin/python manage.py syncdb')
        run('../venv/bin/python manage.py migrate')
        with settings(warn_only=True):
            run('../venv/bin/python manage.py collectstatic --noinput')
    # if we are testing under vagrant, deploy our local media and db
    if 'vagrant' in env.fg.home:
        with cd(code_path):
            run('cp /vagrant/visual_changelog.db .')
            run('cp -r /vagrant/django_project/media/* django_project/media/')
            run('touch django_project/core/wsgi.py')
    fastprint('*******************************************')
    fastprint(' Don\'t forget set ALLOWED_HOSTS in ')
    fastprint(' django_project/core/settings/prod.py')
    fastprint(' to the domain name for the site.')
    fastprint('*******************************************')


@task
def freshen():
    """Freshen the server with latest git copy and touch wsgi."""
    setup_env()
    show_environment()
    base_path = os.path.abspath(os.path.join(
        env.fg.home, 'dev', 'python'))
    git_url = 'http://github.com/timlinux/visual_changelog.git'
    repo_alias = 'visual_changelog'
    fastprint('Checking out %s to %s as %s' % (git_url, base_path, repo_alias))
    update_git_checkout(base_path, git_url, repo_alias)
    code_path = os.path.abspath(os.path.join(base_path, repo_alias))
    with cd(os.path.join(code_path, 'django_project')):
        run('touch core/wsgi.py')

    fastprint('*******************************************\n')
    fastprint(' Don\'t forget set ALLOWED_HOSTS in \n')
    fastprint(' django_project/core/settings/prod.py\n')
    fastprint(' to the domain name for the site.\n')
    fastprint('*******************************************\n')
