
RapidSMS Thousand Days
========================
RapidSMS project for tracking mother/child pairs and supporting interventions
across the contiuum of care from conception to age two: the most critical 1000 days
of a child's life.

Includes modules for:

- Antenatal care appointment reminders
- Postnatal care appointment reminders
- Growth monitoring and analysis
- Arbitrary exploration of patient data
- API for accessing patient information
- Simple exporting of data formatted for csv, html, json, R, or SAS


Below you will find basic setup instructions for the thousand
project. To begin you should have the following applications installed on your
local development system:

- Python >= 2.6 (2.7 recommended)
- `pip >= 1.1 <http://www.pip-installer.org/>`_
- `virtualenv >= 1.7 <http://www.virtualenv.org/>`_
- `virtualenvwrapper >= 3.0 <http://pypi.python.org/pypi/virtualenvwrapper>`_
- Postgres >= 8.4 (9.1 recommended)
- git >= 1.7

Getting Started
---------------

To setup your local environment you should create a virtualenv and install the
necessary requirements::

    virtualenv --distribute thousand-env
    $VIRTUAL_ENV/bin/pip install -r $PWD/requirements/dev.txt

Then create a local settings file and set your ``DJANGO_SETTINGS_MODULE`` to use it::

    cp thousand/settings/local.example.py thousand/settings/local.py
    echo "export DJANGO_SETTINGS_MODULE=thousand.settings.local" >> $VIRTUAL_ENV/bin/postactivate
    echo "unset DJANGO_SETTINGS_MODULE" >> $VIRTUAL_ENV/bin/postdeactivate

Exit the virtualenv and reactivate it to activate the settings just changed::

    deactivate
    workon thousand-env

Create the Postgres database and run the initial syncdb/migrate::

    createdb -E UTF-8 deployproj
    python manage.py syncdb
    python manage.py migrate

Load timelines and milestones::

    python manage.py loaddata appointments_timeline.json
    python manage.py loaddata appointments_milestone.json

You should now be able to run the development server::

    python manage.py runserver

Along with celery and celerybeat::

    python manage.py celery worker -E --loglevel=info  --settings=thousand.settings
    python manage.py celery beat --loglevel=info --settings=thousand.settings


Production
----------

See included nginx.conf.example for example web server configuration

To generate admin credentials for circus-web::

    printf "admin:$(openssl passwd -crypt ch@ng3m3)\n" >> htpasswd-example


Use Django's management command to prepare static assets::

    python manage.py collectstatic


For production deployment, there is an included ini file for circus that can
be used to start and manage the django and celery services::

    circusd --daemon circus.ini


Then use::

    circusctl


Or::
    circus-top


Or navigate to http://localhost:8001 to manage circus

And navigate to http://localhost:8002 to manage celery

And navigate to http://localhost:8003 to view cleaver experiments


Experiments
-----------

The Thousand Days project includes `Cleaver <https://github.com/ryanpetrello/cleaver>`_
for split testing experiments.

To conduct web split testing experiments, add your experiments to thousand/context_processors.py
which makes the experiment choice available in the RequestContext.

See thousand/context_processors.py and thousand/templates/thousand/index.html for example usage.

