
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory, modelformset_factory
from django.template import context

from home.models import Contact
from partners.models import CampusPartner
from .forms import CampusPartnerForm, CampusPartnerContactForm

from django.shortcuts import render, redirect

'''
def registerCampusPartner(request):
    if request.method == 'POST':
        campus_partner_form = CampusPartnerForm(request.POST)
        campus_partner_contact_form = CampusPartnerForm(request.POST)


        if campus_partner_form.is_valid() and campus_partner_contact_form.is_valid():
            campus_partner_contact_form.save()
            campus_partner_form.save()
            return render(request, 'home/community_partner_register_done.html', )
    else:
        campus_partner_form = CampusPartnerForm()
        campus_partner_contact_form = CampusPartnerContactForm()
    return render(request,
                  'registration/campus_partner_register.html',
                  {'campus_partner_form': campus_partner_form, 'campus_partner_contact_form': campus_partner_contact_form})


'''


def registerCampusPartner(request):
    ContactFormset = modelformset_factory(Contact, extra=1, form=CampusPartnerContactForm)
    if request.method == 'POST':
        campus_partner_form = CampusPartnerForm(request.POST )

        formset = ContactFormset(request.POST or None)

        if campus_partner_form.is_valid() and formset.is_valid():
                campus_partner = campus_partner_form.save()
                contacts = formset.save(commit=False)
                print(contacts)
                for contact in contacts:
                 contact.campus_partner = campus_partner
                 contact.save()
                 print(contact)
                return render(request, 'home/community_partner_register_done.html')

    else:
        campus_partner_form = CampusPartnerForm()
        formset = ContactFormset(queryset=Contact.objects.none())
    return render(request,
                  'registration/campus_partner_register.html',
                  {'campus_partner_form': campus_partner_form, 'formset': formset})




