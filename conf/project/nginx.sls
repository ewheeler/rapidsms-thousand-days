nginx_install:
  pkgrepo.managed:
    - ppa: nginx/stable

  pkg.installed:
    - name: nginx-extras
    - require:
      - pkgrepo: nginx_install

  service.running:
    - name: nginx
    - enable: True
    - require:
      - pkg: nginx_install
