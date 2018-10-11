from django.forms import formset_factory
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms import modelformset_factory
from django.shortcuts import render, redirect
from .forms import CampusPartnerForm, CampusPartnerContactForm, CampusPartnerFormProfile
from .models import CampusPartner as CampusPartnerModel
from home.models import Contact as ContactModel, Contact, User
from home.forms import userUpdateForm
from partners.models import CampusPartner, CampusPartnerUser
from .forms import CampusPartnerForm, CampusPartnerContactForm


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
                return render(request, 'home/community_partner_register_done.html')

    else:
        campus_partner_form = CampusPartnerForm()
        formset = ContactFormset(queryset=Contact.objects.none())
    return render(request,
                  'registration/campus_partner_register.html',
                  {'campus_partner_form': campus_partner_form, 'formset': formset})


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
  
#   # campus_user = CampusPartnerUser.objects.get(
#   #     user= request.user.id)

#   campus_user = get_object_or_404(CampusPartnerUser, user= request.user.id)

#   if not campus_user:
#     return HttpResponseNotFound('<h1>Page not found</h1>')

#   campus_partner_contact = ContactModel.objects.get(
#     campus_partner=campus_user.campus_partner
#     )

#   return render(request, 'partners/campus_partner_user_profile.html', {"data": campus_partner_contact})


# @login_required
# def campusPartnerUserProfileUpdate(request):
#   campus_partner_contact_form = CampusPartnerContactForm()
  
#   return render(request,
#                 'partners/campus_partner_user_update.html',
#                 {'campus_partner_contact_form': campus_partner_contact_form}
#               )


# Campus Partner User Profile

@login_required
def campusPartnerUserProfile(request):

  campus_user = get_object_or_404(CampusPartnerUser, user= request.user.id)

  return render(request, 'partners/campus_partner_user_profile.html', {"campus_partner_name": str(campus_user.campus_partner)})

# Campus Partner User Update Profile

@login_required
def campusPartnerUserProfileUpdate(request):
  campus_user = get_object_or_404(CampusPartnerUser, user= request.user.id)
  user = get_object_or_404(User, id= request.user.id)

  if request.method == 'POST':
    user_form = userUpdateForm(data = request.POST, instance=user)

    if user_form.is_valid():
      user_form.save()
      messages.success(request, 'Your profile was successfully updated!')
      return redirect('partners:campuspartneruserprofile')
    else:
      messages.error(request, 'Please correct the error below.')

  else:
    user_form = userUpdateForm(instance=user)

  return render(request,
                'partners/campus_partner_user_update.html',
                {'user_form': user_form, "campus_partner_name": str(campus_user.campus_partner)}
              )