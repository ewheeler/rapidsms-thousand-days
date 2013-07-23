circus_pkgs:
  pkg.installed:
    - names:
      - python-dev
      - python-pip

circus:
  pip.installed:
    - name: circus
    - require:
      - pkg: python-pip
  service:
    - running
    - require:
      - pip: circus
