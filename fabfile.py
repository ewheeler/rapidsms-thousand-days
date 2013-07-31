#!/usr/bin/env python

from __future__ import with_statement
import os
import re
from StringIO import StringIO

from fabric.api import run
from fabric.api import env
from fabric.api import cd
from fabric.api import task
from fabric.api import require
from fabric.api import settings
from fabric.api import abort
from fabric.api import put
from fabric.api import sudo
from fabric.api import hide

from fabric.contrib import files

import pystache

env.key_filename = ["/Users/ewheeler/ewheeler.pem", ]

PROJECT_ROOT = os.path.dirname(__file__)
CONF_ROOT = os.path.join(PROJECT_ROOT, 'conf', 'templates')
SERVER_ROLES = ['app', 'lb', 'db', 'data']

env.project = 'thousand'
env.repo = u'https://github.com/ewheeler/rapidsms-thousand-days.git'
env.project_user = 'ewheeler'

env.django_port = 8000
env.circushttpd_port = 8001
env.celeryflower_port = 8002


def setup_path():
    env.home = '/home/%(project_user)s/' % env
    env.root = os.path.join(env.home, 'www', env.environment)
    env.code_root = os.path.join(env.root, env.project)
    env.project_root = os.path.join(env.code_root, env.project)
    env.virtualenv_root = os.path.join(env.root, 'env')
    env.log_dir = os.path.join(env.root, 'log')
    env.vhost = '%s_%s' % (env.project, env.environment)
    env.settings = '%(project)s.settings.%(environment)s' % env


@task
def vagrant():
    env.environment = 'staging'
    env.hosts = ['127.0.0.1']
    env.port = 2222
    env.branch = 'master'
    env.server_name = 'vagrant.localhost'
    setup_path()


@task
def staging():
    env.environment = 'staging'
    env.hosts = ['127.0.0.1']
    env.port = 2222
    env.branch = 'master'
    env.server_name = 'vagrant.localhost'
    setup_path()


@task
def production():
    env.environment = 'production'
    env.hosts = ["thousand-days.lobos.biz"]
    env.branch = 'master'
    env.server_name = 'thousand-days.lobos.biz'
    setup_path()


@task
def update_requirements():
    """Update required Python libraries."""
    require('environment')
    run(u'HOME=%(home)s %(virtualenv)s/bin/pip install'
        u' --use-mirrors --quiet -r %(requirements)s' % {
        'virtualenv': env.virtualenv_root,
        'requirements': os.path.join(env.code_root,
                                     'requirements',
                                     'production.txt'),
        'home': env.home,
        })


@task
def manage_run(command):
    """Run a Django management command on the remote server."""
    require('environment')
    manage_base = u"%(virtualenv_root)s/bin/django-admin.py " % env
    if '--pythonpath' not in command:
        command = u"%s --pythonpath=%s" % (command, env.code_root)
    if '--settings' not in command:
        command = u"%s --settings=%s" % (command, env.settings)
    run(u'%s %s' % (manage_base, command))


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
        # remove pyc files
        sudo('find . -name "*.pyc" -exec rm {} \;')
        with settings(user=env.project_user):
            run('git fetch origin')
        # Look for new requirements or migrations
        changes = run("git diff origin/%(branch)s --stat-name-width=9999" %
                      env)
        requirements = match_changes(changes, r"requirements/")
        migrations = match_changes(changes, r"/migrations/")
        if requirements or migrations:
            sudo("service circus stop")
        with settings(user=env.project_user):
            run("git reset --hard origin/%(branch)s" % env)
    if requirements:
        update_requirements()
        # New requirements might need new tables/migrations
        syncdb()
    elif migrations:
        syncdb()
    collectstatic()
    sudo("service circus restart")


@task
def setup_server(*roles):
    """Install packages and add configurations for server given roles."""
    require('environment')

    roles = list(roles)

    if not roles:
        abort("setup_server requires one or more server roles,"
              "e.g. setup_server:app or setup_server:all")

    if roles == ['all', ]:
        roles = SERVER_ROLES
    if 'base' not in roles:
        roles.insert(0, 'base')
    if 'app' in roles:
        # Create project directories and install Python requirements
        run('mkdir -p %(root)s' % env)
        run('mkdir -p %(log_dir)s' % env)
        # FIXME: update to SSH as normal user and use sudo
        # we ssh as the project_user here to maintain ssh agent
        # forwarding, because it doesn't work with sudo. read:
        # http://serverfault.com/q/107187
        with settings(user=env.project_user):
            if not files.exists(env.code_root):
                run('git clone --quiet %(repo)s %(code_root)s' % env)
            with cd(env.code_root):
                run('git checkout %(branch)s' % env)
        if not files.exists(env.virtualenv_root):
            run('virtualenv --quiet -p python2.7'
                ' --clear --distribute %s' % env.virtualenv_root)
            # TODO: Why do we need this next part?
            path_file = os.path.join(env.virtualenv_root, 'lib', 'python2.7',
                                     'site-packages', 'project.pth')
            files.append(path_file, env.code_root, use_sudo=True)
            sudo('chown %s:%s %s' % (env.project_user,
                                     env.project_user, path_file))
        update_requirements()
        upload_circus_conf(app_name=u'%(project)s-%(environment)s' % env)
    if 'lb' in roles:
        remove_default_site()
        upload_nginx_site_conf(site_name=u'%(project)s-%(environment)s' % env)
    if 'data' in roles:
        put('dev-thousand.db', env.code_root)
        put('patients.db', env.code_root)
        put('experiments/experiment.db',
            '%s/experiments/experiment.db' % env.code_root)


@task
def upload_template(filename, destination, context=None,
                    use_sudo=False, backup=True, mode=None):
    print filename
    print destination
    func = use_sudo and sudo or run
    # Normalize destination to be an actual filename, due to using StringIO
    with settings(hide('everything'), warn_only=True):
        if func('test -d %s' % destination).succeeded:
            sep = "" if destination.endswith('/') else "/"
            destination += sep + os.path.basename(filename)
    # Process template
    context = context or {}
    env_context = env.copy()
    env_context.update(context)
    filepath = os.path.join(CONF_ROOT, filename)
    # TODO use jinja?
    text = pystache.render(open(filepath).read(), env_context)
    # Back up original file
    if backup and files.exists(destination):
        func("cp %s{,.bak}" % destination)
    # Upload the file.
    put(
        local_path=StringIO(text),
        remote_path=destination,
        use_sudo=use_sudo,
        mode=mode
    )


@task
def upload_circus_conf(app_name, template_name=None, context=None):
    """Upload circus configuration from a template."""
    # TODO should this be a salt-managed file?
    template_name = template_name or u'circus/circus.ini'
    destination = u"/etc/circus.ini"
    upload_template(template_name, destination, context=context, use_sudo=True)
    sudo('chown root:root /etc/circus.ini')

    upstart_conf = u'circus/circus.conf'
    upstart_destination = u'/etc/init/circus.conf'
    upload_template(upstart_conf, upstart_destination,
                    context=context, use_sudo=True)
    sudo('chown root:root /etc/init/circus.conf')


@task
def remove_default_site():
    """Remove the default Nginx site if it exists."""

    nginx_default = u'/etc/nginx/conf.d/default.conf'
    if files.exists(nginx_default):
        sudo(u'rm %s' % nginx_default)


@task
def upload_nginx_site_conf(site_name, template_name=None,
                           context=None, enable=True):
    """Upload Nginx site configuration from a template."""
    # TODO should this be a salt-managed file?
    template_name = template_name or u'nginx/%s.conf' % site_name
    site_available = u'/etc/nginx/conf.d/%s.conf' % site_name
    upload_template(template_name, site_available,
                    context=context, use_sudo=True)
    sudo(u'/etc/init.d/nginx restart')
