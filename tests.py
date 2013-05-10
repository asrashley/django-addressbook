"""
Copyright 2010 Alex Ashley

This file is part of Django addressbook.

    Django addressbook is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Django addressbook is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Django addressbook.  If not, see <http://www.gnu.org/licenses/>.
"""
from addressbook.models import Person
from django.test import TestCase
from django.core.urlresolvers import reverse

class NoAddressTest(TestCase):
    fixtures = [] #['site']

    def test_get_asset_list(self):
        """
        Test GET list of all people, when no people in database
        """
        self.failUnlessEqual(Person.objects.count(), 0, 'There should not be any people loaded from fixtures')
        url = reverse('ab_all',args=[])
        response = self.client.get(url)

        # Check some response details
        self.failUnlessEqual(response.status_code, 200)
        
class AddressTest(TestCase):
    fixtures = ['addresses']

    def test_get_asset_list(self):
        """
        GET list of all people
        """
        self.failIfEqual(Person.objects.count(), 0, 'No people loaded from fixtures')

        url = reverse('ab_all',args=[])
        response = self.client.get(url)

        # Check some response details
        self.failUnlessEqual(response.status_code, 200)
        
        self.assertContains(response, 'Bloggs')
        self.assertContains(response, '1 Example Road')
        
    def test_edit_person(self):
        url = reverse('intranet.addressbook.views.person_edit',args=['bloggs','fred'])
        response = self.client.get(url)
        # Should re-direct to login required
        self.failUnlessEqual(response.status_code, 302)
        login = self.client.login(username='test', password='password')
        self.failUnless(login, 'Could not log in')
        response = self.client.get(url)
        self.failUnlessEqual(response.status_code, 200)
