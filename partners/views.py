from django.forms import formset_factory

from home.forms import UserForm, CampusPartnerAvatar
from .forms import *
from django.shortcuts import render, get_object_or_404, redirect
from django.forms import modelformset_factory
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import *
from .models import CampusPartner as CampusPartnerModel
from projects.models import *
from partners.models import *
from home.models import Contact as ContactModel, Contact, User
from home.forms import userUpdateForm


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

'''
def campusPartnerUserProfile(request):

  campus_user = get_object_or_404(CampusPartnerUser, user= request.user.id)

  return render(request, 'partners/campus_partner_user_profile.html', {"campus_partner_name": str(campus_user.campus_partner)})

def campusPartnerUserProfileUpdate(request):
  campus_user = get_object_or_404(CampusPartnerUser, user= request.user.id)
  user = get_object_or_404(User, id= request.user.id)

  if request.method == 'POST':
    user_form = userUpdateForm(data = request.POST, instance=user)
    avatar_form = CampusPartnerAvatar(data = request.POST,files=request.FILES, instance=user)

    if user_form.is_valid() and avatar_form.is_valid():
       user_form.save()
       print(avatar_form)
       avatar_form.save()


       messages.success(request, 'Your profile was successfully updated!')
       return redirect('partners:campuspartneruserprofile')
    else:
      messages.error(request, 'Please correct the error below.')

  else:
    user_form = userUpdateForm(instance=user)
    avatar_form = CampusPartnerAvatar(instance=user)
  return render(request,
                'partners/campus_partner_user_update.html',
                {'user_form': user_form, "campus_partner_name": str(campus_user.campus_partner),
                 'avatar_form' :avatar_form}
              )
'''
#Campus and Community Partner user Profile

def userProfile(request):

  if request.user.is_campuspartner:
    campus_user = get_object_or_404(CampusPartnerUser, user= request.user.id)
    return render(request, 'partners/campus_partner_user_profile.html', {"campus_partner_name": str(campus_user.campus_partner)})

  elif request.user.is_communitypartner:
    community_user = get_object_or_404(CommunityPartnerUser, user= request.user.id)
    return render(request, 'partners/community_partner_user_profile.html', {"community_partner_name": str(community_user.community_partner)})


# Campus and Community Partner User Update Profile

def userProfileUpdate(request):
    if request.user.is_campuspartner:

        campus_user = get_object_or_404(CampusPartnerUser, user=request.user.id)
        user = get_object_or_404(User, id=request.user.id)

        if request.method == 'POST':
            user_form = userUpdateForm(data=request.POST, instance=user)
            avatar_form = CampusPartnerAvatar(data=request.POST, files=request.FILES, instance=user)

            if user_form.is_valid() and avatar_form.is_valid():
                user_form.save()
                avatar_form.save()
                messages.success(request, 'Your profile was successfully updated!')
                return redirect('partners:userprofile')
            else:
                messages.error(request, 'Please correct the error below.')

        else:
            user_form = userUpdateForm(instance=user)
            avatar_form = CampusPartnerAvatar(instance=user)
        return render(request,
                          'partners/campus_partner_user_update.html',
                          {'user_form': user_form, "campus_partner_name": str(campus_user.campus_partner),
                           'avatar_form': avatar_form}
                          )

    elif request.user.is_communitypartner:

        community_user = get_object_or_404(CommunityPartnerUser, user=request.user.id)
        user = get_object_or_404(User, id=request.user.id)

        if request.method == 'POST':
            user_form = userUpdateForm(data=request.POST, instance=user)
            avatar_form = CampusPartnerAvatar(data=request.POST, files=request.FILES, instance=user)

            if user_form.is_valid()and avatar_form.is_valid():
                user_form.save()
                avatar_form.save()
                messages.success(request, 'Your profile was successfully updated!')
                return redirect('partners:userprofile')
            else:
                messages.error(request, 'Please correct the error below.')

        else:
            user_form = userUpdateForm(instance=user)
            avatar_form = CampusPartnerAvatar(instance=user)

        return render(request,
                      'partners/community_partner_user_update.html',
                      {'user_form': user_form, 'community_partner_name': str(community_user.community_partner),
                       'avatar_form': avatar_form}
                      )

