from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from home.models import User

# Create your views here.


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_campuspartner:
                    login(request, user)
                    print("test")
                    return render(request, 'home/Campus_Home.html')
                elif user.is_communitypartner:
                    login(request, user)
                    return render(request, 'home/Community_Home.html')

            else:
                return HttpResponse('Invalid Credentials')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

