nodejs_ppa:
  pkgrepo.managed:
    - ppa: chris-lea/node.js

nodejs:
  pkg.latest:
    - names:
      - nodejs
      - npm
    - refresh: True
    - require:
      - pkgrepo: nodejs_ppa
