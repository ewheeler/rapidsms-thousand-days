redis_ppa:
  pkgrepo.managed:
    - ppa: chris-lea/redis-server

redis-server:
  pkg.latest:
    - refresh: True
    - require:
       - pkgrepo: redis_ppa

  service.running:
    - enable: True
    - reload: True
    - require:
       - pkg: redis-server
