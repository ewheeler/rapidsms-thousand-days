npm:
  pkg.installed

yaml:
  npm.installed:
    - require:
      - pkg: npm
