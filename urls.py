#Copyright 2010 Alex Ashley
#
#This file is part of Django addressbook.
#
#    Django addressbook is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Django addressbook is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Django addressbook.  If not, see <http://www.gnu.org/licenses/>.

from django.conf.urls.defaults import patterns,url
import views;

urlpatterns = patterns('',
    # front page
    url(r'^$', views.index, name="addressbook_index"),
    url(r'^export$', views.vcard_export, name="addressbook_export"),
    url(r'^\*$', views.person_search, {'query':None},name='ab_all'),
    url(r'^(?P<query>\w+)/*$',views.person_search, name="addressbook_search"),
    url(r'^(?P<lastname>[a-zA-Z0-9\-]+)/(?P<firstname>[a-zA-Z0-9\-]+)/$', views.person_by_name, name="ab_person_by_name"),
    (r'^(?P<lastname>[a-zA-Z0-9\-]+)/(?P<firstname>[a-zA-Z0-9\-]+)/edit$', views.person_edit),
    (r'^(?P<lastname>[a-zA-Z0-9\-]+)/(?P<firstname>[a-zA-Z0-9\-]+)/delete$', views.person_delete),
)

