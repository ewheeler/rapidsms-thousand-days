nodejs_ppa:
  pkgrepo.managed:
    - ppa: chris-lea/node.js

nodejs:
  pkg.latest:
    - names:
      - nodejs
    - refresh: True
    - require:
      - pkgrepo: nodejs_ppa
