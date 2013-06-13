
Thousand
========================

Below you will find basic setup instructions for the thousand
project. To begin you should have the following applications installed on your
local development system:

- Python >= 2.6 (2.7 recommended)
- `pip >= 1.1 <http://www.pip-installer.org/>`_
- `virtualenv >= 1.8 <http://www.virtualenv.org/>`_

Getting Started
---------------

To setup your local environment you should create a virtualenv and install the
necessary requirements::

    virtualenv --distribute thousand-env
    source thousand-env/bin/activate
    cd thousand
    pip install -r requirements/base.txt

Run syncdb::

    python manage.py syncdb

Run south migrations::

    python manage.py migrate

You should now be able to run the development server::

    python manage.py runserver

Along with celery and celerybeat::

    python manage.py celery worker -E --loglevel=info  --settings=thousand.settings
    python manage.py celery beat --loglevel=info --settings=thousand.settings

For production deployment, there is an included ini file for circus that can
be used to start and manage the django and celery services::

    circusd circus.ini

