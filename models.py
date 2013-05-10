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

from django.db import models
from django.core.urlresolvers import reverse

class Country(models.Model):
    code = models.CharField(max_length=4, primary_key=True)
    name = models.CharField(max_length=127)

    class Meta:
        verbose_name_plural="countries"
        
    def __unicode__(self):
        return u"%s (%s)"%(self.name,self.code)
    
class State(models.Model):
    short_name = models.CharField(max_length=127)
    long_name = models.CharField(max_length=254)
    country = models.ForeignKey(Country)

    class Meta:
        unique_together = ("short_name","country")
        
    def __unicode__(self):
        return u"%s, %s"%(self.long_name,self.country.code)

class ContactLocation(models.Model):
    value = models.CharField(max_length=31)
    
    def __unicode__(self):
        return self.value
    
class ContactMethod(models.Model):
    location = models.ForeignKey(ContactLocation)
    primary = models.BooleanField(default=False)
    class Meta:
        abstract = True
    
class Address(ContactMethod):
    line1 = models.CharField(max_length=255)
    line2 = models.CharField(max_length=255, null=True, blank=True)
    line3 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255)
    state = models.ForeignKey(State)
    zip = models.CharField(max_length=31, blank=True)
    
    class Meta:
        verbose_name_plural="addresses"
        
    def __unicode__(self):
        rv = self.line1
        if self.line2:
            rv += ', '+self.line2
        if self.line3:
            rv += ', '+self.line3
        rv += ', '+self.city
        rv += ', '+self.state.short_name
        if self.zip:
            rv += ', '+self.zip
        rv += ', '+self.state.country.code
        return rv

    def __str__(self):
        return self.__unicode__()
    
class Telephone(ContactMethod):
    number = models.CharField(max_length=63, db_index=True)
    type = models.PositiveSmallIntegerField(choices=[(1,'Fixed'),(2,'Cell'),(3,'Fax')])
    def __unicode__(self):
        return self.number
    
class Email(ContactMethod):
    email = models.EmailField()
    def __unicode__(self):
        return self.email
    def url(self):
        return "mailto:%s"%self.email
    
class Website(ContactMethod):
    url = models.URLField()
    def __unicode__(self):
        return self.url

class Prefix(models.Model):    
    value = models.CharField(max_length=55, blank=True)
    def __unicode__(self):
        return self.value
    
class Person(models.Model):
    prefix = models.ForeignKey(Prefix)
    first_name = models.CharField(max_length=255, db_index=True)
    last_name = models.CharField(max_length=255, db_index=True)
    suffix = models.CharField(max_length=55, blank=True)
    image = models.ImageField(upload_to='mugshots',null=True, blank=True)
    addresses = models.ManyToManyField(Address)
    telephones = models.ManyToManyField(Telephone)
    emails = models.ManyToManyField(Email)
    websites = models.ManyToManyField(Website)
    notes = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    slug_first = models.SlugField(editable=False)
    slug_last = models.SlugField(editable=False)
    
    class Meta:
        ordering = ["last_name", "first_name"]
        verbose_name_plural="people"
        
    def __unicode__(self):
        return u"%s, %s"%(self.last_name,self.first_name)
    
    def primary_address(self):
        try:
            return self.addresses.filter(primary=True)[0]
        except IndexError:
            return None

    def primary_telephone(self):
        try:
            return self.telephones.filter(primary=True)[0]
        except IndexError:
            if self.telephones.exists():
                return self.telephones.all()[0]
            return None
        
    def primary_email(self):
        try:
            return self.emails.filter(primary=True)[0]
        except IndexError:
            return None
        
    def get_absolute_url(self):
        if not (self.slug_first or self.slug_last):
            self.save(force_update=True)
        return reverse('ab_person_by_name',args=[self.slug_last,self.slug_first])
    
    def save(self,force_insert=False, force_update=False):
        from django.template.defaultfilters import slugify
        if not self.slug_last:
            self.slug_last = slugify(self.last_name)
        if not self.slug_first:
            self.slug_first = slugify(self.first_name)
        models.Model.save(self,force_insert,force_update)   

