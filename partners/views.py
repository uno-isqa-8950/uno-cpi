from django.forms import formset_factory
from .forms import CampusPartnerForm, CampusPartnerContactForm
from django.shortcuts import render

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
    campus_partner_form = CampusPartnerForm(request.POST or None)
    if campus_partner_form.is_valid():
           new_campus_partner= campus_partner_form.save()
           contact_formset = CampusPartnerContactForm(request.POST or None, request.FILES or None, instance=new_campus_partner)
           if contact_formset.is_valid():
            contact_formset.save()
            return render(request, 'home/community_partner_register_done.html', )

    else:
        contact_formset = CampusPartnerContactForm(request.POST or None, request.FILES or None,)
    return render(request,
                  'registration/campus_partner_register.html',
                  {'campus_partner_form': campus_partner_form, 'contact_formset': contact_formset})




