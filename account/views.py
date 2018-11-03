from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.contrib import messages
from home.models import User

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
                    response = redirect('/campusHome')
                    return response
                elif user.is_communitypartner:
                    login(request, user)
                    response = redirect('/CommunityHome')
                    return response
                elif user.is_superuser:
                    return admin(request)

            else:
                messages.error(request, 'Email or Password is incorrect')
                return redirect('/account/loginPage/')
                #return HttpResponse('Invalid Credentials')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


def campushome(request):
    return render(request, 'home/Campus_Home.html',{'campushome': campushome})


def CommunityHome(request):
    return render(request, 'home/Community_Home.html',{'CommunityHome': CommunityHome})


def admin(request):
    return render(request, 'home/CpiHome.html',{'admin': admin})
