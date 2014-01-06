{% import '_vars.sls' as vars with context %}
{% set venv_dir = vars.path_from_root('env') %}

app-packages:
    pkg.installed:
        - pkgs:
            - python2.7
            - python-all-dev
            - python-setuptools
            - python-pip
            - python-virtualenv
            - libpq-dev
            - libevent-1.4-2
            - libevent-core-1.4-2
            - libevent-extra-1.4-2
            - libevent-dev
            - libmemcached-dev
            - libjpeg8
            - libjpeg8-dev
            - libfreetype6
            - libfreetype6-dev
            - zlib1g
            - zlib1g-dev
            - sqlite3

include:
  - memcached
  - postfix
  - version-control
  - python

project_user:
  user.present:
    - name: {{ pillar['project_name'] }}
    - remove_groups: False
    - groups: [www-data, admin]

root_dir:
  file.directory:
    - name: {{ vars.root_dir }}
    - user: {{ pillar['project_name'] }}
    - group: admin
    - mode: 775
    - makedirs: True
    - require:
      - user: project_user

run_dir:
  file.directory:
    - name: {{ vars.run_dir }}
    - user: {{ pillar['project_name'] }}
    - group: admin
    - mode: 775
    - makedirs: True
    - require:
      - user: project_user

log_dir:
  file.directory:
    - name: {{ vars.log_dir }}
    - user: {{ pillar['project_name'] }}
    - group: admin
    - mode: 775
    - makedirs: True
    - require:
      - file: root_dir

venv:
  virtualenv.managed:
    - name: {{ venv_dir }}
    - no_site_packages: True
    - distribute: True
    - require:
      - pip: virtualenv
      - file: root_dir

venv_dir:
  file.directory:
    - name: {{ venv_dir }}
    - user: {{ pillar['project_name'] }}
    - group: admin
    - mode: 775
    - recurse:
      - user
      - group
    - require:
      - virtualenv: venv
