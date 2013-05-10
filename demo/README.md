This directory contains a basic Django setup to demonstrate the use of the addressbook.

To run this site:

    python manage.py syncdb
    python manage.py loaddata addresses.json
    python manage.py runserver

This demo assumes that sqlite is installed, which should be a fairly safe assumption if you are running a version of Python above 2.5.

You can safely delete this directory from any site using the Django addressbook.


