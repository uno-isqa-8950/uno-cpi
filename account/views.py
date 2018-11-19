from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm
from django.contrib import messages


# Create your views here.


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, email=cd['email'], password=cd['password'])
            if user is not None:
                if user.is_campuspartner:
                    login(request, user)
                    response = redirect('/campususerproject')
                    return response
                elif user.is_communitypartner:
                    login(request, user)
                    response = redirect('/communitypartnerproject')
                    return response
                elif user.is_superuser:
                    login(request, user)
                    response = redirect('/AdminHome')
                    return response
            else:
                messages.error(request, 'Email or Password is incorrect')
                return redirect('/account/loginPage/')
                #return HttpResponse('Invalid Credentials')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


def campushome(request):
    return render(request, 'projects/Projectlist.html',{'campushome': campushome})


def CommunityHome(request):
    return render(request, 'projects/community_partner_projects.html',{'CommunityHome': CommunityHome})


def admin(request):
    return render(request, "home/admin_frame.html",{'admin': admin})


def logout_view(request):
    logout(request)