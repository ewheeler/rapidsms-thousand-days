python-pkgs:
  pkg:
    - installed
    - names:
      - python-pip
      - python-dev
      - build-essential
      - python-imaging
      - python-software-properties

python-headers:
  pkg:
    - installed
    - names:
      - libpq-dev
      - libev-dev
      - libevent-dev
      - libmemcached-dev
      - libjpeg8
      - libjpeg8-dev
      - libfreetype6
      - libfreetype6-dev
      - zlib1g
      - zlib1g-dev
      - libxml2-dev
      - libxslt1-dev

virtualenv:
  pip.installed:
    - upgrade: True
    - require:
      - pkg: python-pkgs
