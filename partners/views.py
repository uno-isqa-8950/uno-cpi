from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from home.forms import UserForm, CampusPartnerAvatar
from .forms import *
from .models import CampusPartner as CampusPartnerModel
from projects.models import *
from partners.models import *
from home.models import Contact as ContactModel, Contact, User, MissionArea
from home.forms import userUpdateForm
from django.template.loader import render_to_string


def registerCampusPartner(request):
    ContactFormset = modelformset_factory(Contact, extra=1, form=CampusPartnerContactForm)
    colleges = []
    for object in College.objects.order_by('college_name'):
        colleges.append(object.college_name)
    departmnts = []
    for object in Department.objects.order_by('department_name'):
        departmnts.append(object.department_name)

    if request.method == 'POST':
        campus_partner_form = CampusPartnerForm(request.POST)

        formset = ContactFormset(request.POST or None)

        if campus_partner_form.is_valid() and formset.is_valid():
                campus_partner = campus_partner_form.save()
                contacts = formset.save(commit=False)
                for contact in contacts:
                 contact.campus_partner = campus_partner
                 contact.save()
                return render(request, 'registration/community_partner_register_done.html')

    else:
        campus_partner_form = CampusPartnerForm()
        formset = ContactFormset(queryset=Contact.objects.none())
    return render(request,'registration/campus_partner_register.html',{'campus_partner_form': campus_partner_form,
                                                                       'formset': formset,'colleges':colleges,'departments':departmnts})


def registerCommunityPartner(request):
    ContactFormsetCommunity = modelformset_factory(Contact, extra=1, form=CommunityContactForm)
    CommunityMissionFormset = modelformset_factory(CommunityPartnerMission, extra=1, form = CommunityMissionForm)
    commType = []
    for object in CommunityType.objects.order_by('community_type'):
        commType.append(object.community_type)

    if request.method == 'POST':
        community_partner_form = CommunityPartnerForm(request.POST)
        formset_mission = CommunityMissionFormset(request.POST)
        formset = ContactFormsetCommunity(request.POST or None)

        if community_partner_form.is_valid() and formset.is_valid():
            community_partner = community_partner_form.save()
            contacts = formset.save(commit=False)
            missions = formset_mission.save(commit=False)

            for contact in contacts:
                contact.community_partner = community_partner
                contact.save()
            if formset_mission.is_valid():
                for mission in missions:
                    mission.community_partner = community_partner
                    mission.save()

                    return render(request, 'registration/community_partner_register_done.html', )
    else:
        community_partner_form = CommunityPartnerForm()
        formset = ContactFormsetCommunity(queryset=Contact.objects.none())
        formset_mission= CommunityMissionFormset(queryset=CommunityPartnerMission.objects.none())

    return render(request,
                  'registration/community_partner_register.html',
                  {'community_partner_form': community_partner_form,
                   'formset': formset,
                   'formset_mission' : formset_mission, 'commType':commType}, )


#Campus and Community Partner user Profile

@login_required
def userProfile(request):

  if request.user.is_campuspartner:
    campus_user = get_object_or_404(CampusPartnerUser, user= request.user.id)
    return render(request, 'partners/campus_partner_user_profile.html', {"campus_partner_name": str(campus_user.campus_partner)})

  elif request.user.is_communitypartner:
    community_user = get_object_or_404(CommunityPartnerUser, user= request.user.id)
    return render(request, 'partners/community_partner_user_profile.html', {"community_partner_name": str(community_user.community_partner)})


# Campus and Community Partner User Update Profile

@login_required
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
                messages.success(request, 'Your profile was successfully updated.')
                return redirect('partners:userprofile')
            else:
                messages.error(request, 'Please correct the error below.')
                return redirect('partners:orgprofile')

        else:
            user_form = userUpdateForm(instance=user)
            avatar_form = CampusPartnerAvatar(instance=user)

        return render(request,
                          'partners/campus_partner_user_update.html', {'user_form': user_form,
                          "campus_partner_name": str(campus_user.campus_partner), 'avatar_form': avatar_form
                          })

    elif request.user.is_communitypartner:

        community_user = get_object_or_404(CommunityPartnerUser, user=request.user.id)
        user = get_object_or_404(User, id=request.user.id)

        if request.method == 'POST':
            user_form = userUpdateForm(data=request.POST, instance=user)
            avatar_form = CampusPartnerAvatar(data=request.POST, files=request.FILES, instance=user)

            if user_form.is_valid()and avatar_form.is_valid():
                user_form.save()
                avatar_form.save()
                messages.success(request, 'Your profile was successfully updated.')
                return redirect('partners:userprofile')
            else:
                messages.error(request, 'Please correct the error below.')
                return redirect('partners:orgprofile')

        else:
            user_form = userUpdateForm(instance=user)
            avatar_form = CampusPartnerAvatar(instance=user)

        return render(request,
                      'partners/community_partner_user_update.html',
                      {'user_form': user_form, 'community_partner_name': str(community_user.community_partner),
                       'avatar_form': avatar_form}
                    )


# Community Partner org Profile

@login_required
def orgProfile(request):
    if request.user.is_communitypartner:
        community_user = get_object_or_404(CommunityPartnerUser, user= request.user.id)
        community_partner = get_object_or_404(CommunityPartner, id= community_user.id)
        community_partner.type = str(community_partner.community_type)
        contacts = Contact.objects.values().filter(community_partner= community_partner.id)
        missions = CommunityPartnerMission.objects.values().filter(community_partner= community_partner.id)

        for mission in missions:
            mission['mission_area'] = str(MissionArea.objects.only('mission_name').get(id = mission['mission_area_id']))

        return render(request, 'partners/community_partner_org_profile.html', {"missions":missions,
                           "community_partner": community_partner, "contacts":contacts
                           })

    elif request.user.is_campuspartner:
        campus_user = get_object_or_404(CampusPartnerUser, user=request.user.id)
        campus_partner = get_object_or_404(CampusPartner, pk=campus_user.id)
        contacts = Contact.objects.filter(campus_partner= campus_partner.id)

        return render(request, 'partners/campus_partner_org_profile.html', {"contacts":contacts,
                               "campus_partner": campus_partner
                           })


# Community Partner org Update Profile

@login_required
def orgProfileUpdate(request):

    if request.user.is_communitypartner:
        community_user = get_object_or_404(CommunityPartnerUser, user= request.user.id)
        community_partner = get_object_or_404(CommunityPartner, pk= community_user.id)
        org_type = str(community_partner.community_type)
        contacts = Contact.objects.filter(community_partner= community_partner.id).first()
        missions = CommunityPartnerMission.objects.filter(community_partner= community_partner.id).first()

        if request.method == 'POST':
            if "k12_level" not in request.POST:
                request.POST._mutable = True
                request.POST['k12_level'] = community_partner.k12_level
                request.POST._mutable = False

            community_org_form = CommunityPartnerForm(data=request.POST, instance=community_partner)
            contacts_form = CommunityContactForm(data=request.POST, instance=contacts)
            missions_form = CommunityMissionForm(data=request.POST, instance=missions)

            if community_org_form.is_valid() and contacts_form.is_valid() and missions_form.is_valid():
                community_org_form.save()
                contacts_form.save()
                missions_form.save()
                messages.success(request, 'Organization profile was successfully updated.')
                return redirect('partners:orgprofile')
            else:
                messages.error(request, 'Please correct the error below.')
                return redirect('partners:orgprofileupdate')

        else:
            community_org_form = CommunityPartnerForm(instance=community_partner)
            contacts_form = CommunityContactForm(instance=contacts)
            missions_form = CommunityMissionForm(instance=missions)

        return render(request,
                          'partners/community_partner_org_update.html', {'missions_form': missions_form,
                          'contacts_form': contacts_form, 'community_org_form': community_org_form,
                          'org_type' : org_type,
                          })

    elif request.user.is_campuspartner:
        campus_user = get_object_or_404(CampusPartnerUser, user=request.user.id)
        campus_partner = get_object_or_404(CampusPartner, pk=campus_user.id)
        contacts = Contact.objects.filter(campus_partner=campus_partner.id).first()

        if request.method == 'POST':
            campus_org_form = CampusPartnerForm(data=request.POST, instance=campus_partner)
            contacts_form = CampusPartnerContactForm(data=request.POST, instance=contacts)

            if contacts_form.is_valid():
                contacts_form.save()
                messages.success(request, 'Organization profile was successfully updated.')
                return redirect('partners:orgprofile')
            else:
                messages.error(request, 'Please correct the error below.')
                return redirect('partners:orgprofileupdate')

        else:
            campus_org_form = CampusPartnerForm(instance=campus_partner)
            contacts_form = CampusPartnerContactForm(instance=contacts)

        return render(request,
                          'partners/campus_partner_org_update.html', {'campus_org_form': campus_org_form,
                          'contacts_form': contacts_form
                          })

