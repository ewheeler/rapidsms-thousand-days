redis_ppa:
  pkgrepo.managed:
    - ppa: chris-lea/redis-server

redis-server:
  service:
    - running
    - require:
      - pkg: redis-server
  pkg:
    - installed
    - require:
      - pkgrepo: redis_ppa
