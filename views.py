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
from intranet.djangoutil import Table, TableColumn
from django import forms, http
from django.shortcuts import render_to_response
from django.template import RequestContext
#from django.core.urlresolvers import reverse
#from django.forms.formsets import formset_factory
from django.forms.models import modelformset_factory
from django.contrib.auth.decorators import login_required
from django.contrib.sitemaps import Sitemap
import vobject
import datetime 
import re

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address

class TelephoneForm(forms.ModelForm):
    class Meta:
        model = Telephone

class EmailForm(forms.ModelForm):
    class Meta:
        model = Email

class WebsiteForm(forms.ModelForm):
    class Meta:
        model = Website

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        exclude = ('addresses','telephones','emails','websites',)
        
class SearchForm(forms.Form):
    first = forms.CharField(required=False,help_text="First Name")
    last = forms.CharField(required=False,help_text="Last Name")
    
    
class AdvancedSearchForm(forms.Form):
    first = forms.CharField(required=False)
    last = forms.CharField(required=False)
    line1 = forms.CharField(label="Address Line 1",required=False)
    line2 = forms.CharField(label="Address Line 2",required=False)
    line3 = forms.CharField(label="Address Line 3",required=False)
    city = forms.CharField(required=False)
    state = forms.CharField(required=False)
    zip = forms.CharField(required=False)
    country = forms.ChoiceField(choices=[('','--------')]+list(Country.objects.order_by('name').values_list('code','name')),required=False)
    phone = forms.CharField(label='Telephone Number',required=False)
    has_phone = forms.BooleanField(label='Has a telephone number?', required=False)
    email = forms.CharField(label='Email Address',required=False)
    website = forms.CharField(label='Website',required=False)
    
class ExportForm(forms.Form):
    ids = forms.CharField(required=True,help_text="Primary keys", widget=forms.HiddenInput)
    
class ListWrapper:
    def __init__(self,lst):
        self._list = lst
    def count(self):
        return len(self._list)
    def __getitem__(self,i):
        return self._list[i]
        
def find_person(request,lastname,firstname):
    try:
        person = Person.objects.get(slug_last__iexact=lastname,slug_first__iexact=firstname)
        return ListWrapper([person])
    except Person.DoesNotExist:
        qs = Person.objects.filter(last_name__istartswith=lastname, first_name__istartswith=firstname)
        if qs.count()>0:
            return qs
        qs = Person.objects.filter(last_name__istartswith=lastname)
        return qs


def index(request):
    if request.GET.get('new', False):
        return person_edit(request)
    #return person_search(request,None)
    mode = request.GET.get('mode', 'normal')
    mode = mode.lower()
    if request.method == 'POST':
        if mode=='advanced':
            form = AdvancedSearchForm(request.POST,request.FILES)
        else:
            form = SearchForm(request.POST,request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            qs = Person.objects
            all = True
            fields = [ ('first','first_name__istartswith'),
                      ('last','last_name__istartswith'),
                      ('line1', 'addresses__line1__icontains'),
                      ('line2', 'addresses__line2__icontains'),
                      ('line3', 'addresses__line3__icontains'),
                      ('city', 'addresses__city__icontains'),
                      ('state', 'addresses__state__icontains'),
                      ('zip', 'addresses__zip__icontains'),
                      ('country', 'addresses__state__country__name__icontains'),
                      ('phone', 'telephones__number__contains' ),
                      ('email', 'emails__email__icontains'),
                      ('website','websites__url__icontains'),
                       ]
            for name,query in fields:
                try:
                    if data[name] and re.match('[a-zA-Z0-9]+',data[name]):
                        qs = eval('qs.filter('+query+'="'+data[name]+'")')
                        all = False
                except KeyError:
                    pass
            if data['has_phone']:
                all = False
                qs = qs.filter(telephones__number__regex=r'[0-9]+')
                #data['has_phone'] = not data['has_phone']
            if all:
                qs = qs.all()
            return do_person_search(request,qs)
    else:
        if mode=='advanced':
            form = AdvancedSearchForm()
        else:
            form = SearchForm()
    context = {'form':form, 'mode':mode, 'title':'Our Address Book'}
    return render_to_response('addressbook/index.html',context,context_instance=RequestContext(request))

def person_search(request,query):
    if query:
        qs = Person.objects.filter(last_name__istartswith=query)
    else:
        qs = Person.objects.all()
    return do_person_search(request, qs)
        
def do_person_search(request,queryset):
    def get_url(object):
        e = object.primary_email()
        if e:
            return e.url()
        return None
    
    table = Table( [ TableColumn('First Name','first_name',url=True, clazz="name"),
                    TableColumn('Last Name','last_name',url=True, clazz="name"),
                    TableColumn('Address','primary_address()',sort=False,url=False, clazz="address"),
                    TableColumn('Telephone','primary_telephone()',sort=False,url=False),
                    TableColumn('Email','primary_email()',sort=False, 
                                url=get_url),
                    ],
                    context={'title':'Our Address Book', 'table_class':'addressbook'},
                    default='last_name'
                    )
    table.paginate(request,queryset)
    table.context['export_form'] = ExportForm({ 'ids':','.join([str(qs.pk) for qs in queryset]) })
    return render_to_response('addressbook/person_list.html',table.context,context_instance=RequestContext(request))
            
def person_by_name(request,lastname,firstname):
    qs = find_person(request,lastname,firstname)
    if not qs:
        raise http.Http404
    if qs.count()>1:
        return do_person_search(request,qs)
    person = qs[0]
    context = { 'object':person,
               'title':'%s %s'%(person.first_name,person.last_name),
               'is_popup':request.GET.get('print',False) }
    return render_to_response('addressbook/person_detail.html',context,context_instance=RequestContext(request))

@login_required
def person_edit(request,object_id=None,lastname=None,firstname=None):
    AddressFormSet = modelformset_factory(Address, form=AddressForm, can_delete=True)
    TelephoneFormSet = modelformset_factory(Telephone, form=TelephoneForm, can_delete=True)
    EmailFormSet = modelformset_factory(Email, form=EmailForm, can_delete=True)
    WebsiteFormSet = modelformset_factory(Website, form=WebsiteForm, can_delete=True)
    if object_id:
        try:
            person = Person.objects.get(pk=object_id)
        except Person.DoesNotExist:
            raise http.Http404
    elif firstname and lastname:
        qs = find_person(request,lastname,firstname)
        if qs.count()>1:
            return http.HttpResponseRedirect(reverse('intranet.addressbook.views.personsearch',args=[lastname]))
        person = qs[0]
    else:
        person = None
    if request.method == 'POST':
        if request.POST.has_key('cancel'):
            return http.HttpResponseRedirect("..")
        if request.POST.has_key('delete'):
            if object_id:
                return http.HttpResponseRedirect(reverse('intranet.addressbook.views.person_delete',args=[person.slug_last,person.slug_first]))
            else:
                return http.HttpResponseRedirect(reverse('intranet.addressbook.views.person_delete',args=[lastname,firstname]))
        if person:        
            form = PersonForm(request.POST,request.FILES,instance=person,prefix="person")
            addr = AddressFormSet(request.POST,request.FILES,queryset=person.addresses.all(),prefix="addr")
            tel = TelephoneFormSet(request.POST,request.FILES,queryset=person.telephones.all(),prefix="tel")
            email = EmailFormSet(request.POST,request.FILES,queryset=person.emails.all(),prefix="email")
            web = WebsiteFormSet(request.POST,request.FILES,queryset=person.websites.all(),prefix="web")
        else:
            form = PersonForm(request.POST,request.FILES,prefix="person")
            addr = AddressFormSet(request.POST,request.FILES,queryset=Address.objects.none(),prefix="addr")
            tel = TelephoneFormSet(request.POST,request.FILES,queryset=Telephone.objects.none(),prefix="tel")
            email = EmailFormSet(request.POST,request.FILES,queryset=Email.objects.none(),prefix="email")
            web = WebsiteFormSet(request.POST,request.FILES,queryset=Website.objects.none(),prefix="web")
        if form.is_valid() and addr.is_valid() and tel.is_valid() and email.is_valid() and web.is_valid():
            if person:
                person = form.save(commit=False)
            else:
                person = form.save()
            for a in addr.save():
                person.addresses.add(a)
            for t in tel.save():
                person.telephones.add(t)
            for e in email.save():
                person.emails.add(e)
            for w in web.save():
                person.websites.add(w) 
            person.save()
            return http.HttpResponseRedirect(person.get_absolute_url())       
    elif person:
        form = PersonForm(instance=person,prefix="person")
        addr = AddressFormSet(queryset=person.addresses.all(),prefix="addr")
        tel = TelephoneFormSet(queryset=person.telephones.all(),prefix="tel")
        email = EmailFormSet(queryset=person.emails.all(),prefix="email")
        web = WebsiteFormSet(queryset=person.websites.all(),prefix="web")
    else:
        form = PersonForm(prefix="person")
        addr = AddressFormSet(queryset=Address.objects.none(),prefix="addr")
        tel = TelephoneFormSet(queryset=Telephone.objects.none(),prefix="tel")
        email = EmailFormSet(queryset=Email.objects.none(),prefix="email")
        web = WebsiteFormSet(queryset=Website.objects.none(),prefix="web")
    context = { 'object':person, 'person':form, 'telephones':tel, 'emails':email,
               'websites':web, 'addresses':addr }
    if person:
        context['title']='Edit %s %s'%(person.first_name,person.last_name)
        context['can_delete']=True
    else:
        context['title']='New Addressbook Entry'
    return render_to_response('addressbook/person_edit.html',context,context_instance=RequestContext(request))

@login_required
def person_delete(request,lastname=None,firstname=None):
    qs = find_person(request,lastname,firstname)
    if qs.count()>1:
        return http.HttpResponseRedirect(reverse('intranet.addressbook.views.personsearch',args=[lastname]))
    object = qs[0]
    del qs
    if request.method == 'POST':
        if request.POST.has_key('cancel'):
            return http.HttpResponseRedirect(reverse('intranet.addressbook.views.person_by_name',args=[lastname,firstname]))
        for a in list(object.addresses.all())+list(object.telephones.all())+list(object.emails.all())+list(object.websites.all()):
            a.delete()
        object.delete()
        return http.HttpResponseRedirect(reverse('intranet.addressbook.views.index'))
    return render_to_response('addressbook/person_delete.html',locals(),context_instance=RequestContext(request))

def vcard_export(request):
    filename = 'addresses'
    if request.method == 'POST':
        form = ExportForm(request.POST,request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            qs = Person.objects.filter(pk__in=data['ids'].split(','))
            result = []
            for person in qs:
                print(person)
                vc = vobject.vCard()
                vc.add('n')
                vc.n.value = vobject.vcard.Name(family=person.last_name, given=person.first_name)
                vc.add('fn')
                vc.fn.value = ' '.join([person.first_name,person.last_name])
                for email in person.emails.all():
                    obj = vc.add('email')
                    obj.value = email.email
                    obj.type_param = email.location.value
                for tel in person.telephones.all():
                    obj = vc.add('tel')
                    obj.value = tel.number
                    obj.type_param = ','.join([tel.location.value,tel.get_type_display()])
                for addr in person.addresses.all():
                    obj = vc.add('adr')
                    street = ''
                    if addr.line1:
                        street = [addr.line1]
                    if addr.line2:
                        street.append(addr.line2)
                    if addr.line3:
                        street.append(addr.line3)
                    region=addr.state.long_name if addr.state else ''
                    country=addr.state.country.name if addr.state else ''
                    obj.value = vobject.vcard.Address(street=street, city=addr.city, region=region, country=country, code=addr.zip)
                    obj.type_param = addr.location.value
                if person.image:
                    obj = vc.add('photo')
                    obj.value = person.image
                    obj.value_param='URL'
                vc.add('rev').value = person.modified.isoformat()
                result.append(vc.serialize())
            if len(result)==1:
                filename = '_'.join([qs[0].first_name, qs[0].last_name])
            else:
                filename += '-'+datetime.datetime.now().date().isoformat()
            resp = http.HttpResponse('\n\n'.join(result),content_type='text/vcard')
            resp['Content-Disposition'] = 'attachment; filename="'+filename+'.vcf"'
            return resp
    raise http.Http404
        
class AddressbookSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Person.objects.all()

    def lastmod(self, obj):
        return obj.modified
    