include:
  - python

libevent-dev:
  pkg.installed

gevent:
  pip.installed:
    - require:
      - pkg: libevent-dev

meinheld:
  pip.installed

chaussette:
  pip.installed

circus:
  pip:
    - installed
    - require:
      - pip: meinheld
      - pip: chaussette
    - watch:
      - file: /etc/circus.ini
      - file: /etc/init/circus.conf

/etc/circus.ini:
  file.managed:
    - source: salt://circus/circus.ini
    - template: jinja

/etc/init/circus.conf:
  file.managed:
    - source: salt://circus/circus.conf
    - template: jinja
