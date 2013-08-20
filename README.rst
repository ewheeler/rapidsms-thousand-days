
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
- A/B and split testing for web views and SMS messages
- Event tracking and cohort analysis
- Scripts for provisioning and managing servers


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


For production deployment, there is an included ``circus.ini`` file for circus that can
be used to start and manage the django and celery services::

    circusd --daemon circus.ini


Then use::

    circusctl


Or::

    circus-top


Then navigate to `http://circus.example.com <http://circus.example.com>`_ to manage circus

Navigate to `http://celery.example.com <http://celery.example.com>`_ to manage celery


Provisioning
------------

The Thousand Days project includes `Salt <http://saltstack.com>`_ states,
and a `Fabric <http://fabfile.org>`_ fabfile for server provisioning and management.

You can test the provisioning/deployment using `Vagrant <http://vagrantup.com/>`_.

After installing Vagrant, install `Salty Vagrant <https://github.com/saltstack/salty-vagrant>`_::

    vagrant plugin install vagrant-salt

Installing `vagrant-cachier <https://github.com/fgrehm/vagrant-cachier>`_ will
help avoid repeated downloads of project dependencies if you reload or provision VMs often.::

    vagrant plugin install vagrant-cachier

Edit `salt/roots/pillar/users.sls` and add your user and ssh key, following
the examples. Later you'll be able to ssh to the vagrant system using that
userid and key.

Using the Vagrantfile you can start up the VM. This requires the ``precise32`` box::

    vagrant up

You can find out how ssh is set up by running::

    vagrant ssh_config

Example output::

    $ vagrant ssh-config
    Host default
      HostName 127.0.0.1
      User vagrant
      Port 2222

You can ssh in as any user with::

    ssh -p 2222 yourusername@127.0.0.1

where `yourusername` is a user you added to users.sls, and 2222 and
127.0.0.1 are changed to whatever vagrant reported.

You can also ssh in as `vagrant` by simply doing::

    vagrant ssh

and vagrant has sudo, so you can do anything you need that way.


If you change the salt files and want to update the virtual machine,
you can::

    ssh -p 2222 localhost sudo salt-call --local state.highstate [-l debug]

but it's easier to::

    vagrant reload

which will both provision and reboot.

You can provision a new server with the
``provision`` fab command::


        fab vagrant provision

Then you have to do an initial deploy.  You also use this command to
deploy updates::

        fab vagrant deploy

or::

        fab vagrant deploy:<branchname>

The Vagrantfile arranges for port 80 in the vm to be accessible
as port 8089 on the host system. The fabfile sets up the configuration
to assume a hostname of `dev.example.com`. So to visit the running
web site:

1. Add ``127.0.0.1 dev.example.com`` to your ``/etc/hosts`` file (and change the hostname
   if you changed it in the fabfile).
2. Visit `http://dev.example.com:8089/`


Deployment
----------

For future deployments, you can deploy changes to a particular environment with
the ``deploy`` command. This takes an optional branch name to deploy. If the branch
is not given, it will use the default branch defined for this environment in
``env.branch``::

    fab staging deploy
    fab staging deploy:new-feature

New requirements or South migrations are detected by parsing the VCS changes and
will be installed/run automatically.


Experiments
-----------

The Thousand Days project includes `rapidsms-xray <https://github.com/ewheeler/rapidsms-xray>`_
for split testing experiments and event tracking.

To conduct web split testing experiments, add your experiments to
your app's ``context_processors.py`` which makes the experiment choice
available in the RequestContext. You don't have to put your experiments in a
context_processor -- its just a convenient location so they can all be in one place.

See `xray/context_processors.py 
<https://github.com/ewheeler/rapidsms-xray/blob/master/xray/context_processors.py>`_
and `xray/templates/xray/index.html
<https://github.com/ewheeler/rapidsms-xray/blob/master/xray/templates/xray/index.html>`_ for example usage.

To conduct sms split testing experiments, add your experiments to your app.py or handler and
ensure that the ``xray`` app is listed in your setting.py's ``INSTALLED_APPS``
`xray/app.py <https://github.com/ewheeler/rapidsms-xray/blob/master/xray/app.py>`_ will deal with identifying experiment participation during the router's
``filter`` phase, so experiments can be conducted in any of the subsequent incoming phases.

Please be aware that experiment participation is handled separately for web and sms
split testing (specifically, web participant identity is cookie-based for non-logged-in
uses and is user_id-based for logged-in users, whereas sms participant identity
is based on mobile number) -- that is, a web experiment participant cannot be scored
by a SMS conversion event and vice-versa.

See `xray/app.py
<https://github.com/ewheeler/rapidsms-xray/blob/master/xray/app.py>`_ for example usage.


Events
------

TODO


Documentation
-----------------------------------

Documentation on using rapidsms-thousand-days is available on
`Read The Docs <http://readthedocs.org/docs/rapidsms-thousand-days/>`_.


Running the Tests
------------------------------------

You can run the tests with via::

    python setup.py test

or::

    python runtests.py


License
--------------------------------------

rapidsms-thousand-days is released under the BSD License. See the
`LICENSE <https://github.com/ewheeler/rapidsms-thousand-days/blob/master/LICENSE>`_ file for more details.


Contributing
--------------------------------------

If you think you've found a bug or are interested in contributing to this project
check out `rapidsms-thousand-days on Github <https://github.com/ewheeler/rapidsms-thousand-days>`_.
