While learning to use the excellent Django web framework, I decided to port an old Perl CGI script that handled our addressbook. I am sure there must be thousands of these kicking around on the web, but that is no reason not to add another! The code is released under a GPL license.

Installation
------------
The model is a fairly simple normalized database with one entry per person with foreign keys pointing to addresses, email address, phone numbers, etc.
To use this Django app, add 'addressbook' to your INSTALLED_APPS and use dbsync
to add the tables to the database.

You probably also want to add the URLs to urlpatterns in your base urls.py,
maybe something like:
(r'^addressbook/', include('addressbook.urls')),

Example templates are included in the "templates" directory. To use them, either
copy them to your templates directory, or make sure the app_directories loader
is in the TEMPLATE_LOADERS section of your settings.py. For example:

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

The templates use the static files feature of Django, which requires
'django.contrib.staticfiles' is in your INSTALLED_APPS
