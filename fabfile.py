#!/usr/bin/env python

from __future__ import with_statement
import json
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
from fabric.api import get
from fabric.api import put
from fabric.api import sudo
from fabric.api import hide
from fabric.api import local
from fabric.colors import red
from fabric.contrib import files
from fabric.contrib import project
from fabric.utils import error

import pystache

PROJECT_ROOT = os.path.dirname(__file__)
CONF_ROOT = os.path.join(PROJECT_ROOT, 'conf')
SERVER_ROLES = ['app', 'lb', 'db', 'data']

env.project = 'thousand'
env.repo = u'https://github.com/ewheeler/rapidsms-thousand-days.git'
env.shell = '/bin/bash -c'
env.disable_known_hosts = True
env.forward_agent = True

env.django_port = 8000
env.circushttpd_port = 8001
env.celeryflower_port = 8002


def setup_path():
    env.home = '/home/%(project_user)s/' % env
    env.root = os.path.join('/var/www/', '%(project)s-%(environment)s' % env)
    env.code_root = os.path.join(env.root, 'source')
    env.virtualenv_root = os.path.join(env.root, 'env')
    env.db = '%s_%s' % (env.project, env.environment)
    env.settings = '%(project)s.settings.%(environment)s' % env


@task
def vagrant():
    env.environment = 'staging'
    env.hosts = ['127.0.0.1']
    env.port = 2222
    env.branch = 'master'
    env.server_name = 'vagrant.localhost'
    env.project_user = 'vagrant'
    env.user = 'vagrant'
    # use vagrant ssh key
    result = local('vagrant ssh-config | grep IdentityFile', capture=True)
    env.key_filename = result.split()[1].strip('"')
    setup_path()


@task
def staging():
    env.environment = 'staging'
    env.hosts = ['127.0.0.1']
    env.port = 2222
    env.branch = 'master'
    env.server_name = 'vagrant.localhost'
    env.project_user = 'ewheeler'
    env.user = 'ewheeler'
    setup_path()


@task
def production():
    env.environment = 'production'
    env.hosts = ["thousand-days.lobos.biz"]
    env.branch = 'master'
    env.server_name = 'thousand-days.lobos.biz'
    env.project_user = 'ubuntu'
    env.user = 'ubuntu'
    setup_path()


@task
def provision(common='master'):
    """Provision server with masterless Salt minion."""
    require('environment')
    # Install salt minion
    with settings(warn_only=True):
        with hide('running', 'stdout', 'stderr'):
            installed = run('which salt-call')
    if not installed:
        bootstrap_file = os.path.join(CONF_ROOT, 'bootstrap-salt.sh')
        put(bootstrap_file, '/tmp/bootstrap-salt.sh')
        sudo('sh /tmp/bootstrap-salt.sh stable')
    # Rsync local states and pillars
    minion_file = os.path.join(CONF_ROOT, 'minion.conf')
    files.upload_template(minion_file, '/etc/salt/minion',
                          use_sudo=True, context=env)
    salt_root = CONF_ROOT if CONF_ROOT.endswith('/') else CONF_ROOT + '/'
    environments = ['staging', 'production']
    # Only include current environment's pillar tree
    exclude = [os.path.join('pillar', e) for e in environments
               if e != env.environment]
    project.rsync_project(local_dir=salt_root, remote_dir='/tmp/salt',
                          delete=True, exclude=exclude)
    sudo('rm -rf /srv/*')
    sudo('mv /tmp/salt/* /srv/')
    sudo('rm -rf /tmp/salt/')
    # Pull common states
    sudo('rm -rf /tmp/common/')
    with settings(warn_only=True):
        with hide('running', 'stdout', 'stderr'):
            installed = run('which git')
    if not installed:
        sudo('apt-get install git-core -q -y')
    #run('git clone git://github.com/caktus/margarita.git /tmp/common/')
    #with cd('/tmp/common/'):
    #    run('git checkout %s' % common)
    #sudo('mv /tmp/common/ /srv/common/')
    #sudo('rm -rf /tmp/common/')
    sudo('chown root:root -R /srv/')
    # Update to highstate
    with settings(warn_only=True):
        sudo('salt-call --local state.highstate -l info --out json > '
             '/tmp/output.json')
        get('/tmp/output.json', 'output.json')
        with open('output.json', 'r') as f:
            try:
                results = json.load(f)
            except (TypeError, ValueError) as e:
                error(u'Non-JSON output from salt-call', exception=e)
            else:
                if isinstance(results['local'], list):
                    for result in results['local']:
                        print red(u'Error: {0}'.format(result))
                else:
                    for state, result in results['local'].items():
                        if not result["result"]:
                            if 'name' in result:
                                print red(u'Error with %(name)s '
                                          'state: %(comment)s'
                                          % result)
                            else:
                                print red(u'Error with {0} state: {1}'
                                          .format(state, result['comment']))


def project_run(cmd):
    """ Uses sudo to allow developer to run commands as project user."""
    sudo(cmd, user=env.project_user)


@task
def update_requirements():
    """Update required Python libraries."""
    require('environment')
    project_run(u'HOME=%(home)s %(virtualenv)s/bin/pip install --use-mirrors -r %(requirements)s' % {
        'virtualenv': env.virtualenv_root,
        'requirements': os.path.join(env.code_root, 'requirements', 'production.txt'),
        'home': env.home,
    })

@task
def manage_run(command):
    """Run a Django management command on the remote server."""
    require('environment')
    manage_base = u"source %(virtualenv_root)s/bin/activate && %(virtualenv_root)s/bin/django-admin.py " % env
    if '--settings' not in command:
        command = u"%s --settings=%s" % (command, env.settings)
    project_run(u'%s %s' % (manage_base, command))


@task
def syncdb():
    """Run syncdb and South migrations."""
    manage_run('syncdb --noinput')
    manage_run('migrate --noinput')


@task
def load_fixtures():
    """Load fixtures."""
    manage_run('loaddata appointments_timeline')
    manage_run('loaddata appointments_milestone')


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
    if not env.repo:
        abort('env.repo is not set.')
    if branch is not None:
        env.branch = branch
    requirements = False
    migrations = False
    initial = False
    if files.exists(env.code_root):
        # Fetch latest changes
        with cd(env.code_root):
            # remove pyc files
            sudo('find . -name "*.pyc" -exec rm {} \;')
            run('git fetch origin')
            # Look for new requirements or migrations
            changes = run("git diff origin/%(branch)s --stat-name-width=9999" % env)
            requirements = match_changes(changes, r"requirements/")
            migrations = match_changes(changes, r"/migrations/")
            if requirements or migrations:
                sudo("service circus stop")
            with settings(user=env.project_user):
                run("git reset --hard origin/%(branch)s" % env)
    else:
        # Initial clone
        run('git clone %(repo)s %(code_root)s' % env)
        with cd(env.code_root):
            run('git submodule init')
            run('git checkout %(branch)s' % env)
            run('git submodule update')
        requirements = True
        migrations = True
        initial = True
        # Add code root to the Python path
        path_file = os.path.join(env.virtualenv_root, 'lib', 'python2.7', 'site-packages', 'project.pth')
        files.append(path_file, env.code_root, use_sudo=True)
        sudo('chown %s:admin %s' % (env.project_user, path_file))
        sudo('chmod 775 %(code_root)s' % env)
    sudo('chown %(project_user)s:admin -R %(code_root)s' % env)
    if requirements:
        update_requirements()
        # New requirements might need new tables/migrations
        syncdb()
    elif migrations:
        syncdb()
    collectstatic()
    sudo("service circus restart")
    if initial:
        put('dev-thousand.db', env.code_root)
        put('patients.db', env.code_root)
        load_fixtures()

@task
def upload_data():
    sudo('chmod 775 %(code_root)s' % env)
    sudo('chown %(project_user)s:admin -R %(code_root)s' % env)
    put('dev-thousand.db', env.code_root)
    put('patients.db', env.code_root)
    load_fixtures()


@task
def setup_nginx():
    remove_default_site()
    upload_nginx_site_conf(site_name=u'%(project)s-%(environment)s' % env)


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
    filepath = os.path.join(CONF_ROOT, 'templates', filename)
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
def remove_default_site():
    """Remove the default Nginx site if it exists."""

    nginx_default = u'/etc/nginx/conf.d/default.conf'
    if files.exists(nginx_default):
        sudo(u'rm %s' % nginx_default)

    nginx_default = u'/etc/nginx/sites-enabled/default'
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
