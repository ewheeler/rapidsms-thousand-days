include:
    - nginx
    - nodejs

graphite_system_requirements:
    pkg.installed:
        - names:
            - sqlite3
            - libcairo2
            - libcairo2-dev
            - python-cairo
            - memcached

graphite_pip_requirements:
    pip.installed:
        - names:
            - whisper
            - django==1.3
            - python-memcached
            - django-tagging
            - gunicorn
        - require:
            - pkg: libcairo2
            - pkg: libcairo2-dev
            - pkg: python-cairo

# carbon doesn't install well with pip.installed, salt 0.14.0
install_carbon:
    cmd.run:
        - name: pip install carbon 
        - require:
            - pip: graphite_pip_requirements
        - unless: test -f /opt/graphite/bin/carbon-client.py

# graphite_web doesn't install well with pip.installed, salt 0.14.0
install_graphite_web:
    cmd.run:
        - name: pip install graphite_web
        - require:
            - cmd.run: install_carbon
        - unless: test -d /opt/graphite/webapp/

/opt/graphite/conf/carbon.conf:
    file.managed:
        - source: salt://statsd/opt/graphite/conf/carbon.conf
        - require:
            - cmd.run: install_carbon

/opt/graphite/conf/storage-schemas.conf:
    file.managed:
        - source: salt://statsd/opt/graphite/conf/storage-schemas.conf
        - require:
            - cmd.run: install_carbon

/opt/graphite/conf/storage-aggregation.conf:
    file.managed:
        - source: salt://statsd/opt/graphite/conf/storage-aggregation.conf
        - require:
            - cmd.run: install_carbon

/opt/graphite/webapp/graphite/local_settings.py:
    file.managed:
        - source: salt://statsd/opt/graphite/webapp/graphite/local_settings.py
        - require:
            - cmd.run: install_graphite_web

syncdb:
    cmd.run:
        - cwd: /opt/graphite/webapp/graphite
        - name: 'python manage.py syncdb --noinput'
        - unless: test -e /opt/graphite/storage/graphite.db
        - require:
            - file: /opt/graphite/webapp/graphite/local_settings.py

git://github.com/etsy/statsd.git:
    git.latest:
        - target: /opt/statsd
        - unless: test -d /opt/statsd

/opt/statsd/localConfig.js:
    file.managed:
        - source: salt://statsd/opt/statsd/localConfig.js
        - require:
            - git: git://github.com/etsy/statsd.git

/opt/graphite/storage:
    file.directory:
        - user: www-data
        - recurse:
            - user
        - require:
            - cmd.run: install_carbon
            - cmd.run: install_graphite_web
