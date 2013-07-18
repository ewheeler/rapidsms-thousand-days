#!/usr/bin/env python

from __future__ import with_statement
import os
import re

from fabric.api import run
from fabric.api import env
from fabric.api import cd
from fabric.api import task
from fabric.api import require
from fabric.api import sudo
from fabric.api import settings

env.user = "ubuntu"
env.key_filename = ["/Users/ewheeler/ewheeler.pem", ]

env.code_root = "/home/ubuntu/rapidsms-thousand-days"

PROJECT_ROOT = os.path.dirname(__file__)
CONF_ROOT = os.path.join(PROJECT_ROOT, 'conf')
env.project = 'rapidsms-thousand-days'
env.repo = u'git@github.com:ewheeler/rapidsms-thousand-days.git'


@task
def production():
    env.environment = 'production'
    env.hosts = ["thousand-days.lobos.biz"]
    env.branch = 'master'
    env.server_name = 'lobos'
    #setup_path()


@task
def update_requirements():
    """Update required Python libraries."""
    require('environment')
    project_run(u'HOME=%(home)s %(virtualenv)s/bin/pip install --use-mirrors --quiet -r %(requirements)s' % {
        'virtualenv': env.virtualenv_root,
        'requirements': os.path.join(env.code_root, 'requirements', 'production.txt'),
        'home': env.home,
    })


def project_run(cmd):
    """ Uses sudo to allow developer to run commands as project user."""
    sudo(cmd, user=env.project_user)


@task
def manage_run(command):
    """Run a Django management command on the remote server."""
    require('environment')
    manage_base = u"%(virtualenv_root)s/bin/django-admin.py " % env
    if '--settings' not in command:
        command = u"%s --settings=%s" % (command, env.settings)
    project_run(u'%s %s' % (manage_base, command))


@task
def syncdb():
    """Run syncdb and South migrations."""
    manage_run('syncdb --noinput')
    manage_run('migrate --noinput')


@task
def collectstatic():
    """Collect static files."""
    manage_run('collectstatic --noinput')


def match_changes(changes, match):
    pattern = re.compile(match)
    return pattern.search(changes) is not None


@task
def deploy(branch=None):
    """Deploy to a given environment."""
    require('environment')
    if branch is not None:
        env.branch = branch
    requirements = False
    migrations = False
    # Fetch latest changes
    with cd(env.code_root):
        run("git stash")
        # remove pyc files
        run('find . -name "*.pyc" -exec rm {} \;')
        with settings(user=env.project_user):
            run('git fetch origin')
        # Look for new requirements or migrations
        changes = run("git diff origin/%(branch)s --stat-name-width=9999" % env)
        requirements = match_changes(changes, r"requirements/")
        migrations = match_changes(changes, r"/migrations/")
        if requirements or migrations:
            run("circusctl stop")
        with settings(user=env.project_user):
            run("git reset --hard origin/%(branch)s" % env)
        run("git stash pop")
    if requirements:
        update_requirements()
        # New requirements might need new tables/migrations
        syncdb()
    elif migrations:
        syncdb()
    collectstatic()

    run("circusctl restart")
