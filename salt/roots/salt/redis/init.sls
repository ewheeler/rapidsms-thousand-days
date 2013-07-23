redis-server:
  service:
    - running
    - require:
      - pkg: redis-server
  pkg:
    - installed
