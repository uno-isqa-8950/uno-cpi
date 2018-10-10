from django.forms import formset_factory
from .forms import *
from django.shortcuts import render
from .models import CampusPartner as CampusPartnerModel
from home.models import Contact as ContactModel, Contact
from projects.models import *
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory, modelformset_factory
from django.template import context
from partners.models import *



def registerCampusPartner(request):
    ContactFormset = modelformset_factory(Contact, extra=1, form=CampusPartnerContactForm)
    if request.method == 'POST':
        campus_partner_form = CampusPartnerForm(request.POST)

        formset = ContactFormset(request.POST or None)

        if campus_partner_form.is_valid() and formset.is_valid():
                campus_partner = campus_partner_form.save()
                contacts = formset.save(commit=False)
                for contact in contacts:
                 contact.campus_partner = campus_partner
                 contact.save()
                 print(contact)
                return render(request, 'registration/community_partner_register_done.html')


    else:
        campus_partner_form = CampusPartnerForm()
        formset = ContactFormset(queryset=Contact.objects.none())
    return render(request,
                  'registration/campus_partner_register.html',
                  {'campus_partner_form': campus_partner_form, 'formset': formset})


# Campus Partner User Profile

# @login_required
# def campusPartnerUserProfile(request):

#   # campus_partner_form = CampusPartnerFormProfile(request.POST or None)

#   # We should get the partner by some unique ID directly based on the login information
#   # current_campus_partner = CampusPartnerModel.objects.get(name="unique name")
#   # Use try catch for using .get

#   # current_campus_partner = CampusPartnerModel.objects.all()[0]
#   # campus_partner_name = current_campus_partner.name
#   # college = current_campus_partner.college
#   # department = current_campus_partner.department

#   # # Contact details from Contact Model
#   # # We should use objects.get(campus_partner=current_campus_partner)
#   # # as it gets the unqiue object mapping result in try catch. 
  

  try:
    partner_contact = ContactModel.objects.get(
      campus_partner=current_campus_partner
    )
    first_name = partner_contact.first_name
    last_name = partner_contact.last_name
    email = partner_contact.email_id
  except ContactModel.DoesNotExist:
    first_name = None
    last_name = None
    email = None
  return render(request,
                  'home/campus_partner_profile.html', {
                    'campus_partner_name': campus_partner_name,
                    'college': college,
                    'department': department,
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email               
                 })


def registerCommunityPartner(request):
    ContactFormsetCommunity = modelformset_factory(Contact, extra=1, form=CommunityContactForm)
    CommunityMissionFormset = modelformset_factory(CommunityPartnerMission, extra=1, form = CommunityMissionForm)
    if request.method == 'POST':
        community_partner_form = CommunityPartnerForm(request.POST)
        formset_mission = CommunityMissionFormset(request.POST)
        formset = ContactFormsetCommunity(request.POST or None)

        if community_partner_form.is_valid() and formset.is_valid():
            community_partner = community_partner_form.save()
            contacts = formset.save(commit=False)
            missions = formset_mission.save(commit=False)
            print(contacts)
            print(missions)
            for contact in contacts:
                contact.community_partner = community_partner
                contact.save()
                print(contact)
            if formset_mission.is_valid():
                for mission in missions:
                    mission.community_partner = community_partner
                    mission.save()
                    print(mission)

                    return render(request, 'registration/community_partner_register_done.html', )
    else:
        community_partner_form = CommunityPartnerForm()
        formset = ContactFormsetCommunity(queryset=Contact.objects.none())
        formset_mission= CommunityMissionFormset(queryset=CommunityPartnerMission.objects.none())

    return render(request,
                  'registration/community_partner_register.html',
                  {'community_partner_form': community_partner_form,
                   'formset': formset,
                   'formset_mission' : formset_mission}, )

# @login_required
# def campusPartnerUserProfileUpdate(request):
#   campus_partner_contact_form = CampusPartnerContactForm()
  
#   return render(request,
#                 'partners/campus_partner_user_update.html',
#                 {'campus_partner_contact_form': campus_partner_contact_form}
#               )

@login_required
def campusPartnerUserProfile(request):

  campus_user = get_object_or_404(CampusPartnerUser, user= request.user.id)

  return render(request, 'partners/campus_partner_user_profile.html', {"campus_partner_name": str(campus_user.campus_partner)})


@login_required
def campusPartnerUserProfileUpdate(request):

  campus_user = get_object_or_404(CampusPartnerUser, user= request.user.id)
  user = get_object_or_404(User, id= request.user.id)

  if request.method == 'POST':
    user_form = UserForm(data = request.POST, instance=user)

    if user_form.is_valid():
      user_form.save()
      messages.success(request, 'Your profile was successfully updated!')
      return redirect('partners:campuspartneruserprofile')
    else:
      messages.error(request, 'Please correct the error below.')

  else:
    user_form = UserForm(instance=user)

  return render(request,
                'partners/campus_partner_user_update.html',
                {'user_form': user_form, "campus_partner_name": str(campus_user.campus_partner)}
              )
