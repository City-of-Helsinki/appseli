Appseli - The Helsinki application catalogue
============================================

Installation
------------

Verify python version. It should be 2.7.x, though other versions may be supported too.

    $ python --version

Setup

    $ git clone git@github.com:koirikivi/appseli.git
    $ cd appseli/
    $ virtualenv venv
    $ source venv/bin/activate
    # Note: Pillow may require some extra packages, so if the following command fails,
    # consult http://pillow.readthedocs.org/en/latest/installation.html#external-libraries
    $ pip install -r requirements.txt
    $ python manage.py syncdb
    $ python manage.py legacy_import

Verify

    $ python manage.py runserver
    # Visit localhost:8000/proto/ with browser
