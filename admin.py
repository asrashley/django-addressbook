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
from models import *
from django.contrib import admin

admin.site.register(ContactLocation)
admin.site.register(Country)
admin.site.register(State)
admin.site.register(Address)
admin.site.register(Telephone)
admin.site.register(Email)
admin.site.register(Website)
admin.site.register(Prefix)
admin.site.register(Person)
